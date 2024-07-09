from sqlalchemy.orm import Session
from app import schemas, models

def get_prenda(db: Session, prenda_id: int):
    return db.query(models.Prenda).filter(models.Prenda.id_prenda == prenda_id).first()

def get_prendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prenda).offset(skip).limit(limit).all()

def create_prenda(db: Session, prenda: schemas.PrendaCreate):
    db_prenda = models.Prenda(**prenda.dict())
    db.add(db_prenda)
    db.commit()
    db.refresh(db_prenda)
    return db_prenda

def update_prenda(db: Session, prenda_id: int, prenda: schemas.PrendaUpdate):
    db_prenda = get_prenda(db, prenda_id)
    if db_prenda is None:
        return None
    for key, value in prenda.dict().items():
        if value is not None:
            setattr(db_prenda, key, value)
    db.commit()
    db.refresh(db_prenda)
    return db_prenda

def delete_prenda(db: Session, prenda_id: int):
    db_prenda = get_prenda(db, prenda_id)
    if db_prenda:
        db.delete(db_prenda)
        db.commit()
        return db_prenda
    return None