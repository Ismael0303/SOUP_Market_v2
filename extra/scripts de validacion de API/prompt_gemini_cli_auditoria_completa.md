# 🤖 Prompt Unificado para Gemini CLI — Auditoría Completa del Proyecto SOUP Market

Este prompt está diseñado para ser ejecutado mediante **Gemini CLI** para aplicar una auditoría automatizada sobre el proyecto **SOUP Market**. Incluye migración de Firebase, eliminación de mockups, conexión de frontend con backend, y verificación de errores.

---

## 🧠 Prompt para Gemini CLI

```bash
Please audit the entire codebase of this React + FastAPI project.

# 🔄 1. Remove Firebase usage
- Delete firebaseConfig.js and all imports from "firebase/*".
- Uninstall Firebase from package.json if used.
- Remove Firestore or Auth logic from POSScreen.js or other screens.

# 📦 2. Detect and remove mock data
- Search and remove all usages of mockBusinesses, mockProducts, mockSales, or mockData.js.
- Refactor those components to use real API calls from api/*.js (e.g. productApi.js, businessApi.js).

# 🔗 3. Reconnect frontend with backend
- Ensure that each CRUD screen (DashboardScreen, CreateProductScreen, POSScreen, etc.) uses the API modules under src/api/.
- Replace hardcoded useEffect logic with actual async functions using await and API calls.
- Validate that Authorization headers send the JWT token from localStorage.

# 🧪 4. Test data persistence
- Confirm that all created businesses, products, and sales are visible after submission.
- Ensure that the user never has to reload the page to see updated data.

# 🚨 5. Detect broken flows
- Find any onClick, onSubmit or handle* functions that are declared but do nothing.
- Check if any button or action doesn’t trigger a visual or state update.

# 🧯 6. Remove silent failures
- Review useEffect and fetch calls: they must include try/catch and handle errors.
- No fetch/axios call should fail silently — display feedback.

# ✅ 7. Final validation
- All data shown on screen comes from the backend.
- All API routes used actually exist.
- All user actions produce a visible and persistent effect.
- All inputs have basic validation.

Please output all changes as a patch or file diff summary so they can be reviewed before committing.
```

---

## 📌 Instrucciones de uso

1. Abrí una terminal en la raíz del proyecto.
2. Ejecutá Gemini CLI con el prompt anterior (usando flag `--prompt` o pegándolo si estás en modo interactivo).
3. Revisá las sugerencias y diffs antes de aplicar cambios.
4. Comprobá en el navegador que los datos se muestran, se actualizan y se almacenan correctamente.

---

Este prompt sirve como checklist ejecutable en lote, ideal para mantener la consistencia general del sistema. ✅

