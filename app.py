import json
import subprocess

from flask import Flask, Response, request, render_template_string, redirect, url_for, render_template
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import os
from classes.freebox import Freebox


g = Gauge(
    "Temperature",
    "Temperature of the raspberry pi",
)

app = Flask(__name__, template_folder="templates")



#################################- ROUTES -#################################


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
FORM_TEMPLATE = os.path.join(os.path.dirname(__file__), "templates", "form.html")

with open(FORM_TEMPLATE, "r") as f:
    FORM_HTML = f.read()

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "build":
            freebox = Freebox(
                mode="create",
                app_id=request.form.get("app_id"),
                app_name=request.form.get("app_name"),
                app_version=request.form.get("app_version"),
                device_name=request.form.get("device_name"),
            )

        elif action == "token":
            freebox = Freebox(
                mode="token",
                app_token=request.form.get("app_token")
            )
        else:
            return "Action non reconnue", 400

        freebox.save_config()

        return redirect(url_for("index"))

    return render_template("form.html", data=data)


@app.route("/show")
def show_config():
    freebox = Freebox()
    freebox.load_config()

    return freebox.__dict__


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
