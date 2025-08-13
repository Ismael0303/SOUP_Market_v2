# backend/app/plugins/bakery/router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, extract
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Usuario, Negocio, Producto, Venta, DetalleVenta, UserRole
from app.plugins.bakery.models import Receta, Produccion, HorarioPico
from app.crud.venta import get_analisis_ventas, get_alertas_stock, get_productos_por_vencer
from app.schemas import VentaResponse

router = APIRouter(prefix="/bakery/{negocio_id}", tags=["Plugin: Panadería"])

# FUNCIONES DE VERIFICACIÓN DE ROLES
def verify_role(current_user: Usuario, required_roles: List[UserRole]) -> bool:
    """Verifica si el usuario tiene uno de los roles requeridos"""
    return current_user.rol in required_roles

def get_business_for_plugin(db: Session, current_user: Usuario, negocio_id: UUID) -> Negocio:
    """Obtiene el negocio para el plugin y verifica la propiedad."""
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el negocio o no tienes permisos sobre él."
        )
    
    return negocio

# DASHBOARD ESPECIALIZADO PARA PANADERÍA
@router.get("/dashboard")
def get_bakery_dashboard(
    negocio_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dashboard especializado para Panadería"""
    
    if not verify_role(current_user, [UserRole.TRABAJADOR_ATENCION, UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al dashboard"
        )
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    
    ventas_mes = db.query(func.sum(Venta.total)).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= inicio_mes
        )
    ).scalar() or 0
    
    productos_mas_vendidos = db.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label("cantidad_vendida"),
        func.sum(DetalleVenta.subtotal).label("total_ventas")
    ).join(DetalleVenta).join(Venta).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= inicio_mes
        )
    ).group_by(Producto.id, Producto.nombre).order_by(desc("cantidad_vendida")).limit(5).all()
    
    alertas_stock = get_alertas_stock(db, negocio.id)
    
    productos_vencimiento = get_productos_por_vencer(db, negocio.id, 7)
    
    horarios_pico = db.query(HorarioPico).filter(
        and_(
            HorarioPico.negocio_id == negocio.id,
            HorarioPico.activo == True
        )
    ).order_by(HorarioPico.dia_semana, HorarioPico.hora_inicio).all()
    
    return {
        "negocio": {
            "id": negocio.id,
            "nombre": negocio.nombre,
        },
        "metricas_mes": {
            "ventas_totales": ventas_mes,
            "inicio_mes": inicio_mes.isoformat(),
            "hoy": hoy.isoformat()
        },
        "productos_mas_vendidos": [
            {
                "nombre": p.nombre,
                "cantidad_vendida": p.cantidad_vendida,
                "total_ventas": p.total_ventas
            }
            for p in productos_mas_vendidos
        ],
        "alertas": {
            "stock_bajo": len(alertas_stock),
            "por_vencer": len(productos_vencimiento)
        },
        "horarios_pico": [
            {
                "dia_semana": h.dia_semana,
                "hora_inicio": h.hora_inicio,
                "hora_fin": h.hora_fin,
            }
            for h in horarios_pico
        ]
    }

# GESTIÓN DE RECETAS
@router.get("/recetas")
def get_recetas(
    negocio_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las recetas del negocio"""
    
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver recetas"
        )
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    recetas = db.query(Receta).filter(Receta.negocio_id == negocio.id).all()
    
    return {
        "recetas": [
            {
                "id": r.id,
                "nombre": r.nombre,
                "producto": r.producto.nombre,
            }
            for r in recetas
        ]
    }

@router.get("/recetas/{receta_id}")
def get_receta_detalle(
    negocio_id: UUID,
    receta_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el detalle completo de una receta"""
    
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver recetas"
        )
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    receta = db.query(Receta).filter(Receta.id == receta_id, Receta.negocio_id == negocio.id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receta no encontrada"
        )
    
    return receta

# GESTIÓN DE PRODUCCIÓN
@router.get("/produccion")
def get_producciones(
    negocio_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las producciones recientes"""
    
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver producciones"
        )
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    producciones = db.query(Produccion).filter(
        Produccion.negocio_id == negocio.id,
        Produccion.fecha_produccion >= date.today() - timedelta(days=30)
    ).order_by(desc(Produccion.fecha_produccion)).limit(20).all()
    
    return {
        "producciones": [
            {
                "id": p.id,
                "receta": p.receta.nombre,
                "producto": p.receta.producto.nombre,
                "fecha_produccion": p.fecha_produccion.isoformat(),
                "cantidad_producida": p.cantidad_producida,
                "estado": p.estado,
                "productor": p.productor.nombre
            }
            for p in producciones
        ]
    }

# ANÁLISIS DE VENTAS
@router.get("/analisis/ventas")
def get_analisis_ventas_plugin(
    negocio_id: UUID,
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Análisis de ventas por producto"""
    
    if not verify_role(current_user, [UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver análisis"
        )
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    return get_analisis_ventas(db, negocio.id, fecha_inicio, fecha_fin)

# ALERTAS
@router.get("/alertas")
def get_alertas(
    negocio_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene alertas de stock y vencimiento"""
    
    negocio = get_business_for_plugin(db, current_user, negocio_id)
    
    alertas_stock = get_alertas_stock(db, negocio.id)
    productos_vencimiento = get_productos_por_vencer(db, negocio.id, 3)
    
    return {
        "alertas_stock": alertas_stock,
        "productos_por_vencer": productos_vencimiento,
    }
