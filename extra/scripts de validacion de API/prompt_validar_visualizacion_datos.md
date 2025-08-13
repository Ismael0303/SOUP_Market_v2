# 🤖 Prompt para Validar Visualización de Datos en Pantallas del Sistema ERP

Este prompt está diseñado para ejecutarse en una IA como **Gemini Code Assist**, **Cursor** o **Copilot Chat**, con el objetivo de verificar que todos los datos generados por el usuario (productos, negocios, ventas, insumos) se reflejen correctamente en las interfaces visuales del frontend.

---

## ✨ Objetivo

Verificar que todos los datos creados o modificados mediante formularios y acciones del sistema se muestren correctamente en las pantallas correspondientes, garantizando consistencia entre base de datos y visualización.

---

## 🔍 Validaciones clave

1. **Productos creados:**
   - Crear un producto desde `ProductosScreen` y verificar que aparece inmediatamente en la lista sin recargar manualmente.

2. **Negocios del usuario:**
   - Crear un negocio desde `DashboardScreen` y confirmar que se ve reflejado en `MarketplaceScreen` y/o `DashboardScreen`.

3. **Ventas registradas:**
   - Realizar una venta desde `POSScreen` y confirmar que aparece en `VentasScreen`.

4. **Insumos gestionados:**
   - Agregar un insumo y verificar que aparece correctamente listado.

5. **Feedback visual:**
   - Cada acción exitosa debe mostrar un mensaje de éxito (`toast`, alerta o notificación en pantalla).
   - Cada error debe tener un mensaje visible al usuario.

6. **Recarga automática:**
   - Evitar tener que recargar la página para ver los cambios reflejados (usar `useEffect`, `useState`, re-fetch o `react-query`).

---

## 🧪 Métodos sugeridos

- Simular cada acción como usuario final (crear negocio, producto, venta, insumo).
- Revisar el DOM con DevTools para asegurar que los datos renderizados coinciden con los datos del backend (ver JSON de respuesta si es necesario).
- Usar el panel de red (F12 > Network) para confirmar que la petición y la respuesta fueron correctas.

---

## ✅ Validación exitosa

- Los elementos creados son visibles inmediatamente en la UI.
- El frontend se actualiza automáticamente sin `window.location.reload()`.
- Los datos mostrados en pantalla reflejan exactamente los valores del backend (sin datos faltantes, nulos o desactualizados).
- Se usan las funciones `api/*.js` para obtener los datos (nunca mockups).

---

## 🚫 Prohibiciones

- ❌ No depender de recargar la página para actualizar la UI.
- ❌ No dejar datos en estado temporal (`const negocio = {}`) sin persistencia real.
- ❌ No ocultar errores de red o de validación al usuario.

---

Este prompt permite verificar que tu sistema ERP no solo funcione a nivel backend, sino que también tenga una experiencia de usuario clara, coherente y sincronizada con los datos reales. ✅

