import requests

API_URL = "https://apiparagit-3yxs.onrender.com/precios"

def obtener_precios():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    return r.json()
