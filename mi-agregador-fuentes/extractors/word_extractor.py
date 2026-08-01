"""
Extrae texto e imágenes de un archivo Word (.docx) usando python-docx.
"""
from docx import Document
import io


def extraer_de_word(archivo_bytes: bytes, nombre_archivo: str) -> dict:
    """
    Recibe los bytes de un .docx y devuelve un diccionario normalizado con:
    titulo, texto, imagenes (lista de bytes de imagen), fuente, tipo_origen
    """
    try:
        doc = Document(io.BytesIO(archivo_bytes))
    except Exception as e:
        return {
            "titulo": nombre_archivo,
            "texto": "",
            "imagenes": [],
            "fuente": nombre_archivo,
            "tipo_origen": "word",
            "error": str(e),
        }

    # Texto: todos los párrafos
    parrafos = [p.text for p in doc.paragraphs if p.text.strip()]
    texto = "\n".join(parrafos)

    # Título: primer párrafo no vacío, o el nombre de archivo
    titulo = parrafos[0] if parrafos else nombre_archivo

    # Imágenes: están embebidas como "media" dentro del paquete .docx
    imagenes = []
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            try:
                imagenes.append(rel.target_part.blob)
            except Exception:
                continue

    return {
        "titulo": titulo[:200],
        "texto": texto,
        "imagenes": imagenes,
        "fuente": nombre_archivo,
        "tipo_origen": "word",
        "error": None,
    }
