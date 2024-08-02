from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import schemas, models, auth, controllers
from ...database import get_db

router = APIRouter()

@router.get("/", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas")
def get_prendas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return controllers.get_prendas(db, skip=skip, limit=limit)

@router.get("/{id}", response_model= schemas.PrendaResponse, description="Obtiene una prenda por su ID")
def get_prenda(id: int, db: Session = Depends(get_db)):
    db_prenda = controllers.get_prenda(db, id)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.get("/categoria/{id}", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas de una categoria")
def get_prendas_by_categoria(id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_prendas = controllers.get_prendas_by_categoria(db, id, skip=skip, limit=limit)
    if not db_prendas:
        return []
    return db_prendas

@router.get("/marca/{id}", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas de una marca")
def get_prendas_by_marca(id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_prendas = controllers.get_prendas_by_marca(db, id, skip=skip, limit=limit)
    if not db_prendas:
        return []
    return db_prendas

@router.get("/categoria/{id_categoria}/marca/{id_marca}", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas de una categoria y marca")
def get_prendas_by_categoria_marca(id_categoria: int, id_marca: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_prendas = controllers.get_prendas_by_categoria_marca(db, id_categoria, id_marca, skip=skip, limit=limit)
    if not db_prendas:
        return []
    return db_prendas

@router.get("color/{color}", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas de un color")
def get_prendas_by_color(color: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_prendas = controllers.get_prendas_by_color(db, color, skip=skip, limit=limit)
    if not db_prendas:
        return []
    return db_prendas