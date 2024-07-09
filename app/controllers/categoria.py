from sqlalchemy.orm import Session
from app import schemas, models

def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id_categoria == categoria_id).first()

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaUpdate):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria is None:
        return None
    for key, value in categoria.dict().items():
        if value is not None:
            setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return db_categoria
    return None