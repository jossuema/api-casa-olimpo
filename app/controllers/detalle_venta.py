from sqlalchemy.orm import Session
from app import schemas, models

def get_detalle_venta(db: Session, detalle_venta_id: int):
    return db.query(models.DetalleVenta).filter(models.DetalleVenta.id_detalle_venta == detalle_venta_id).first()

def get_detalles_venta(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DetalleVenta).offset(skip).limit(limit).all()

def create_detalle_venta(db: Session, detalle_venta: schemas.DetalleVentaCreate):
    db_detalle_venta = models.DetalleVenta(**detalle_venta.dict())
    db.add(db_detalle_venta)
    db.commit()
    db.refresh(db_detalle_venta)
    return db_detalle_venta

def update_detalle_venta(db: Session, detalle_venta_id: int, detalle_venta: schemas.DetalleVentaUpdate):
    db_detalle_venta = get_detalle_venta(db, detalle_venta_id)
    if db_detalle_venta is None:
        return None
    for key, value in detalle_venta.dict().items():
        if value is not None:
            setattr(db_detalle_venta, key, value)
    db.commit()
    db.refresh(db_detalle_venta)
    return db_detalle_venta

def delete_detalle_venta(db: Session, detalle_venta_id: int):
    db_detalle_venta = get_detalle_venta(db, detalle_venta_id)
    if db_detalle_venta:
        db.delete(db_detalle_venta)
        db.commit()
        return db_detalle_venta
    return None