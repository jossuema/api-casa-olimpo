from sqlalchemy.orm import Session, joinedload
from app import schemas, models
from typing import List

def get_venta(db: Session, venta_id: int):
    return db.query(models.Venta).options(joinedload(models.Venta.detalle_ventas).joinedload(models.DetalleVenta.prenda)).filter(models.Venta.id_venta == venta_id).first()

def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Venta).options(joinedload(models.Venta.detalle_ventas).joinedload(models.DetalleVenta.prenda)).offset(skip).limit(limit).all()

def create_venta(db: Session, venta: schemas.VentaBase):
    db_venta = models.Venta(**venta.dict())
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta

def update_venta(db: Session, venta_id: int, venta: schemas.VentaUpdate):
    db_venta = get_venta(db, venta_id)
    if db_venta is None:
        return None
    for key, value in venta.dict().items():
        if value is not None:
            setattr(db_venta, key, value)
    db.commit()
    db.refresh(db_venta)
    return db_venta

def delete_venta(db: Session, venta_id: int):
    db_venta = get_venta(db, venta_id)
    if db_venta:
        db.delete(db_venta)
        db.commit()
        return db_venta
    return None