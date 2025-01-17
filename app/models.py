from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)
    cedula_cliente = Column(String(10))
    primer_nombre_cliente = Column(String(50))
    segundo_nombre_cliente = Column(String(50))
    primer_apellido_cliente = Column(String(50))
    segundo_apellido_cliente = Column(String(50))
    direccion_cliente = Column(String(100))
    ciudad_cliente = Column(String(50))
    correo_cliente = Column(String(100))

    carritos = relationship("Carrito", back_populates="cliente")
    ventas = relationship("Venta", back_populates="cliente")
    usuario = relationship("Usuario", back_populates="cliente")

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_rol = Column(Integer, ForeignKey('rol.id_rol'))
    username_usuario = Column(String(50))
    clave_usuario = Column(String(200))
    email_usuario = Column(String(100))

    rol = relationship("Rol", back_populates="usuarios")
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)

class Rol(Base):
    __tablename__ = 'rol'
    id_rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_rol = Column(String(50))
    descripcion_rol = Column(String(255))

    usuarios = relationship("Usuario", back_populates="rol")

class Carrito(Base):
    __tablename__ = 'carrito'
    id_carrito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)

    cliente = relationship("Cliente", back_populates="carritos")
    carrito_prendas = relationship("CarritoPrenda", back_populates="carrito")

class CarritoPrenda(Base):
    __tablename__ = 'carrito_prenda'
    id_carrito = Column(Integer, ForeignKey('carrito.id_carrito'), primary_key=True, nullable=False)
    id_prenda = Column(Integer, ForeignKey('prenda.id_prenda'), primary_key=True, nullable=False)
    cantidad_carrito_prenda = Column(Integer)

    carrito = relationship("Carrito", back_populates="carrito_prendas")
    prenda = relationship("Prenda", back_populates="carrito_prendas")

class Categoria(Base):
    __tablename__ = 'categoria'
    id_categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_categoria = Column(String(50))
    descripcion_categoria = Column(String(255))

    prendas = relationship("Prenda", back_populates="categoria")

class Marca(Base):
    __tablename__ = 'marca'
    id_marca = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_marca = Column(String(50))
    descripcion_marca = Column(String(255))

    prendas = relationship("Prenda", back_populates="marca")

class Prenda(Base):
    __tablename__ = 'prenda'
    id_prenda = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)
    id_marca = Column(Integer, ForeignKey('marca.id_marca'), nullable=False)
    nombre_prenda = Column(String(100))
    descripcion_prenda = Column(String(250))
    talla_prenda = Column(String(10))
    color_prenda = Column(String(30))
    precio_prenda = Column(Numeric)
    stock_prenda = Column(Integer, default=0)
    img_prenda = Column(Text)

    categoria = relationship("Categoria", back_populates="prendas")
    marca = relationship("Marca", back_populates="prendas")
    carrito_prendas = relationship("CarritoPrenda", back_populates="prenda")
    detalle_ventas = relationship("DetalleVenta", back_populates="prenda")

class Venta(Base):
    __tablename__ = 'venta'
    id_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    fecha_venta = Column(Date)
    total_venta = Column(Numeric)
    metodo_pago_venta = Column(String(50))

    cliente = relationship("Cliente", back_populates="ventas")
    detalle_ventas = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id_detalle_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey('venta.id_venta'), nullable=False)
    id_prenda = Column(Integer, ForeignKey('prenda.id_prenda'), nullable=False)
    cantidad_detalle_venta = Column(Integer)
    total_detalle_venta = Column(Numeric)

    venta = relationship("Venta", back_populates="detalle_ventas")
    prenda = relationship("Prenda", back_populates="detalle_ventas")