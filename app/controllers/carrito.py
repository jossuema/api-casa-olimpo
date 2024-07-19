from sqlalchemy.orm import Session
from app import schemas, models

def get_carrito(db: Session, carrito_id: int):
    return db.query(models.Carrito).filter(models.Carrito.id_carrito == carrito_id).first()

def get_carritos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Carrito).offset(skip).limit(limit).all()

def get_carrito_by_cliente(db: Session, cliente_id: int):
    return db.query(models.Carrito).filter(models.Carrito.id_cliente == cliente_id).first()

def create_carrito(db: Session, carrito: schemas.CarritoCreate):
    db_carrito = models.Carrito(**carrito.dict())
    db.add(db_carrito)
    db.commit()
    db.refresh(db_carrito)
    return db_carrito

def update_carrito(db: Session, carrito_id: int, carrito: schemas.CarritoUpdate):
    db_carrito = get_carrito(db, carrito_id)
    if db_carrito is None:
        return None
    for key, value in carrito.dict().items():
        if value is not None:
            setattr(db_carrito, key, value)
    db.commit()
    db.refresh(db_carrito)
    return db_carrito

def delete_carrito(db: Session, carrito_id: int):
    db_carrito = get_carrito(db, carrito_id)
    if db_carrito:
        db.delete(db_carrito)
        db.commit()
        return db_carrito
    return None