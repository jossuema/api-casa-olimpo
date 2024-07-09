from sqlalchemy.orm import Session
from app import schemas, models

def get_carrito_prenda(db: Session, carrito_prenda_id: int):
    return db.query(models.CarritoPrenda).filter(models.CarritoPrenda.id_carrito_prenda == carrito_prenda_id).first()

def get_carrito_prendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CarritoPrenda).offset(skip).limit(limit).all()

def create_carrito_prenda(db: Session, carrito_prenda: schemas.CarritoPrendaCreate):
    db_carrito_prenda = models.CarritoPrenda(**carrito_prenda.dict())
    db.add(db_carrito_prenda)
    db.commit()
    db.refresh(db_carrito_prenda)
    return db_carrito_prenda

def update_carrito_prenda(db: Session, carrito_prenda_id: int, carrito_prenda: schemas.CarritoPrendaUpdate):
    db_carrito_prenda = get_carrito_prenda(db, carrito_prenda_id)
    if db_carrito_prenda is None:
        return None
    for key, value in carrito_prenda.dict().items():
        if value is not None:
            setattr(db_carrito_prenda, key, value)
    db.commit()
    db.refresh(db_carrito_prenda)
    return db_carrito_prenda

def delete_carrito_prenda(db: Session, carrito_prenda_id: int):
    db_carrito_prenda = get_carrito_prenda(db, carrito_prenda_id)
    if db_carrito_prenda:
        db.delete(db_carrito_prenda)
        db.commit()
        return db_carrito_prenda
    return None