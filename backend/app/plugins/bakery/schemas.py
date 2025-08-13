# backend/app/plugins/bakery/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

from app.plugins.bakery.models import ProductCategory
from app.models import ProductType

# SCHEMAS PARA PRODUCTOS MEJORADOS (PANADERÍA)
class ProductoPanaderiaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: Optional[ProductCategory] = None
    codigo_lote: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    fecha_produccion: Optional[date] = None
    stock_minimo: Optional[float] = 0.0
    stock_maximo: Optional[float] = None
    unidad_venta: Optional[str] = "unidad"
    es_perecedero: Optional[bool] = True
    tiempo_vida_util: Optional[int] = None
    requiere_refrigeracion: Optional[bool] = False
    ingredientes: Optional[List[str]] = None
    alergenos: Optional[List[str]] = None
    calorias_por_porcion: Optional[Optional[float]] = None
    peso_porcion: Optional[float] = None
    unidad_peso: Optional[str] = "g"

class ProductoPanaderiaCreate(ProductoPanaderiaBase):
    negocio_id: UUID
    tipo_producto: ProductType = ProductType.PHYSICAL_GOOD

class ProductoPanaderiaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[ProductCategory] = None
    codigo_lote: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    fecha_produccion: Optional[date] = None
    stock_minimo: Optional[float] = None
    stock_maximo: Optional[float] = None
    unidad_venta: Optional[str] = None
    es_perecedero: Optional[bool] = None
    tiempo_vida_util: Optional[int] = None
    requiere_refrigeracion: Optional[bool] = None
    ingredientes: Optional[List[str]] = None
    alergenos: Optional[List[str]] = None
    calorias_por_porcion: Optional[float] = None
    peso_porcion: Optional[float] = None
    unidad_peso: Optional[str] = None

class ProductoPanaderiaResponse(ProductoPanaderiaBase):
    id: UUID
    negocio_id: UUID
    propietario_id: UUID
    tipo_producto: ProductType
    stock_terminado: Optional[float] = None
    rating_promedio: float
    reviews_count: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)
