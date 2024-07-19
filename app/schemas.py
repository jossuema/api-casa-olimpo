from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import date
from decimal import Decimal


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

# Esquema de Usuario
class UsuarioBase(BaseModel):
    id_rol: Optional[int]
    username_usuario: Optional[str] = Field(None, max_length=50)
    clave_usuario: str = Field(None, max_length=200)
    email_usuario: Optional[EmailStr]

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    rol: Rol

    class Config:
        orm_mode = True
        exclude = {'clave_usuario'}

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True
        exclude = {'clave_usuario'}

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

class ClienteResponse(ClienteBase):
    id_cliente: int
    usuario_nombre: str
    usuario_rol: str

    @validator('usuario_nombre', 'usuario_rol', pre=True, always=True)
    def get_usuario_info(cls, v, values, **kwargs):
        # Intenta obtener el nombre del usuario y del rol desde el objeto usuario si está disponible
        if 'usuario' in values:
            usuario = values['usuario']
            if 'usuario_nombre' in kwargs['field'].name and usuario:
                return usuario.username_usuario
            elif 'usuario_rol' in kwargs['field'].name and usuario:
                return usuario.rol.nombre_rol
        return v

    class Config:
        orm_mode = True
        
class Cliente(ClienteBase):
    id_cliente: int

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

class PrendaResponse(PrendaBase):
    id_prenda: int
    categoria: Categoria
    marca: Marca

    class Config:
        orm_mode = True

class Prenda(PrendaBase):
    id_prenda: int

    class Config:
        orm_mode = True

# Esquema de Venta
class VentaBase(BaseModel):
    id_cliente: int
    fecha_venta: date
    total_venta: Decimal
    metodo_pago_venta: str = Field(None, max_length=50)

class VentaBaseDetalleCreate(BaseModel):
    id_prenda: int
    cantidad_detalle_venta: Optional[int]

class VentaCreate(BaseModel):
    id_cliente: int
    metodo_pago_venta: str = Field(None, max_length=50)
    prendas: List[VentaBaseDetalleCreate]

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

class DetalleVentaResponse(BaseModel):
    id_detalle_venta: int
    id_venta: int
    id_prenda: int
    cantidad_detalle_venta: Optional[int]
    total_detalle_venta: Optional[Decimal]
    prenda: Prenda

    class Config:
        orm_mode = True

class VentaResponse(VentaBase):
    id_venta: int
    fecha_venta: date
    total_venta: Decimal
    metodo_pago_venta: str = Field(None, max_length=50)
    prendas: List[DetalleVentaResponse]
    
class DetalleVenta(DetalleVentaBase):
    id_detalle_venta: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None