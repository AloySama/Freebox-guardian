import json
import subprocess

from flask import Flask, Response, request, render_template_string
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


#################################- FORM ABOUT FREEBOX APP -#################################


CONFIG_FILE = "freebox_config.json"
FORM_TEMPLATE = "./template/form.html"

with open(FORM_TEMPLATE) as f:
    FORM_HTML = f.read()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        data = ""

        if action == "Créer App":
            data = {
                "mode": "create",
                "app_id": request.form["app_id"],
                "app_name": request.form["app_name"],
                "app_version": request.form["app_version"],
                "device_name": request.form["device_name"],
                "use_token": False
            }

        elif action == "Utiliser Token":
            data = {
                "mode": "token",
                "app_token": request.form["app_token"],
                "use_token": True
            }

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

        return f"Saved config: {data}"

    return render_template_string(FORM_HTML)


@app.route("/show")
def show_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data
    return "No config found."


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
