# 🤖 Prompt para Validar Conexiones Activas del Frontend con el Backend (FastAPI + PostgreSQL)

Este prompt está diseñado para ser ejecutado en una IA como **Gemini Code Assist**, **Cursor** o **Copilot Chat**, y tiene como objetivo auditar el frontend para verificar que todas las operaciones realicen llamadas exitosas al backend real y no fallen silenciosamente.

---

## ✨ Objetivo

Asegurar que cada función, pantalla o componente del frontend esté correctamente conectado al backend:

- Las rutas existen
- Las respuestas son válidas
- El token se está enviando
- No hay errores silenciosos en consola o red

---

## 🤍 Validaciones a realizar

1. **Verificar que cada **``** o evento **``** relevante llame a alguna función de:**

   - `api/*.js` (ej: `productApi`, `businessApi`, `ventaApi`, etc.)

2. **Confirmar que los **``** o **``** devuelven respuestas válidas (status 200 o 201).**

3. **Verificar que cada llamada a endpoints privados incluya el header:**

   ```js
   Authorization: Bearer <token>
   ```

   Obtenido desde `localStorage.getItem("token")`

4. **Simular respuestas fallidas:**

   - Eliminar temporalmente el token y verificar que el backend responde con 401.
   - Simular error 404 para rutas inexistentes y verificar mensajes adecuados.

5. **Comprobar logs de consola y red:**

   - Usar DevTools (F12) > pestaña "Network" y "Console"
   - Verificar que no haya errores como:
     - `ERR_CONNECTION_REFUSED`
     - `Failed to fetch`
     - `Unexpected token < in JSON`
     - `401 Unauthorized`

6. **Asegurar consistencia visual:**

   - Que los datos mostrados en pantalla coincidan con los datos reales del backend.

---

## 🌐 Pantallas prioritarias para validar

- `DashboardScreen`
- `MarketplaceScreen`
- `POSScreen`
- `VentasScreen`
- `ProductosScreen`
- `InsumosScreen`

---

## ✅ Validación exitosa

- Todas las funciones del sistema están conectadas a `api/*.js`
- Las respuestas del backend se usan para actualizar el estado (`useState`)
- El token JWT se envía correctamente
- No hay errores visibles en consola ni en el inspector de red
- Los datos en pantalla reflejan lo guardado en la base de datos

---

## 🚧 Prohibiciones

- ❌ No dejar `try/catch` vacíos
- ❌ No ocultar errores de red
- ❌ No hacer fetch sin `await`
- ❌ No llamar directamente al endpoint en el componente (usar `api/*.js`)

---

Este prompt garantiza que el frontend funcione de forma conectada, validada y robusta con el backend en FastAPI. ✅

