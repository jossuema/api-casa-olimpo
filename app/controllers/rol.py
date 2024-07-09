from sqlalchemy.orm import Session
from app import schemas, models

def get_rol(db: Session, rol_id: int):
    return db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rol).offset(skip).limit(limit).all()

def create_rol(db: Session, rol: schemas.RolCreate):
    db_rol = models.Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db: Session, rol_id: int, rol: schemas.RolUpdate):
    db_rol = get_rol(db, rol_id)
    if db_rol is None:
        return None
    for key, value in rol.dict().items():
        if value is not None:
            setattr(db_rol, key, value)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def delete_rol(db: Session, rol_id: int):
    db_rol = get_rol(db, rol_id)
    if db_rol:
        db.delete(db_rol)
        db.commit()
        return db_rol
    return None