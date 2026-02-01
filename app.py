from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_URLS = [
    "https://apiparagit-3yxs.onrender.com/precios",
    "https://apiparagit-otra.onrender.com/precios"
]

TIMEOUT = 10

@app.route("/")
def index():
    return render_template("index.html")


def obtener_datos_api():
    errores = []

    for url in API_URLS:
        try:
            r = requests.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json(), url
        except Exception as e:
            errores.append(f"{url} -> {str(e)}")

    raise Exception("Todas las APIs fallaron", errores)


@app.route("/api/precios")
def api_precios():
    try:
        data, api_usada = obtener_datos_api()

        metadata = data[0] if data else {}
        productos = [item for item in data if "producto" in item]

        return jsonify({
            "api_activa": api_usada,
            "metadata": metadata,
            "productos": productos
        })

    except Exception as e:
        return jsonify({
            "error": "No se pudo conectar a ninguna API",
            "detalle": str(e)
        }), 500


if __name__ == "__main__":
    app.run()
