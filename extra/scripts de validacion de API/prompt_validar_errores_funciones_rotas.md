# 🤖 Prompt para Validar Errores, Funcionalidades Rotas y Flujos Incompletos en el Sistema ERP

Este prompt está diseñado para ejecutarse en una IA como **Gemini Code Assist**, **Cursor** o **Copilot Chat**, y su propósito es detectar acciones que no producen efectos reales, botones que no hacen nada, rutas sin conexión o funcionalidades visibles pero incompletas en el sistema.

---

## ✨ Objetivo

Identificar y reportar:
- Funciones que están declaradas pero no conectadas
- Botones o acciones sin efecto visible
- Flujos de usuario incompletos (crear sin mostrar, eliminar sin actualizar UI)
- Pantallas que muestran datos irreales o no vinculados

---

## 🔍 Validaciones a realizar

1. **Botones sin funcionalidad:**
   - Identificar cualquier botón con `onClick` vacío o con funciones que no alteran el estado ni hacen fetch.

2. **Funciones sin impacto real:**
   - Revisar funciones como `handleCreate`, `handleDelete`, `handleUpdate`.
   - Verificar si están conectadas a `api/*.js` y producen cambios reales en la UI y backend.

3. **Flujos incompletos:**
   - Crear un negocio → ¿se muestra luego?
   - Registrar venta → ¿aparece en la lista?
   - Agregar producto → ¿se refleja automáticamente?

4. **Endpoints faltantes o no conectados:**
   - Funciones que intentan hacer fetch a rutas inexistentes.
   - Componentes que deberían mostrar datos, pero están vacíos o con `[]` por defecto.

5. **Mensajes de error ausentes:**
   - Verificar que errores de red o validación muestren feedback visible al usuario.

6. **Validaciones faltantes en formularios:**
   - ¿Se puede enviar un formulario vacío?
   - ¿Se puede enviar un dato inválido (precio negativo, nombre vacío, etc.)?

---

## 📌 Pantallas prioritarias

- `DashboardScreen`
- `POSScreen`
- `MarketplaceScreen`
- `VentasScreen`
- `CreateProductScreen`
- `LoginScreen`

---

## ✅ Validación exitosa

- Todos los botones tienen un efecto observable (visual o funcional)
- No hay funciones vacías o desconectadas
- Cada acción produce un cambio en el backend y en la UI
- Los formularios tienen validación básica activa
- Se muestran mensajes de éxito o error para cada acción

---

## 🚫 Prohibiciones

- ❌ No permitir acciones sin feedback
- ❌ No dejar formularios con `onSubmit={e => e.preventDefault()}` sin lógica real
- ❌ No ocultar fallas de conexión sin informar al usuario

---

Este prompt ayuda a cerrar brechas entre diseño y funcionalidad, asegurando que todo lo visible en la app esté correctamente implementado y conectado. ✅

