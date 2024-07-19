from .cliente import get_cliente, get_clientes, create_cliente, update_cliente, delete_cliente
from .carrito_prenda import get_carrito_prenda, get_carrito_prendas, create_carrito_prenda, delete_carrito_prendas, delete_carrito_prenda
from .carrito import get_carrito, get_carritos, create_carrito, update_carrito, delete_carrito, get_carrito_by_cliente
from .categoria import get_categoria, get_categorias, create_categoria, update_categoria, delete_categoria
from .detalle_venta import get_detalle_venta, get_detalles_venta, create_detalle_venta, update_detalle_venta, delete_detalle_venta
from .marca import get_marca, get_marcas, create_marca, update_marca, delete_marca
from .prenda import get_prenda, get_prendas, create_prenda, update_prenda, delete_prenda, get_prendas_by_categoria, get_prendas_by_marca, get_prendas_by_categoria_marca, get_prendas_by_color
from .rol import get_rol, get_roles, create_rol, update_rol, delete_rol
from .usuario import get_usuario, get_usuarios, create_usuario, update_usuario, delete_usuario, get_usuario_by_username, get_usuario_by_email
from .venta import get_venta, get_ventas, create_venta, update_venta, delete_venta

__all__ = [
    "get_cliente",
    "get_clientes",
    "create_cliente",
    "update_cliente",
    "delete_cliente",
    "get_carrito_prenda",
    "get_carrito_prendas",
    "create_carrito_prenda",
    "delete_carrito_prendas",
    "delete_carrito_prenda",
    "get_carrito",
    "get_carritos",
    "create_carrito",
    "update_carrito",
    "delete_carrito",
    "get_categoria",
    "get_categorias",
    "create_categoria",
    "update_categoria",
    "delete_categoria",
    "get_detalle_venta",
    "get_detalles_venta",
    "create_detalle_venta",
    "update_detalle_venta",
    "delete_detalle_venta",
    "get_marca",
    "get_marcas",
    "create_marca",
    "update_marca",
    "delete_marca",
    "get_prenda",
    "get_prendas",
    "create_prenda",
    "update_prenda",
    "delete_prenda",
    "get_rol",
    "get_roles",
    "create_rol",
    "update_rol",
    "delete_rol",
    "get_usuario",
    "get_usuarios",
    "create_usuario",
    "update_usuario",
    "delete_usuario",
    "get_venta",
    "get_ventas",
    "create_venta",
    "update_venta",
    "delete_venta",
    "get_usuario_by_username",
    "get_usuario_by_email",
    "get_prendas_by_categoria",
    "get_prendas_by_marca",
    "get_prendas_by_categoria_marca",
    "get_prendas_by_color",
    "get_carrito_by_cliente"
]