"""
Detecta y elimina duplicados entre los elementos extraídos.

Dos niveles:
1. Duplicado exacto: mismo hash del texto normalizado.
2. Duplicado aproximado: similitud de texto por encima de un umbral (difflib).
"""
import hashlib
import difflib


def _normalizar(texto: str) -> str:
    return " ".join(texto.lower().split())


def _hash_texto(texto: str) -> str:
    return hashlib.sha256(_normalizar(texto).encode("utf-8")).hexdigest()


def eliminar_duplicados(items: list, umbral_similitud: float = 0.85) -> list:
    """
    Recibe una lista de diccionarios (cada uno con clave 'texto') y devuelve
    la lista sin duplicados exactos ni casi-duplicados.
    """
    vistos_hash = set()
    resultado = []

    for item in items:
        texto = item.get("texto", "") or ""
        if not texto.strip():
            # Sin texto (ej. error de extracción): se mantiene, no se puede comparar
            resultado.append(item)
            continue

        h = _hash_texto(texto)

        # 1) Duplicado exacto
        if h in vistos_hash:
            continue

        # 2) Duplicado aproximado: comparar contra los ya aceptados
        es_similar = False
        for existente in resultado:
            texto_existente = existente.get("texto", "") or ""
            if not texto_existente.strip():
                continue
            ratio = difflib.SequenceMatcher(
                None, _normalizar(texto)[:3000], _normalizar(texto_existente)[:3000]
            ).ratio()
            if ratio >= umbral_similitud:
                es_similar = True
                break

        if es_similar:
            continue

        vistos_hash.add(h)
        resultado.append(item)

    return resultado
