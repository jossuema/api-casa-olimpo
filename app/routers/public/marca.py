from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models

router = APIRouter()

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