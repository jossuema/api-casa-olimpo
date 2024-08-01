from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth, controllers
from fastapi import Depends
from ...database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED, description="Crea un nuevo usuario", response_model_exclude=['clave_usuario'])
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = controllers.get_usuario_by_username(db, user.username_usuario)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = controllers.get_usuario_by_email(db, user.email_usuario)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_base = schemas.UsuarioBase(**user.dict())
    user_base.id_rol = 2  # Asignar el rol de usuario
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = auth.get_password_hash(user_base.clave_usuario)
    user_base.clave_usuario = hashed_password
    return controllers.create_usuario(db=db, usuario=user_base)

@router.delete("/", response_model=schemas.Usuario, description="Elimina un usuario", response_model_exclude=['clave_usuario'])
def delete_user(db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    id = user.id_usuario
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return controllers.delete_usuario(db, id)

@router.put("/", response_model=schemas.Usuario, description="Actualiza un usuario", response_model_exclude=['clave_usuario'])
def update_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    id = current_user.id_usuario
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = controllers.get_usuario_by_username(db, user.username_usuario)
    if db_user and db_user.id_usuario != id:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = controllers.get_usuario_by_email(db, user.email_usuario)
    if db_user and db_user.id_usuario != id:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.clave_usuario)
    db_user = schemas.UsuarioUpdate(**user.dict())
    db_user.clave_usuario = hashed_password
    return controllers.update_usuario(db, id, db_user)

@router.get("/", response_model=schemas.Usuario, description="Obtiene un usuario", response_model_exclude=['clave_usuario'])
def read_user(db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    id = user.id_usuario
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user