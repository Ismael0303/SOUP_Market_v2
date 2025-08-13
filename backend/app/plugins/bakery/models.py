# backend/app/plugins/bakery/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Enum, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from typing import List, Optional

from app.database import Base
from app.models import Producto, Negocio, Usuario, Insumo

class ProductCategory(str, enum.Enum):
    PAN = "pan"
    PASTEL = "pastel"
    GALLETA = "galleta"
    BOLLO = "bollo"
    TARTA = "tarta"
    EMPANADA = "empanada"
    CHIPA = "chipa"
    OTRO = "otro"

class Receta(Base):
    __tablename__ = "recetas"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    creador_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    
    tiempo_preparacion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tiempo_coccion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    temperatura_horno: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rendimiento: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad_rendimiento: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dificultad: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    instrucciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    producto: Mapped["Producto"] = relationship("Producto")
    negocio: Mapped["Negocio"] = relationship("Negocio")
    creador: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[creador_id])
    ingredientes: Mapped[List["IngredienteReceta"]] = relationship("IngredienteReceta", back_populates="receta", cascade="all, delete-orphan")

class IngredienteReceta(Base):
    __tablename__ = "ingredientes_receta"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    receta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recetas.id"), nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String, nullable=False)
    orden: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    receta: Mapped["Receta"] = relationship("Receta", back_populates="ingredientes")
    insumo: Mapped["Insumo"] = relationship("Insumo")

class Produccion(Base):
    __tablename__ = "producciones"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    receta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recetas.id"), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    productor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    
    fecha_produccion: Mapped[Date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    hora_fin: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cantidad_producida: Mapped[float] = mapped_column(Float, nullable=False)
    cantidad_esperada: Mapped[float] = mapped_column(Float, nullable=False)
    rendimiento_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    calidad: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    problemas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    costo_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    costo_unitario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    estado: Mapped[str] = mapped_column(String, nullable=False, default="planificada")
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    receta: Mapped["Receta"] = relationship("Receta")
    negocio: Mapped["Negocio"] = relationship("Negocio")
    productor: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[productor_id])

class HorarioPico(Base):
    __tablename__ = "horarios_pico"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)
    hora_inicio: Mapped[str] = mapped_column(String, nullable=False)
    hora_fin: Mapped[str] = mapped_column(String, nullable=False)
    
    ventas_promedio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    productos_vendidos_promedio: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clientes_promedio: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    prioridad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    negocio: Mapped["Negocio"] = relationship("Negocio")
