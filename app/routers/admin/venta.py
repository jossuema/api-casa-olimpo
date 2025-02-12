from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app.models import Venta, DetalleVenta, Prenda
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.Venta)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    venta_db = schemas.VentaBase(
        id_cliente=venta.id_cliente,
        fecha_venta = datetime.now(),
        metodo_pago_venta=venta.metodo_pago_venta,
        total_venta=0
    )

    for prenda in venta.prendas:
        prenda_db = controllers.get_prenda(db, prenda.id_prenda)
        if prenda_db is None:
            raise HTTPException(status_code=404, detail="Prenda not found")
        venta_db.total_venta += prenda_db.precio_prenda * prenda.cantidad_detalle_venta

    db_venta = controllers.create_venta(db=db, venta=venta_db)
    print(db_venta)

    for prenda in venta.prendas:
        prenda_db = controllers.get_prenda(db, prenda.id_prenda)
        detalle_venta = schemas.DetalleVentaCreate(
            id_venta=db_venta.id_venta,
            id_prenda=prenda.id_prenda,
            cantidad_detalle_venta=prenda.cantidad_detalle_venta,
            total_detalle_venta=prenda_db.precio_prenda * prenda.cantidad_detalle_venta
        )
        controllers.update_prenda_stock(db, prenda.id_prenda, prenda_db.stock_prenda - prenda.cantidad_detalle_venta)
        controllers.create_detalle_venta(db=db, detalle_venta=detalle_venta)
    
    return db_venta

@router.get("/", response_model=List[schemas.VentaResponse])
def read_ventas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ventas_db = controllers.get_ventas(db, skip=skip, limit=limit)
    ventas = []
    for db_venta in ventas_db:
        venta = schemas.VentaResponse(
            id_venta=db_venta.id_venta,
            id_cliente=db_venta.id_cliente,
            fecha_venta=db_venta.fecha_venta,
            total_venta=db_venta.total_venta,
            metodo_pago_venta=db_venta.metodo_pago_venta,
            prendas=[]
        )
        for detalle_venta in db_venta.detalle_ventas:
            prenda = controllers.get_prenda(db, detalle_venta.id_prenda)
            detalle_venta = schemas.DetalleVentaResponse(
                id_detalle_venta=detalle_venta.id_detalle_venta,
                id_venta=detalle_venta.id_venta,
                id_prenda=detalle_venta.id_prenda,
                cantidad_detalle_venta=detalle_venta.cantidad_detalle_venta,
                total_detalle_venta=detalle_venta.total_detalle_venta,
                prenda=prenda
            )
            venta.prendas.append(detalle_venta)
        ventas.append(venta)
    return ventas

@router.get("/{venta_id}", response_model=schemas.VentaResponse)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = controllers.get_venta(db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    venta = schemas.VentaResponse(
        id_venta=db_venta.id_venta,
        id_cliente=db_venta.id_cliente,
        fecha_venta=db_venta.fecha_venta,
        total_venta=db_venta.total_venta,
        metodo_pago_venta=db_venta.metodo_pago_venta,
        prendas=[]
    )
    for detalle_venta in db_venta.detalle_ventas:
        prenda = controllers.get_prenda(db, detalle_venta.id_prenda)
        detalle_venta = schemas.DetalleVentaResponse(
            id_detalle_venta=detalle_venta.id_detalle_venta,
            id_venta=detalle_venta.id_venta,
            id_prenda=detalle_venta.id_prenda,
            cantidad_detalle_venta=detalle_venta.cantidad_detalle_venta,
            total_detalle_venta=detalle_venta.total_detalle_venta,
            prenda=prenda
        )
        venta.prendas.append(detalle_venta)
    return venta

@router.delete("/{venta_id}")
def delete_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = controllers.get_venta(db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    for detalle_venta in db_venta.detalle_ventas:
        controllers.delete_detalle_venta(db, detalle_venta.id_detalle_venta)
    controllers.delete_venta(db, venta_id)
    return {"message": "Venta borrada"}