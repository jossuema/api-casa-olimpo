from sqlalchemy.orm import Session
from app import schemas, models

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()

def get_usuario_by_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username_usuario == username).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email_usuario == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        return None
    for key, value in usuario.dict().items():
        if value is not None:
            setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return db_usuario
    return None
