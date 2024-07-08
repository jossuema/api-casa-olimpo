from fastapi import APIRouter
from .cliente import router as cliente_router
from .user import router as user_router
# Importa otros routers de manera similar

router = APIRouter()
router.include_router(cliente_router, prefix="/clientes", tags=["clientes"])
router.include_router(user_router, prefix="/users", tags=["users"])
# Incluye otros routers de manera similar