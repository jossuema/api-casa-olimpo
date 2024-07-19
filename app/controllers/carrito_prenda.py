from sqlalchemy.orm import Session
from app import schemas, models

def get_carrito_prenda(db: Session, id_carrito: int, id_prenda: int):
    return db.query(models.CarritoPrenda).filter(models.CarritoPrenda.id_carrito == id_carrito, models.CarritoPrenda.id_prenda == id_prenda).first()

def get_carrito_prendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CarritoPrenda).offset(skip).limit(limit).all()

def create_carrito_prenda(db: Session, carrito_prenda: schemas.CarritoPrendaCreate):
    db_carrito_prenda = models.CarritoPrenda(**carrito_prenda.dict())
    db.add(db_carrito_prenda)
    db.commit()
    db.refresh(db_carrito_prenda)
    return db_carrito_prenda

def delete_carrito_prendas(db: Session, carrito_id: int):
    db_carrito_prendas = db.query(models.CarritoPrenda).filter(models.CarritoPrenda.id_carrito == carrito_id).all()
    for carrito_prenda in db_carrito_prendas:
        db.delete(carrito_prenda)
    db.commit()
    return db_carrito_prendas

def delete_carrito_prenda(db:Session, carrito_id: int, prenda_id: int):
    db_carrito_prenda = db.query(models.CarritoPrenda).filter(models.CarritoPrenda.id_carrito == carrito_id, models.CarritoPrenda.id_prenda == prenda_id).first()
    if db_carrito_prenda:
        db.delete(db_carrito_prenda)
        db.commit()
        return db_carrito_prenda
    return None