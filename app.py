import subprocess

from flask import Flask, Response, request
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import os

g = Gauge(
    "Temperature",
    "Temperature of the raspberry pi",
)

app = Flask(__name__)


@app.route("/machine-temperature")
def temperature():
    try:
        raw = subprocess.check_output(
            ["cat", "/sys/class/thermal/thermal_zone0/temp"], text=True
        ).strip()
        temp = float(raw) / 1000.0

        g.set(temp)

        return Response(str(temp), mimetype=CONTENT_TYPE_LATEST)

    except Exception as e:
        return Response(f"Erreur : {e}", status=500, mimetype="text/plain")





@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
