from sqlalchemy.orm import Session
from app import schemas, models

def get_marca(db: Session, marca_id: int):
    return db.query(models.Marca).filter(models.Marca.id_marca == marca_id).first()

def get_marcas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Marca).offset(skip).limit(limit).all()

def create_marca(db: Session, marca: schemas.MarcaCreate):
    db_marca = models.Marca(**marca.dict())
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def update_marca(db: Session, marca_id: int, marca: schemas.MarcaUpdate):
    db_marca = get_marca(db, marca_id)
    if db_marca is None:
        return None
    for key, value in marca.dict().items():
        if value is not None:
            setattr(db_marca, key, value)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def delete_marca(db: Session, marca_id: int):
    db_marca = get_marca(db, marca_id)
    if db_marca:
        db.delete(db_marca)
        db.commit()
        return db_marca
    return None