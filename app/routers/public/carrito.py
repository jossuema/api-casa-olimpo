from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models
from app.auth import get_current_user
from app.schemas import CarritoPrendaCreate

router = APIRouter()

@router.post("/item/", response_model=schemas.CarritoResponse)
def add_carrito_item(carrito_prenda: schemas.CarritoPrendaC, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    carrito_db = controllers.get_carrito_by_cliente(db, user.id_usuario)
    if carrito_db is None:
        carrito = schemas.CarritoCreate(id_cliente=user.id_usuario)
        carrito_db = controllers.create_carrito(db=db, carrito=carrito)
    carrito_prend_db = controllers.get_carrito_prenda(db, carrito_db.id_carrito, carrito_prenda.id_prenda)
    if carrito_prend_db is not None:
        controllers.delete_carrito_prenda(db, carrito_db.id_carrito, carrito_prenda.id_prenda)
    prenda_db = controllers.get_prenda(db, carrito_prenda.id_prenda)
    if prenda_db is None:
        raise HTTPException(status_code=404, detail="Prenda not found")
    carrito_prenda = CarritoPrendaCreate(id_carrito=carrito_db.id_carrito, id_prenda=carrito_prenda.id_prenda, cantidad=carrito_prenda.cantidad_carrito_prenda)
    return controllers.create_carrito_prenda(db, carrito_prenda)

@router.get("/", response_model=schemas.CarritoResponse)
def read_carrito(db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    carrito_db = controllers.get_carrito_by_cliente(db, user.id_usuario)
    if carrito_db is None:
        raise HTTPException(status_code=404, detail="Carrito not found")
    return carrito_db

@router.delete("/", response_model=schemas.CarritoResponse)
def delete_carrito_item(db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    carrito_db = controllers.get_carrito_by_cliente(db, user.id_usuario)
    if carrito_db is None:
        raise HTTPException(status_code=404, detail="Carrito not found")
    return controllers.delete_carrito_prendas(db, carrito_db.id_carrito)

@router.delete("/item/{prenda_id}", response_model=schemas.CarritoPrenda)
def delete_carrito_item(prenda_id: int, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    carrito_db = controllers.get_carrito_by_cliente(db, user.id_usuario)
    if carrito_db is None:
        raise HTTPException(status_code=404, detail="Carrito not found")
    return controllers.delete_carrito_prenda(db, carrito_db.id_carrito, prenda_id)
