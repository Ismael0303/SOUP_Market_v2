# ✅ Guía Integral de Auditoría del Sistema ERP SOUP Market

Esta guía reúne todos los prompts diseñados para asistencias de IA como Gemini Code Assist, Cursor o Copilot, con el fin de validar que la aplicación SOUP Market esté completamente conectada, funcional y libre de datos simulados o errores silenciosos.

---

## 🧩 Índice de Prompts

### 1. 🔄 Prompt de Migración Firebase → Backend Real
**Nombre en Canva:** `Prompt Migracion Firebase`
- Elimina Firebase del proyecto.
- Reemplaza sus funciones por endpoints reales.
- Limpia dependencias obsoletas.

### 2. 🔗 Prompt para Conectar el Frontend con el Backend
**Nombre en Canva:** `Prompt Conectar Frontend Backend`
- Reemplaza todos los mockups y datos simulados.
- Usa los archivos `api/*.js` para operaciones CRUD.
- Asegura que la interfaz refleje cambios reales.

### 3. 🔎 Prompt para Validar Uso de Mockups
**Nombre en Canva:** `Prompt Validar Mockups`
- Detecta archivos, imports y funciones que usan datos estáticos.
- Sugiere reemplazos con llamadas a la API.
- Evita estructuras engañosas o arrays internos hardcodeados.

### 4. 📡 Prompt para Validar Conexiones Backend
**Nombre en Canva:** `Prompt Validar Conexion Backend`
- Asegura que todas las funciones llamen a la API.
- Verifica envío de token JWT y respuesta correcta del servidor.
- Controla errores de red y validaciones faltantes.

### 5. 👁️ Prompt para Validar Visualización de Datos
**Nombre en Canva:** `Prompt Validar Visualización Datos`
- Verifica que los elementos creados se vean en pantalla.
- Asegura que no se requiera recargar manualmente.
- Confirma consistencia entre backend y lo que se ve en UI.

### 6. 🛠️ Prompt para Validar Funciones Rotas o Flujos Incompletos
**Nombre en Canva:** `Prompt Validar Errores Funciones Rotas`
- Detecta botones sin acción, funciones desconectadas.
- Verifica que los formularios tengan efecto real.
- Audita formularios sin validaciones y acciones sin feedback.

---

## ✅ Cómo Usarlos

1. Abrí tu proyecto con Gemini Code Assist, Cursor o entorno similar.
2. Pegá cada uno de los prompts individualmente en el chat del asistente.
3. Ejecutá y seguí las recomendaciones en cada sección del código.
4. Repetí el ciclo hasta que:
   - No existan mockups activos
   - Todos los flujos estén conectados
   - Los datos visibles coincidan con el backend

---

## 🎯 Resultado esperado

Al completar todos los prompts:
- La app será totalmente funcional, sin dependencias innecesarias.
- Cada acción (crear, modificar, listar, eliminar) tendrá impacto real.
- Toda la UI estará sincronizada con la base de datos PostgreSQL.
- El backend responderá con autenticación JWT y manejo de errores.

---

Esta guía puede reutilizarse tras cada gran migración, iteración o integración en el sistema. ✅

