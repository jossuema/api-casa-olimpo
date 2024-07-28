from sqlalchemy.orm import Session, joinedload
from app import schemas, models
from app.models import Cliente, Usuario, Rol

def get_cliente(db: Session, cliente_id: int) -> schemas.ClienteResponse:
    cliente = db.query(models.Cliente).options(joinedload(Cliente.usuario).joinedload(Usuario.rol)).filter(models.Cliente.id_cliente == cliente_id).first()
    print(cliente)
    print(cliente.usuario)
    print(cliente.usuario.rol)
    return cliente

def get_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.ClienteResponse]:
    clientes = db.query(models.Cliente).options(joinedload(Cliente.usuario).joinedload(Usuario.rol)).offset(skip).limit(limit).all()
    return clientes

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente is None:
        return None
    for key, value in cliente.dict().items():
        if value is not None:
            setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return db_cliente
    return None