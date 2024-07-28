from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models

router = APIRouter()

@router.post("/", response_model=schemas.ClienteResponse)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return controllers.create_cliente(db=db, cliente=cliente)

@router.get("/", response_model=List[schemas.ClienteResponse])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = controllers.get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = controllers.get_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.ClienteResponse)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = controllers.update_cliente(db, cliente_id=cliente_id, cliente=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.delete("/{cliente_id}", response_model=schemas.ClienteResponse)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = controllers.delete_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente