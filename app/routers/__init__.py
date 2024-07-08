from fastapi import APIRouter
from .cliente import router as cliente_router
# Importa otros routers de manera similar

router = APIRouter()
router.include_router(cliente_router, prefix="/clientes", tags=["clientes"])
# Incluye otros routers de manera similar