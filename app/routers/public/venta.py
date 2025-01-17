from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas
from app.database import get_db
from app import models
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.Venta)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    cliente_db = controllers.get_cliente_by_user(db, user.id_usuario)
    venta_db = schemas.VentaBase(
        id_cliente=cliente_db.id_cliente,
        fecha_venta=datetime.now(),
        metodo_pago_venta=venta.metodo_pago_venta,
        total_venta=0
    )
    for prenda in venta.prendas:
        prenda_db = controllers.get_prenda(db, prenda.id_prenda)
        if prenda_db is None:
            raise HTTPException(status_code=404, detail="Prenda not found")
        venta_db.total_venta += prenda_db.precio_prenda * prenda.cantidad_detalle_venta
    db_venta = controllers.create_venta(db=db, venta=venta_db)
    for prenda in venta.prendas:
        prenda_db = controllers.get_prenda(db, prenda.id_prenda)
        detalle_venta = schemas.DetalleVentaCreate(
            id_venta=db_venta.id_venta,
            id_prenda=prenda.id_prenda,
            cantidad_detalle_venta=prenda.cantidad_detalle_venta,
            total_detalle_venta=prenda_db.precio_prenda * prenda.cantidad_detalle_venta
        )
        controllers.update_prenda(db, prenda.id_prenda, prenda_db.stock_prenda - prenda.cantidad_detalle_venta)
        controllers.create_detalle_venta(db=db, detalle_venta=detalle_venta)
    return db_venta
