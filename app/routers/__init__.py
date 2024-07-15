from fastapi import APIRouter, Depends
from .admin.usuarios import router as usuario_router_admin
from .public.usuarios import router as usuario_router_public
from .admin.rol import router as rol_router
from .admin.prenda import router as prenda_router_admin
from .public.prenda import router as prenda_router_public
from app.auth import get_current_admin_user
# Importa otros routers de manera similar

router = APIRouter()

public_router = APIRouter(prefix="/api/public" , tags=["public"])
admin_router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(get_current_admin_user)])

public_router.include_router(usuario_router_public, tags=["usuarios"], prefix="/usuarios")
public_router.include_router(prenda_router_public, tags=["prendas"], prefix="/prendas")

admin_router.include_router(usuario_router_admin, tags=["usuarios"], prefix="/usuarios")
admin_router.include_router(rol_router, tags=["roles"], prefix="/roles")
admin_router.include_router(prenda_router_admin, tags=["prendas"], prefix="/prendas")

router.include_router(public_router)
router.include_router(admin_router)
# Incluye otros routers de manera similar