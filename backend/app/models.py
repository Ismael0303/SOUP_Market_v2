# backend/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Enum, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from typing import List, Optional

from app.database import Base

# Enumeraciones
class UserTier(str, enum.Enum):
    CLIENTE = "cliente"
    MICROEMPRENDIMIENTO = "microemprendimiento"
    FREELANCER = "freelancer"

class UserRole(str, enum.Enum):
    TRABAJADOR_ATENCION = "trabajador_atencion"
    COCINERO = "cocinero"
    MANAGER = "manager"
    ADMIN = "admin"

class BusinessType(str, enum.Enum):
    PRODUCTOS = "PRODUCTOS"
    SERVICIOS = "SERVICIOS"
    AMBOS = "AMBOS"

class ProductType(str, enum.Enum):
    PHYSICAL_GOOD = "PHYSICAL_GOOD"
    SERVICE_BY_HOUR = "SERVICE_BY_HOUR"
    SERVICE_BY_PROJECT = "SERVICE_BY_PROJECT"
    DIGITAL_GOOD = "DIGITAL_GOOD"

class PublicidadTipo(str, enum.Enum):
    BANNER = "banner"
    LISTADO_DESTACADO = "listado_destacado"
    ANUNCIO_RED_SOCIAL = "anuncio_red_social"

# Modelos de la Base de Datos

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    tipo_tier: Mapped[UserTier] = mapped_column(Enum(UserTier), default=UserTier.CLIENTE, nullable=False)
    localizacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    curriculum_vitae: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    plugins_activos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=list)
    
    rol: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole), nullable=True)
    
    negocio_asignado_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=True)
    fecha_contratacion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    salario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    horario_trabajo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    permisos_especiales: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)

    @property
    def negocio_principal_id(self) -> Optional[UUID]:
        """Returns the ID of the first business owned by the user, or None if none."""
        if self.negocios:
            return self.negocios[0].id
        return None

    negocios: Mapped[List["Negocio"]] = relationship(
        "Negocio",
        back_populates="propietario",
        foreign_keys="[Negocio.propietario_id]",
        cascade="all, delete-orphan"
    )
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="propietario", cascade="all, delete-orphan")
    insumos: Mapped[List["Insumo"]] = relationship("Insumo", back_populates="usuario", cascade="all, delete-orphan")
    negocio_asignado: Mapped[Optional["Negocio"]] = relationship(
        "Negocio",
        foreign_keys=[negocio_asignado_id]
    )

class Negocio(Base):
    __tablename__ = "negocios"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    tipo_negocio: Mapped[BusinessType] = mapped_column(Enum(BusinessType), nullable=False)
    rubro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    localizacion_geografica: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fotos_urls: Mapped[Optional[List[str]]] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    calificacion_promedio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_calificaciones: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ventas_completadas: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    propietario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="negocios",
        foreign_keys="[Negocio.propietario_id]"
    )
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="negocio", cascade="all, delete-orphan")
    publicidades: Mapped[List["Publicidad"]] = relationship(
        "Publicidad",
        primaryjoin="and_(Publicidad.item_publicitado_id == Negocio.id, Publicidad.item_publicitado_tipo.in_(['banner', 'listado_destacado']))",
        foreign_keys="[Publicidad.item_publicitado_id]",
        viewonly=True,
        overlaps="producto_publicitado"
    )

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_producto: Mapped[ProductType] = mapped_column(Enum(ProductType), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    stock_terminado: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)

    precio_venta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margen_ganancia_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    precio_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cogs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margen_ganancia_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    rating_promedio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reviews_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    categoria: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Changed from ProductCategory to String
    codigo_lote: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fecha_vencimiento: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    fecha_produccion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    stock_minimo: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    stock_maximo: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad_venta: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="unidad")
    es_perecedero: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    tiempo_vida_util: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requiere_refrigeracion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    ingredientes: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    alergenos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    calorias_por_porcion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    peso_porcion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad_peso: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="g")

    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="productos")
    negocio: Mapped["Negocio"] = relationship("Negocio", back_populates="productos")
    insumos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="producto", cascade="all, delete-orphan")

class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    cantidad_disponible: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unidad_medida_compra: Mapped[str] = mapped_column(String, nullable=False)
    costo_unitario_compra: Mapped[float] = mapped_column(Float, nullable=False)
    usuario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="insumos")
    productos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="insumo", cascade="all, delete-orphan")

class ProductoInsumo(Base):
    __tablename__ = "producto_insumos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_asociacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    producto: Mapped["Producto"] = relationship("Producto", back_populates="insumos_asociados")
    insumo: Mapped["Insumo"] = relationship("Insumo", back_populates="productos_asociados")

class Publicidad(Base):
    __tablename__ = "publicidades"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tipo_publicidad: Mapped[PublicidadTipo] = mapped_column(Enum(PublicidadTipo), nullable=False)
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)
    item_publicitado_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    item_publicitado_tipo: Mapped[str] = mapped_column(String, nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    cliente_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    numero_venta: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    fecha_venta: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    descuento: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    impuestos: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    metodo_pago: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    estado: Mapped[str] = mapped_column(String, nullable=False, default="completada")
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    margen_ganancia_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    costo_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    negocio: Mapped["Negocio"] = relationship("Negocio")
    cliente: Mapped[Optional["Usuario"]] = relationship("Usuario", foreign_keys=[cliente_id])
    detalles: Mapped[List["DetalleVenta"]] = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    venta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    descuento_unitario: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    
    costo_unitario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margen_ganancia: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    codigo_lote: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    venta: Mapped["Venta"] = relationship("Venta", back_populates="detalles")
    producto: Mapped["Producto"] = relationship("Producto")

class CarritoCompra(Base):
    __tablename__ = "carritos_compra"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    cliente_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    negocio: Mapped["Negocio"] = relationship("Negocio")
    cliente: Mapped[Optional["Usuario"]] = relationship("Usuario", foreign_keys=[cliente_id])
    items: Mapped[List["ItemCarrito"]] = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")

class ItemCarrito(Base):
    __tablename__ = "items_carrito"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    carrito_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("carritos_compra.id"), nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_agregado: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    carrito: Mapped["CarritoCompra"] = relationship("CarritoCompra", back_populates="items")
    producto: Mapped["Producto"] = relationship("Producto")