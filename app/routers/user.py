from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth
from fastapi import Depends
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = db.query(models.Usuario).filter(models.Usuario.username_usuario == user.username_usuario).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = auth.get_password_hash(user.clave_usuario)
    db_user = models.Usuario(
        username_usuario=user.username_usuario,
        clave_usuario=hashed_password,
        email_usuario=user.email_usuario,
        id_rol=user.id_rol  # Asegúrate de manejar los roles adecuadamente
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}", response_model=schemas.Usuario)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id_usuario == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
