from sqlalchemy.orm import Session
from app import schemas
from sqlalchemy.orm import joinedload
from app.models import Prenda, Categoria, Marca

def get_prenda(db: Session, prenda_id: int):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).filter(Prenda.id_prenda == prenda_id).first()

def get_prendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).offset(skip).limit(limit).all()

def get_prendas_by_categoria(db: Session, categoria_id: int, skip: int = 0, limit: int = 100):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).filter(Prenda.id_categoria == categoria_id).offset(skip).limit(limit).all()

def get_prendas_by_marca(db: Session, marca_id: int, skip: int = 0, limit: int = 100):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).filter(Prenda.id_marca == marca_id).offset(skip).limit(limit).all()

def get_prendas_by_categoria_marca(db: Session, categoria_id: int, marca_id: int, skip: int = 0, limit: int = 100):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).filter(Prenda.id_categoria == categoria_id, Prenda.id_marca == marca_id).offset(skip).limit(limit).all()

def get_prendas_by_color(db: Session, color: str, skip: int = 0, limit: int = 100):
    return db.query(Prenda).options(joinedload(Prenda.categoria), joinedload(Prenda.marca)).filter(Prenda.color_prenda == color).offset(skip).limit(limit).all()

def create_prenda(db: Session, prenda: schemas.PrendaCreate):
    db_prenda = Prenda(**prenda.dict())
    db.add(db_prenda)
    db.commit()
    db.refresh(db_prenda)
    return db_prenda

def update_prenda(db: Session, prenda_id: int, prenda: schemas.PrendaUpdate):
    db_prenda = get_prenda(db, prenda_id)
    if db_prenda is None:
        return None
    for key, value in prenda.dict().items():
        if value is not None:
            setattr(db_prenda, key, value)
    db.commit()
    db.refresh(db_prenda)
    return db_prenda

def delete_prenda(db: Session, prenda_id: int):
    db_prenda = get_prenda(db, prenda_id)
    if db_prenda:
        db.delete(db_prenda)
        db.commit()
        return db_prenda
    return None