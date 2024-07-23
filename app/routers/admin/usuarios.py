from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth, controllers
from fastapi import Depends
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED, description="Crea un nuevo usuario", response_model_exclude=['clave_usuario'])
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = controllers.get_usuario_by_username(db, user.username_usuario)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = auth.get_password_hash(user.clave_usuario)
    user.clave_usuario = hashed_password
    return controllers.create_usuario(db=db, usuario=user)

@router.delete("/{id}", response_model=schemas.Usuario)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return controllers.delete_usuario(db, id)

@router.get("/", response_model=list[schemas.Usuario])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return controllers.get_usuarios(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Usuario)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{id}", response_model=schemas.Usuario)
def update_user(id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
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
    user.clave_usuario = hashed_password
    return controllers.update_usuario(db, id, user)