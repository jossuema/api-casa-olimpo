from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth, controllers
from ...database import get_db
from app.utils import generate_img_name, generate_img_url, upload_img_prenda, delete_img_prenda, update_img_prenda
from fastapi import UploadFile, File, Form
from decimal import Decimal
from typing import Optional

router = APIRouter()

@router.get("/", response_model= list[schemas.PrendaResponse], description="Obtiene todas las prendas")
def get_prendas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    prendas = controllers.get_prendas(db, skip=skip, limit=limit)
    for prenda in prendas:
        prenda.img_prenda = generate_img_url(prenda.img_prenda)
    return prendas

@router.get("/{id}", response_model= schemas.PrendaResponse, description="Obtiene una prenda por su ID")
def get_prenda(id: int, db: Session = Depends(get_db)):
    db_prenda = controllers.get_prenda(db, id)
    db_prenda.img_prenda = generate_img_url(db_prenda.img_prenda)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.put("/{id}", response_model= schemas.Prenda)
def update_prenda(id: int, prenda: schemas.PrendaUpdate, db: Session = Depends(get_db)):
    db_prenda = controllers.update_prenda(db, id, prenda)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.put("/{id}/img", response_model= schemas.Prenda)
def update_img_prenda(id: int, img_prenda: UploadFile = File(...), db: Session = Depends(get_db)):
    db_prenda = controllers.get_prenda(db, id)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    img_name = generate_img_name(img_prenda.filename)
    update_img_prenda(img_prenda, img_name)
    db_prenda.img_prenda = img_name
    controllers.update_prenda(db, id, db_prenda)
    return db_prenda

@router.delete("/{id}", response_model= schemas.Prenda)
def delete_prenda(id: int, db: Session = Depends(get_db)):
    db_prenda = controllers.delete_prenda(db, id)
    delete_img_prenda(db_prenda.img_prenda)
    if db_prenda is None:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    return db_prenda

@router.post("/", response_model=schemas.Prenda, status_code=status.HTTP_201_CREATED, description="Crea una nueva prenda")
def create_prenda(
    id_categoria: int = Form(...),
    id_marca: int = Form(...),
    nombre_prenda: Optional[str] = Form(None),
    descripcion_prenda: Optional[str] = Form(None),
    talla_prenda: Optional[str] = Form(None),
    color_prenda: Optional[str] = Form(None),
    precio_prenda: Optional[Decimal] = Form(None),
    stock_prenda: Optional[int] = Form(0),
    img_prenda: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    categoria = db.get(models.Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")

    marca = db.get(models.Marca, id_marca)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca not found")

    img_name = generate_img_name(img_prenda.filename)
    upload_img_prenda(img_prenda, img_name)

    nueva_prenda = schemas.PrendaCreate(
        id_categoria=id_categoria,
        id_marca=id_marca,
        nombre_prenda=nombre_prenda,
        descripcion_prenda=descripcion_prenda,
        talla_prenda=talla_prenda,
        color_prenda=color_prenda,
        precio_prenda=precio_prenda,
        stock_prenda=stock_prenda,
        img_prenda=img_name
    )

    return controllers.create_prenda(db=db, prenda=nueva_prenda)