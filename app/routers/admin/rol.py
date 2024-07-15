from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, controllers
from app.auth import get_current_admin_user
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Rol, description="Crea un nuevo rol")
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return controllers.create_rol(db=db, rol=rol)

@router.get("/", response_model=List[schemas.Rol])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = controllers.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{rol_id}", response_model=schemas.Rol)
def read_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = controllers.get_rol(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol

@router.put("/{rol_id}", response_model=schemas.Rol)
def update_rol(rol_id: int, rol: schemas.RolUpdate, db: Session = Depends(get_db)):
    db_rol = controllers.update_rol(db, rol_id=rol_id, rol=rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol

@router.delete("/{rol_id}", response_model=schemas.Rol)
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = controllers.delete_rol(db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol