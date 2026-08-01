"""
Extrae título, texto e imágenes de una página web a partir de su URL.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AgregadorFuentesBot/1.0)"
}


def extraer_de_url(url: str, timeout: int = 15) -> dict:
    """
    Descarga una URL y extrae un diccionario normalizado con:
    titulo, texto, imagenes (lista de URLs absolutas), fuente, tipo_origen
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        return {
            "titulo": url,
            "texto": "",
            "imagenes": [],
            "fuente": url,
            "tipo_origen": "url",
            "error": str(e),
        }

    soup = BeautifulSoup(resp.text, "lxml")

    # Título: og:title si existe, si no <title>
    titulo = None
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        titulo = og_title["content"].strip()
    elif soup.title and soup.title.string:
        titulo = soup.title.string.strip()
    else:
        titulo = url

    # Texto: concatenar párrafos <p> (heurística simple pero robusta)
    parrafos = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    texto = "\n".join([p for p in parrafos if len(p) > 40])  # filtra ruido corto

    # Imágenes: <img> con src absoluto
    imagenes = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            imagenes.append(urljoin(url, src))
    # og:image como imagen destacada si existe
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        imagenes.insert(0, urljoin(url, og_image["content"]))

    return {
        "titulo": titulo,
        "texto": texto,
        "imagenes": list(dict.fromkeys(imagenes)),  # quita duplicados manteniendo orden
        "fuente": url,
        "tipo_origen": "url",
        "error": None,
    }
