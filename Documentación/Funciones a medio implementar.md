# Funcionalidades a Medio Implementar - 12 de Agosto de 2025

Este documento detalla las funcionalidades que están parcialmente implementadas en el sistema SOUP Market V2 y los pasos necesarios para completarlas.

## 1. Refactorización de Funcionalidades de Panadería a un Plugin Modular

**Objetivo:** Extraer las funcionalidades específicas de panadería (actualmente codificadas como "Ñiam") a un plugin modular y genérico llamado "Bakery". Esto mejorará la modularidad y escalabilidad del sistema.

**Estado Actual:** Las funcionalidades de panadería están hardcodeadas en `niam_router.py` y dependen de un negocio con el nombre "Ñiam". Los modelos de `Receta` y `Produccion` existen pero no están completamente integrados.

**Tareas Pendientes:**

### Fase 1: Refactorización del Backend

1.  **Crear la estructura del plugin:**
    -   [ ] Crear el directorio `backend/app/plugins/bakery`.
    -   [ ] Dentro de `bakery`, crear los archivos `__init__.py`, `router.py`, `models.py`, `schemas.py`, y `crud.py`.

2.  **Mover y Generalizar el Router:**
    -   [ ] Mover el contenido de `backend/app/routers/niam_router.py` a `backend/app/plugins/bakery/router.py`.
    -   [ ] **Generalizar la lógica del router:**
        -   Eliminar la función `get_niam_business` que busca un negocio por el nombre "Ñiam".
        -   Modificar todos los endpoints para que acepten un `negocio_id` como parámetro o lo obtengan del usuario autenticado.
        -   Renombrar el prefijo del router de `/niam` a `/bakery`.

3.  **Mover y Refinar los Modelos:**
    -   [ ] Mover los modelos `Receta`, `IngredienteReceta`, y `Produccion` de `backend/app/models.py` a `backend/app/plugins/bakery/models.py`.
    -   [ ] Revisar y generalizar los modelos si es necesario (ej. eliminar categorías de productos hardcodeadas como "chipa").
    -   [ ] Actualizar las relaciones de los modelos para que funcionen dentro del plugin.

4.  **Implementar la Carga Dinámica de Plugins:**
    -   [ ] En `backend/app/main.py`, modificar la inicialización de la aplicación para que:
        -   Lea el campo `plugins_activos` del usuario (una vez que el usuario se autentica).
        -   Si el plugin "bakery" está activo, registrar dinámicamente el router de `bakery_router.py`.
        -   Esto podría requerir un middleware o una dependencia de FastAPI que verifique los plugins activos por petición.

### Fase 2: Implementación del Frontend

1.  **Crear la Interfaz de Gestión de Plugins:**
    -   [ ] Crear una nueva pantalla `PluginsScreen.js`.
    -   [ ] En esta pantalla, mostrar una lista de plugins disponibles (inicialmente, solo "Bakery Tools").
    -   [ ] Permitir al usuario activar o desactivar el plugin "Bakery Tools". Esta acción debe actualizar el campo `plugins_activos` del usuario en la base de datos a través de una llamada a la API.

2.  **Renderizado Condicional de la Interfaz de Panadería:**
    -   [ ] En el frontend, obtener la lista de plugins activos del usuario al iniciar sesión.
    -   [ ] Modificar la barra de navegación y el dashboard para que:
        -   Muestren los enlaces a "Recetas" y "Producción" solo si el plugin "bakery" está activo.
    -   [ ] Crear las pantallas para gestionar recetas y producción (`RecipeScreen.js`, `ProductionScreen.js`) y asegurarse de que solo sean accesibles si el plugin está activo.

### Fase 3: Actualización de la Documentación y Limpieza

1.  **Actualizar la Documentación:**
    -   [ ] Actualizar la `DOCUMENTACION_TECNICA.md` para reflejar la nueva arquitectura de plugins.
    -   [ ] Eliminar las referencias a "Ñiam" de la documentación.
2.  **Limpieza del Código:**
    -   [ ] Eliminar el archivo `backend/app/routers/niam_router.py`.
    -   [ ] Eliminar los scripts de migración y testing relacionados con "Ñiam" en la carpeta `debugging`.

## 2. Roles y Permisos de Empleados

**Estado Actual:** El modelo `Usuario` tiene un campo `rol`, pero no se utiliza para controlar el acceso en la aplicación.

**Tareas Pendientes:**
- [ ] **Backend:**
    - [ ] Implementar un sistema de permisos basado en roles. Se puede usar un decorador de FastAPI para proteger los endpoints.
    - [ ] Modificar los endpoints existentes para que verifiquen el rol del usuario (ej. solo un `MANAGER` o `ADMIN` puede eliminar productos).
    - [ ] Crear endpoints para que un `MANAGER` o `ADMIN` pueda asignar roles a otros usuarios.
- [ ] **Frontend:**
    - [ ] Crear una pantalla de gestión de usuarios/empleados (`EmployeeManagementScreen.js`).
    - [ ] En la interfaz, mostrar u ocultar botones y acciones según el rol del usuario.
    - [ ] Permitir que los administradores asignen roles a los usuarios desde la nueva pantalla.

## 3. Visualización de COGS y Márgenes de Ganancia

**Estado Actual:** El backend calcula el COGS y el margen de ganancia, pero esta información no se muestra en el frontend.

**Tareas Pendientes:**
- [ ] **Frontend:**
    - [ ] En la pantalla de `CreateProductScreen.js` y `EditProductScreen.js`, mostrar los campos de `cogs` y `precio_sugerido` (solo lectura) después de seleccionar los insumos.
    - [ ] Añadir una sección de "Análisis de Rentabilidad" en la `DashboardScreen.js` o en una nueva pantalla de reportes.
    - [ ] Mostrar el margen de ganancia de cada producto en la lista de productos.

## 4. Integración de Métodos de Pago

**Estado Actual:** La funcionalidad de métodos de pago está marcada como en progreso. La UI del POS tiene botones, pero la integración completa no está confirmada.

**Tareas Pendientes:**
- [ ] **Backend:**
    - [ ] Integrar con una pasarela de pagos real (ej. Mercado Pago) para procesar pagos con tarjeta.
    - [ ] Guardar el resultado de la transacción en la base de datos.
- [ ] **Frontend:**
    - [ ] Implementar el flujo de pago para tarjetas de crédito en el `POSScreen.js`.
    - [ ] Manejar las respuestas de la pasarela de pago (aprobado, rechazado).
    - [ ] Mostrar un resumen de la transacción al finalizar la venta.