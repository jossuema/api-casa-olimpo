from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models

router = APIRouter()

@router.post("/", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return controllers.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=List[schemas.Categoria])
def read_categorias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categorias = controllers.get_categorias(db, skip=skip, limit=limit)
    return categorias

@router.get("/{categoria_id}", response_model=schemas.Categoria)
def read_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = controllers.get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return db_categoria

@router.put("/{categoria_id}", response_model=schemas.Categoria)
def update_categoria(categoria_id: int, categoria: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    db_categoria = controllers.update_categoria(db, categoria_id=categoria_id, categoria=categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return db_categoria

@router.delete("/{categoria_id}", response_model=schemas.Categoria)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = controllers.delete_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return db_categoria
