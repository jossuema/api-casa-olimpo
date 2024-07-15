from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models

router = APIRouter()

@router.post("/", response_model=schemas.Marca)
def create_marca(marca: schemas.MarcaCreate, db: Session = Depends(get_db)):
    return controllers.create_marca(db=db, marca=marca)

@router.get("/", response_model=List[schemas.Marca])
def read_marcas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    marcas = controllers.get_marcas(db, skip=skip, limit=limit)
    return marcas

@router.get("/{marca_id}", response_model=schemas.Marca)
def read_marca(marca_id: int, db: Session = Depends(get_db)):
    db_marca = controllers.get_marca(db, marca_id=marca_id)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return db_marca

@router.put("/{marca_id}", response_model=schemas.Marca)
def update_marca(marca_id: int, marca: schemas.MarcaUpdate, db: Session = Depends(get_db)):
    db_marca = controllers.update_marca(db, marca_id=marca_id, marca=marca)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return db_marca

@router.delete("/{marca_id}", response_model=schemas.Marca)
def delete_marca(marca_id: int, db: Session = Depends(get_db)):
    db_marca = controllers.delete_marca(db, marca_id=marca_id)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return db_marca