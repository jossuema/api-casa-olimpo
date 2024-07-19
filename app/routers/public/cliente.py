from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.database import get_db
from app import models
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return controllers.create_cliente(db=db, cliente=cliente)

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    # Verifica que el cliente pertenezca al usuario antes de mostrarlo
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id, models.Cliente.id_usuario == user.id_usuario).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    # Verifica que el cliente a actualizar pertenezca al usuario
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id, models.Cliente.id_usuario == user.id_usuario).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return controllers.update_cliente(db, cliente_id, cliente)

@router.delete("/{cliente_id}", response_model=schemas.Cliente)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db), user: schemas.Usuario = Depends(get_current_user)):
    # Verifica que el cliente a eliminar pertenezca al usuario
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id, models.Cliente.id_usuario == user.id_usuario).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return controllers.delete_cliente(db, cliente_id)