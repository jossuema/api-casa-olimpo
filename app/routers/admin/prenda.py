from fastapi import APIRouter, Depends, HTTPException, status
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

@router.put("/{id}", response_model= schemas.Prenda)
def update_prenda(id: int, prenda: schemas.PrendaUpdate, db: Session = Depends(get_db)):
    db_prenda = controllers.update_prenda(db, id, prenda)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.delete("/{id}", response_model= schemas.Prenda)
def delete_prenda(id: int, db: Session = Depends(get_db)):
    db_prenda = controllers.delete_prenda(db, id)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.post("/", response_model=schemas.Prenda, status_code=status.HTTP_201_CREATED, description="Crea una nueva prenda")
def create_prenda(prenda: schemas.PrendaCreate, db: Session = Depends(get_db)):
    categoria = db.get(models.Categoria, prenda.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")
    
    marca = db.get(models.Marca, prenda.id_marca)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca not found")
    
    return controllers.create_prenda(db=db, prenda=prenda)

