from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from fastapi.openapi.utils import get_openapi
from app.routers import router
from app.database import engine, SessionLocal, Base, get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt, logging, time
from sqlalchemy.orm import Session
from datetime import timedelta
from . import auth, models, schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.utils import enviar_correo_oauth2
from app.auth import verify_password, create_access_token
from app.models import Usuario
from datetime import datetime

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Registrar la solicitud
    start_time = time.time()  # Para medir el tiempo de la solicitud
    logger.info(f"Request: {request.method} {request.url}")

    # Procesar la solicitud y obtener la respuesta
    response = await call_next(request)

    # Calcular el tiempo que tomó procesar la solicitud
    process_time = time.time() - start_time

    # Registrar la respuesta y el tiempo de procesamiento
    logger.info(f"Response status code: {response.status_code} (Processed in {process_time:.4f} seconds)")

    return response

app.include_router(router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/verify-2fa")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API con 2FA",
        version="1.0.0",
        description="Autenticación con doble factor (2FA)",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/verify-2fa",  # Endpoint de verificación
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown():
    SessionLocal.close_all()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username_usuario == form_data.username).first()
    if not user or not verify_password(form_data.password, user.clave_usuario):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    user.generate_2fa_code()
    db.commit()
    await enviar_correo_oauth2(user.email_usuario, "Codigo de verificacion doble factor - CASA OLIMPO", user.two_fa_code)
    return {"message": "Código 2FA enviado al email", "user_id": user.id_usuario}

@app.post("/verify-2fa", response_model=schemas.Token)
def verify_2fa(form_data: OAuth2PasswordRequestForm = Depends(), code: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username_usuario == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user.two_fa_code != code or user.two_fa_expiration < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Código 2FA inválido o expirado")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username_usuario}, expires_delta=access_token_expires
    )
    user.two_fa_code = None
    user.two_fa_expiration = None
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.Usuario)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.username_usuario == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user