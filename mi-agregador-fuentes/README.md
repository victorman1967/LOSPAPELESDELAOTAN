# Agregador de Fuentes

Aplicación web (Streamlit) que agrega contenido de URLs, PDFs y documentos Word,
elimina duplicados y muestra texto, imágenes y ubicaciones en un mapa.

## 🚀 Cómo publicarlo (paso a paso)

### 1. Crear cuenta en GitHub (si no tienes)
Ve a https://github.com y regístrate gratis.

### 2. Crear un repositorio nuevo
- Pulsa "New repository".
- Nómbralo, por ejemplo, `agregador-fuentes`.
- Ponlo como **público**.
- No añadas README (ya tienes uno).

### 3. Subir estos archivos a tu repositorio
Puedes hacerlo de dos formas:

**Opción fácil (sin terminal):**
En la página de tu repositorio, pulsa "Add file" → "Upload files" y arrastra
todos los archivos y carpetas de este proyecto (manteniendo la estructura de
carpetas `extractors/` y `utils/`).

**Opción con terminal (si tienes git instalado):**
```bash
cd mi-agregador-fuentes
git init
git add .
git commit -m "Primera versión del agregador de fuentes"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/agregador-fuentes.git
git push -u origin main
```

### 4. Desplegar en Streamlit Community Cloud (gratis)
1. Ve a https://share.streamlit.io
2. Inicia sesión con tu cuenta de GitHub.
3. Pulsa "New app".
4. Selecciona tu repositorio `agregador-fuentes`, la rama `main` y el archivo
   principal `app.py`.
5. Pulsa "Deploy".

En un par de minutos tendrás un enlace público tipo:
`https://TU-APP.streamlit.app`

Ese enlace es de **acceso libre**: cualquiera que lo tenga puede usar la app.

### 5. Actualizar la app en el futuro
Cada vez que subas cambios nuevos a tu repositorio de GitHub, Streamlit Cloud
redepliega la app automáticamente — no tienes que hacer nada más.

## 📁 Estructura del proyecto
```
mi-agregador-fuentes/
├── app.py                     ← app principal de Streamlit
├── requirements.txt           ← librerías necesarias
├── extractors/
│   ├── url_extractor.py       ← extrae texto/imágenes de páginas web
│   ├── pdf_extractor.py       ← extrae texto/imágenes de PDFs
│   └── word_extractor.py      ← extrae texto/imágenes de Word
└── utils/
    ├── dedup.py                ← elimina duplicados (exactos y casi-iguales)
    └── map_utils.py             ← geocodificación y mapa interactivo
```

## 🧪 Cómo probarlo en tu propio ordenador (opcional, antes de publicar)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

## 🔧 Posibles mejoras futuras
- Guardar los elementos en una base de datos (SQLite) para que no se pierdan
  al cerrar la app.
- Detección automática de ubicaciones en el texto (en vez de añadirlas a mano).
- Comparación de duplicados por significado (embeddings) en vez de solo texto.
- Filtros y búsqueda dentro del feed.
