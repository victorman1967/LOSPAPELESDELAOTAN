"""
Agregador de Fuentes
---------------------
Aplicación Streamlit que permite subir URLs, PDFs y documentos Word,
extraer su contenido (texto + imágenes), eliminar duplicados y mostrar
todo en un feed único, incluyendo un mapa si hay ubicaciones asociadas.
"""
import streamlit as st
from streamlit_folium import st_folium

from extractors.url_extractor import extraer_de_url
from extractors.pdf_extractor import extraer_de_pdf
from extractors.word_extractor import extraer_de_word
from utils.dedup import eliminar_duplicados
from utils.map_utils import geocodificar, construir_mapa

st.set_page_config(page_title="Agregador de Fuentes", layout="wide")

# --- Estado persistente durante la sesión ---
if "items" not in st.session_state:
    st.session_state.items = []

st.title("📚 Agregador de Fuentes")
st.caption("Sube URLs, PDFs y documentos Word. La app extrae el contenido, "
           "elimina duplicados y lo muestra todo en un solo lugar.")

# --- Panel lateral: entradas ---
with st.sidebar:
    st.header("Añadir fuentes")

    st.subheader("🔗 URLs")
    urls_texto = st.text_area(
        "Pega una o varias URLs (una por línea)", height=100,
        placeholder="https://ejemplo.com/articulo1\nhttps://ejemplo.com/articulo2"
    )

    st.subheader("📄 Archivos PDF")
    pdfs = st.file_uploader("Sube PDFs", type=["pdf"], accept_multiple_files=True)

    st.subheader("📝 Archivos Word")
    words = st.file_uploader("Sube documentos Word", type=["docx"], accept_multiple_files=True)

    umbral = st.slider(
        "Sensibilidad de deduplicación (más alto = más estricto)",
        min_value=0.5, max_value=0.99, value=0.85, step=0.01
    )

    procesar = st.button("Procesar fuentes", type="primary")

    if st.button("🗑️ Vaciar todo"):
        st.session_state.items = []
        st.rerun()

# --- Procesamiento ---
if procesar:
    nuevos_items = []

    # URLs
    if urls_texto.strip():
        lista_urls = [u.strip() for u in urls_texto.splitlines() if u.strip()]
        with st.spinner(f"Extrayendo {len(lista_urls)} URL(s)..."):
            for url in lista_urls:
                nuevos_items.append(extraer_de_url(url))

    # PDFs
    if pdfs:
        with st.spinner(f"Extrayendo {len(pdfs)} PDF(s)..."):
            for pdf in pdfs:
                nuevos_items.append(extraer_de_pdf(pdf.read(), pdf.name))

    # Word
    if words:
        with st.spinner(f"Extrayendo {len(words)} documento(s) Word..."):
            for w in words:
                nuevos_items.append(extraer_de_word(w.read(), w.name))

    st.session_state.items.extend(nuevos_items)
    st.session_state.items = eliminar_duplicados(st.session_state.items, umbral)
    st.success(f"Procesado. Total de elementos únicos: {len(st.session_state.items)}")

# --- Mostrar resultados ---
items = st.session_state.items

if not items:
    st.info("Añade fuentes desde el panel lateral y pulsa 'Procesar fuentes'.")
else:
    tab_feed, tab_mapa = st.tabs(["📰 Feed de contenido", "🗺️ Mapa"])

    with tab_feed:
        for i, item in enumerate(items):
            with st.container(border=True):
                st.subheader(item.get("titulo") or "(sin título)")
                st.caption(f"Origen: {item['tipo_origen'].upper()} · Fuente: {item['fuente']}")

                if item.get("error"):
                    st.warning(f"No se pudo extraer completamente: {item['error']}")

                texto = item.get("texto", "")
                if texto:
                    st.write(texto[:600] + ("..." if len(texto) > 600 else ""))
                    with st.expander("Ver texto completo"):
                        st.write(texto)

                imagenes = item.get("imagenes", [])
                if imagenes:
                    cols = st.columns(min(4, len(imagenes)))
                    for idx, img in enumerate(imagenes[:8]):
                        with cols[idx % len(cols)]:
                            try:
                                st.image(img, use_container_width=True)
                            except Exception:
                                pass

                # Ubicación opcional manual (para el mapa)
                with st.expander("📍 Añadir ubicación a este elemento"):
                    direccion = st.text_input(
                        "Dirección o lugar (ej: 'Madrid, España')",
                        key=f"direccion_{i}"
                    )
                    if st.button("Geocodificar", key=f"geocod_{i}"):
                        coords = geocodificar(direccion)
                        if coords:
                            item["lat"], item["lon"] = coords
                            st.success(f"Ubicación asignada: {coords}")
                        else:
                            st.error("No se encontró la ubicación.")

    with tab_mapa:
        items_con_ubicacion = [
            it for it in items if "lat" in it and "lon" in it
        ]
        if items_con_ubicacion:
            mapa = construir_mapa(items_con_ubicacion)
            st_folium(mapa, width=1000, height=600)
        else:
            st.info("Ningún elemento tiene ubicación asignada todavía. "
                    "Añádela desde el feed con 'Añadir ubicación a este elemento'.")
