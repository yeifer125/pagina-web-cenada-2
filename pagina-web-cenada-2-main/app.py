from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_URL = "https://apiparagit-3yxs.onrender.com/precios"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/precios")
def api_precios():
    try:
        r = requests.get(API_URL, timeout=15)
        r.raise_for_status()
        data = r.json()

        # Metadatos (primer objeto)
        metadata = data[0] if data else {}

        # Productos reales
        productos = [item for item in data if "producto" in item]

        return jsonify({
            "metadata": metadata,
            "productos": productos
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

