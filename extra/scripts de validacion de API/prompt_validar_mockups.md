# 🤖 Prompt para Validar Uso de Mockups en el Frontend (Detección de Datos Simulados)

Este prompt está diseñado para ser ejecutado en una IA como **Gemini Code Assist**, **Cursor** o **Copilot Chat**, y tiene como objetivo auditar el frontend del proyecto para detectar cualquier dependencia activa a datos simulados (mockups), archivos temporales o estructuras hardcodeadas que deben reemplazarse por conexiones al backend real.

---

## ✨ Objetivo

Detectar todas las instancias donde el frontend utiliza datos mockeados y sugerir reemplazos automáticos por las funciones API disponibles.

---

## 🤍 Qué buscar

1. Importaciones de:

   - `mockBusinesses`, `mockProducts`, `mockSales`
   - `mockData.js`, `data.js`, `testData.js`

2. Variables declaradas como arrays de objetos simulados:

   ```js
   const businesses = [
     { id: 1, name: "Panadería" },
     ...
   ];
   ```

3. `useEffect` que no contiene llamada a `fetch`, `axios` o `api/*.js`

4. Renders condicionales basados en arrays simulados (`if (mockBusinesses.length)`)

5. Archivos donde se encuentre alguna de las siguientes palabras clave:

   - `mock`, `fake`, `demo`, `static`, `placeholder`, `simulate`

---

## 🔍 Rutas de escaneo prioritario

- `frontend/src/screens/**/*.js`
- `frontend/src/components/**/*.js`
- `frontend/src/data/`

---

## 🚀 Acciones automáticas sugeridas

Por cada hallazgo:

1. **Proponer un reemplazo** usando funciones de los archivos API existentes:

   - `businessApi.js`
   - `productApi.js`
   - `ventaApi.js`
   - `insumoApi.js`

2. **Insertar fetch real** dentro de `useEffect` si no existe:

   ```js
   useEffect(() => {
     const load = async () => {
       const data = await productApi.getMyProducts();
       setProducts(data);
     };
     load();
   }, []);
   ```

3. **Agregar comentarios de refactor** en línea:

   ```js
   // TODO: reemplazar mock con llamada real a productApi.getMyProducts()
   ```

---

## ✅ Validación exitosa

- Todos los componentes consumen datos desde `api/*.js`.
- No existen importaciones de `mockData` en ningún archivo JS.
- Todos los `useEffect` que cargan datos tienen una llamada a backend.
- No hay arrays de objetos simulados dentro del JSX.

---

## 🚧 Prohibiciones

- ❌ No dejar ningún array de datos estáticos.
- ❌ No ocultar el uso de mockups con renombres como `initialData`, `defaultItems`, etc.
- ❌ No reintroducir datos temporales tras el reemplazo.

---

Este prompt puede ejecutarse de forma iterativa hasta eliminar por completo el uso de datos simulados en el frontend. ✅

