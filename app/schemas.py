# app/schemas.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date
from decimal import Decimal

# Esquema de Cliente
class ClienteBase(BaseModel):
    id_usuario: int
    cedula_cliente: Optional[str] = Field(None, max_length=10)
    primer_nombre_cliente: Optional[str] = Field(None, max_length=50)
    segundo_nombre_cliente: Optional[str] = Field(None, max_length=50)
    primer_apellido_cliente: Optional[str] = Field(None, max_length=50)
    segundo_apellido_cliente: Optional[str] = Field(None, max_length=50)
    direccion_cliente: Optional[str] = Field(None, max_length=100)
    ciudad_cliente: Optional[str] = Field(None, max_length=50)
    correo_cliente: Optional[EmailStr]

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id_cliente: int

    class Config:
        orm_mode = True

# Esquema de Usuario
class UsuarioBase(BaseModel):
    id_rol: Optional[int]
    username_usuario: Optional[str] = Field(None, max_length=50)
    clave_usuario: Optional[str] = Field(None, max_length=50)
    email_usuario: Optional[EmailStr]

class UsuarioCreate(UsuarioBase):
    id_rol: int
    username_usuario: str
    clave_usuario: str
    email_usuario: EmailStr

class UsuarioUpdate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True

# Esquema de Rol
class RolBase(BaseModel):
    nombre_rol: Optional[str] = Field(None, max_length=50)
    descripcion_rol: Optional[str] = Field(None, max_length=255)

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    pass

class Rol(RolBase):
    id_rol: int

    class Config:
        orm_mode = True

# Esquema de Carrito
class CarritoBase(BaseModel):
    id_cliente: int

class CarritoCreate(CarritoBase):
    pass

class CarritoUpdate(CarritoBase):
    pass

class Carrito(CarritoBase):
    id_carrito: int

    class Config:
        orm_mode = True

# Esquema de CarritoPrenda
class CarritoPrendaBase(BaseModel):
    id_carrito: int
    id_prenda: int
    cantidad_carrito_prenda: Optional[int]

class CarritoPrendaCreate(CarritoPrendaBase):
    pass

class CarritoPrendaUpdate(CarritoPrendaBase):
    pass

class CarritoPrenda(CarritoPrendaBase):
    class Config:
        orm_mode = True

# Esquema de Categoria
class CategoriaBase(BaseModel):
    nombre_categoria: Optional[str] = Field(None, max_length=50)
    descripcion_categoria: Optional[str] = Field(None, max_length=255)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id_categoria: int

    class Config:
        orm_mode = True

# Esquema de Marca
class MarcaBase(BaseModel):
    nombre_marca: Optional[str] = Field(None, max_length=50)
    descripcion_marca: Optional[str] = Field(None, max_length=255)

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(MarcaBase):
    pass

class Marca(MarcaBase):
    id_marca: int

    class Config:
        orm_mode = True

# Esquema de Prenda
class PrendaBase(BaseModel):
    id_categoria: int
    id_marca: int
    nombre_prenda: Optional[str] = Field(None, max_length=100)
    descripcion_prenda: Optional[str] = Field(None, max_length=250)
    talla_prenda: Optional[str] = Field(None, max_length=10)
    color_prenda: Optional[str] = Field(None, max_length=30)
    precio_prenda: Optional[Decimal]
    img_prenda: Optional[str]

class PrendaCreate(PrendaBase):
    pass

class PrendaUpdate(PrendaBase):
    pass

class Prenda(PrendaBase):
    id_prenda: int

    class Config:
        orm_mode = True

# Esquema de Venta
class VentaBase(BaseModel):
    id_cliente: int
    fecha_venta: Optional[date]
    total_venta: Optional[Decimal]
    metodo_pago_venta: Optional[str] = Field(None, max_length=50)

class VentaCreate(VentaBase):
    pass

class VentaUpdate(VentaBase):
    pass

class Venta(VentaBase):
    id_venta: int

    class Config:
        orm_mode = True

# Esquema de DetalleVenta
class DetalleVentaBase(BaseModel):
    id_venta: int
    id_prenda: int
    cantidad_detalle_venta: Optional[int]
    total_detalle_venta: Optional[Decimal]

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaUpdate(DetalleVentaBase):
    pass

class DetalleVenta(DetalleVentaBase):
    id_detalle_venta: int

    class Config:
        orm_mode = True