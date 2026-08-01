"""
Geocodifica direcciones/lugares de texto libre y construye un mapa folium
con un marcador por cada elemento que tenga ubicación.
"""
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium

_geolocator = Nominatim(user_agent="agregador_fuentes_app")
_geocode = RateLimiter(_geolocator.geocode, min_delay_seconds=1)


def geocodificar(direccion: str):
    """Devuelve (lat, lon) o None si no se encuentra la dirección."""
    if not direccion or not direccion.strip():
        return None
    try:
        ubicacion = _geocode(direccion)
        if ubicacion:
            return (ubicacion.latitude, ubicacion.longitude)
    except Exception:
        pass
    return None


def construir_mapa(items_con_ubicacion: list):
    """
    items_con_ubicacion: lista de dicts con claves 'titulo', 'lat', 'lon', 'fuente'
    Devuelve un objeto folium.Map listo para mostrar en Streamlit.
    """
    if not items_con_ubicacion:
        # Mapa centrado en el mundo por defecto
        return folium.Map(location=[20, 0], zoom_start=2)

    lat_media = sum(i["lat"] for i in items_con_ubicacion) / len(items_con_ubicacion)
    lon_media = sum(i["lon"] for i in items_con_ubicacion) / len(items_con_ubicacion)

    mapa = folium.Map(location=[lat_media, lon_media], zoom_start=4)

    for item in items_con_ubicacion:
        popup_html = f"<b>{item['titulo']}</b><br>Fuente: {item['fuente']}"
        folium.Marker(
            location=[item["lat"], item["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=item["titulo"],
        ).add_to(mapa)

    return mapa
