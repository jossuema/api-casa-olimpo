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
    user.id_rol = 2  # Asignar el rol de usuario
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = auth.get_password_hash(user.clave_usuario)
    user.clave_usuario = hashed_password
    return controllers.create_usuario(db=db, usuario=user)

@router.delete("/{id}", response_model=schemas.Usuario, description="Elimina un usuario", response_model_exclude=['clave_usuario'])
def delete_user(id: int, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    if user.id_usuario != id:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return controllers.delete_usuario(db, id)

@router.put("/{id}", response_model=schemas.Usuario, description="Actualiza un usuario", response_model_exclude=['clave_usuario'])
def update_user(id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    if current_user.id_usuario != id:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    db_user = controllers.update_usuario(db, id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{id}", response_model=schemas.Usuario, description="Obtiene un usuario", response_model_exclude=['clave_usuario'])
def read_user(id: int, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    if user.id_usuario != id:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    db_user = controllers.get_usuario(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user