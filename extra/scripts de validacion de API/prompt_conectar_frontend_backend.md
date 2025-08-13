# 🤖 Prompt Profesional para Conectar el Frontend con el Backend Real (FastAPI + PostgreSQL)

Este prompt está diseñado para ser ejecutado en una IA de programación como **Gemini Code Assist** o **Cursor**, y tiene como objetivo eliminar el uso de datos mockeados en el frontend y conectar todas las pantallas con los endpoints reales del backend.

---

## ✨ Objetivo

Eliminar el uso de datos simulados (mockups) en el frontend y asegurar que todas las operaciones CRUD estén conectadas al backend real, implementado en FastAPI con PostgreSQL.

---

## 🧰 Stack actual

| Capa          | Tecnología                     |
| ------------- | ------------------------------ |
| Frontend      | React 18 + Vite + Tailwind     |
| Backend       | FastAPI + PostgreSQL + JWT     |
| Autenticación | JWT (guardado en localStorage) |

---

## 🔍 Problemas identificados

- En `frontend/src/screens/MarketplaceScreen.js`, los negocios del marketplace están mockeados y no provienen del backend.
- En `DashboardScreen.js`, los negocios creados no se almacenan correctamente en la base de datos ni se reflejan luego.
- Otras pantallas como `VentasScreen`, `ProductosScreen`, `InsumosScreen`, etc., también usan mockups o `data.js` en lugar de APIs reales.

---

## 🚀 Reemplazo por APIs reales

Para cada pantalla, deberás:

1. **Eliminar** las importaciones de `mockBusinesses`, `mockProducts`, `mockSales`, etc.
2. **Reemplazar** las llamadas a datos estáticos por llamadas a los siguientes endpoints:

---

### 🏢 Negocios (Businesses)

**Endpoint:** `GET /businesses/me`

- Usar en Marketplace y Dashboard.

**Endpoint:** `POST /businesses/`

- Para crear negocios desde el dashboard.

**Frontend API:** `frontend/src/api/businessApi.js`

```js
const businesses = await businessApi.getMyBusinesses();
await businessApi.createBusiness(formData);
```

---

### 🌝 Productos

**Endpoint:** `GET /products/me` **Endpoint:** `POST /products/`

**Frontend API:** `frontend/src/api/productApi.js`

```js
const products = await productApi.getMyProducts();
await productApi.createProduct(formData);
```

---

### 💪 Ventas

**Endpoint:** `GET /ventas/me` **Endpoint:** `POST /ventas/record`

**Frontend API:** `frontend/src/api/ventaApi.js`

```js
const ventas = await ventaApi.getMyVentas();
await ventaApi.recordSale(saleData);
```

---

### 📊 Insumos

**Endpoint:** `GET /insumos/me` **Endpoint:** `POST /insumos/`

**Frontend API:** `frontend/src/api/insumoApi.js`

---

## 🌎 Reglas de implementación

1. No deben quedar datos hardcodeados ni archivos `mockData.js` activos.
2. Todos los `useEffect` deben hacer fetch desde la API correspondiente.
3. Las funciones `handleCreate`, `handleDelete`, `handleUpdate` deben interactuar con `api/*.js`.
4. Las respuestas de la API deben ser usadas para actualizar el estado local (`useState`).

---

## ✅ Validación final

- El dashboard muestra negocios reales del usuario.
- El marketplace muestra negocios obtenidos desde el backend.
- Crear un producto o negocio refleja el cambio sin recargar la página.
- No hay errores de red por endpoints inexistentes.
- El `console.log` no debe mostrar datos mockeados.

---

## 🚧 Prohibiciones

- ❌ No usar `mockBusinesses`, `mockProducts`, ni ningún archivo `mockData.js`.
- ❌ No escribir datos en localStorage directamente (usar `AuthContext` para el token).
- ❌ No llamar a la API directamente desde el componente (usar `api/*.js`).

---

Listo para ser ejecutado en Gemini o Cursor para automatizar la reconexión del frontend al backend real. ✅

