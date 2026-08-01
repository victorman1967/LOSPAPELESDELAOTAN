"""
Extrae texto e imágenes de un archivo PDF usando PyMuPDF (fitz).
"""
import fitz  # PyMuPDF
import io


def extraer_de_pdf(archivo_bytes: bytes, nombre_archivo: str) -> dict:
    """
    Recibe los bytes de un PDF y devuelve un diccionario normalizado con:
    titulo, texto, imagenes (lista de bytes de imagen), fuente, tipo_origen
    """
    try:
        doc = fitz.open(stream=archivo_bytes, filetype="pdf")
    except Exception as e:
        return {
            "titulo": nombre_archivo,
            "texto": "",
            "imagenes": [],
            "fuente": nombre_archivo,
            "tipo_origen": "pdf",
            "error": str(e),
        }

    texto_completo = []
    imagenes = []

    # Título: metadatos del PDF si existen, si no el nombre de archivo
    titulo = doc.metadata.get("title") if doc.metadata else None
    if not titulo:
        titulo = nombre_archivo

    for pagina in doc:
        texto_completo.append(pagina.get_text())

        for img_info in pagina.get_images(full=True):
            xref = img_info[0]
            try:
                base_img = doc.extract_image(xref)
                imagenes.append(base_img["image"])  # bytes de la imagen
            except Exception:
                continue

    doc.close()

    return {
        "titulo": titulo,
        "texto": "\n".join(texto_completo).strip(),
        "imagenes": imagenes,
        "fuente": nombre_archivo,
        "tipo_origen": "pdf",
        "error": None,
    }
