# 🤖 Prompt Profesional para Migrar Firebase a Backend Real (FastAPI + PostgreSQL)

Este prompt está diseñado para ejecutarse dentro de una IA de programación como **Gemini Code Assist** o **Cursor**, con máxima precisión y contexto sobre la arquitectura del proyecto.

---

## ✨ Objetivo

Migrar completamente el código que utiliza Firebase (Firestore y Auth) hacia el backend real del proyecto, construido con FastAPI y PostgreSQL.

---

## 🧰 Stack actual

| Capa          | Tecnología                     |
| ------------- | ------------------------------ |
| Frontend      | React 18 + Vite + Tailwind     |
| Backend       | FastAPI + PostgreSQL + JWT     |
| Autenticación | JWT (guardado en localStorage) |

---

## 🚫 Firebase: qué eliminar

1. **Archivo:** `frontend/src/firebaseConfig.js`

   - Contiene `initializeApp`, `getFirestore`, `getAuth`.
   - ❌ Eliminar completamente.

2. **Archivo:** `frontend/src/screens/POSScreen.js`

   - Reemplazar toda llamada a Firestore (como `collection`, `addDoc`, etc.) por llamada al backend `recordSale()` o similar.

3. **Dependencia:**

   - Ejecutar:
     ```bash
     npm uninstall firebase
     ```

4. **Verificar que no quede ningún import de:**

   - `firebase/app`
   - `firebase/auth`
   - `firebase/firestore`

---

## 🚀 Reemplazo: conectarse al backend real

1. **Autenticación:**

   - Usar `authApi.js` para login/register.
   - El token JWT se guarda en `localStorage` y se inyecta automáticamente desde `axios.js`.

2. **POS y ventas:**

   - Reemplazar funciones Firebase por llamadas a la API como:
     ```javascript
     import { recordSale } from '../api/ventaApi';

     const response = await recordSale(saleData);
     ```

3. **Contextos:**

   - Asegurarse que `AuthContext` use `authApi.js` y no Firebase.
   - Confirmar que `CartContext` y `POSContext` no usen persistencia Firebase.

---

## 🔧 Referencias internas disponibles

- `frontend/src/api/authApi.js`
- `frontend/src/api/ventaApi.js`
- `frontend/src/context/AuthContext.js`
- `backend/app/routers/auth_router.py`
- `backend/app/routers/venta_router.py`
- `.env` contiene `DATABASE_URL` y `SECRET_KEY`
- `DOCUMENTACION_TECNICA.md`: descripción completa de arquitectura

---

## ✅ Validación

1. La app debe iniciar sin errores tras eliminar Firebase.
2. El login/register debe seguir funcionando (vía backend).
3. Las ventas desde el POS deben guardarse en PostgreSQL.
4. Las rutas del backend deben ser protegidas correctamente con JWT.
5. No debe quedar ningún `import firebase` en el proyecto.

---

## 🌐 Endpoint de ejemplo (venta):

```python
@router.post("/ventas/record")
def record_sale(sale_data: VentaSchema, current_user: User = Depends(get_current_user)):
    ...
```

Y en el frontend:

```javascript
const token = localStorage.getItem('token');
await fetch('/ventas/record', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  },
  body: JSON.stringify(saleData)
});
```

---

## 📦 Resultado esperado

Una vez ejecutado este prompt correctamente:

- Firebase quedará eliminado del código.
- Toda la funcionalidad se conectará al backend real.
- El proyecto será desplegable sin dependencias externas.

---

**Recuerda:** si alguna pantalla (como el POS) no tiene implementado `recordSale`, deberás adaptarla usando `ventaApi.js` u otro archivo de API REST.

---

Listo para ejecutar este prompt con una IA de desarrollo como Gemini, Cursor o Claude. ✅

