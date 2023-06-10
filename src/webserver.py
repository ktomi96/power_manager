#!/usr/bin/env python
import os
import sys
import requests
import glob
from datetime import date, timedelta, datetime

from flask import (
    Flask,
    redirect,
    request,
    url_for,
    render_template,
    jsonify,
)
import dotenv
import pandas as pd

from forms import AC_login_setup
from plotter import ac_plotter, solar_plotter, solar_produce_agr
from migrate_csv_to_sql import migrate_to_database
from ac_handler import ac_status_getter, ac_status_setter

env_path = "./env/"
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)

logs_dir = ["ac", "solar"]

logs_path = os.getenv("LOG_PATH")
db_path = os.getenv("DB_PATH")
db_url = f"{os.getenv('DB')}{db_path}"
debug = os.getenv("DEBUG") == "True"

app = Flask(
    __name__,
    static_folder="../src/frontend/build/",
    static_url_path="/",
)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


def is_config():
    return os.path.exists(env_file)


def is_database():
    if not os.path.exists(db_path):
        migrate_to_database(logs_path, db_url)
    return True


def init_dotenv():
    dotenv.load_dotenv(env_file)


def set_dotenv_ac(request):
    request_dict = request.form.to_dict()
    request_dict.pop("csrf_token")
    request_dict.pop("submit")

    for key, value in request_dict.items():
        dotenv.set_key(env_file, key, value)


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/ac", methods=["GET"])
def get_ac_plot():
    start_date = request.args.get("start_date", default=None, type=str)
    end_date = request.args.get("end_date", default=None, type=str)
    if ((start_date or end_date)) is None:
        return {"error": 404}

    ac_data = ac_plotter([start_date, end_date])
    return ac_data if ac_data is not None else jsonify(None)


@app.route("/solar", methods=["GET"])
def get_solar_plot():
    start_date = request.args.get("start_date", default=None, type=str)
    end_date = request.args.get("end_date", default=None, type=str)
    if ((start_date or end_date)) is None:
        return {"error": 404}

    solar_data = solar_plotter([start_date, end_date])
    return solar_data if solar_data is not None else jsonify(None)


@app.route("/solar_sum", methods=["GET"])
def get_solar_agr():
    start_date = request.args.get("start_date", default=None, type=str)
    end_date = request.args.get("end_date", default=None, type=str)
    if ((start_date or end_date)) is None:
        return {"error": 404}

    solar_data = int(solar_produce_agr([start_date, end_date]))
    print(f"solar_sum: {solar_data}")
    return jsonify(solar_data) if solar_data is not None else jsonify(None)


@app.route("/ac_status", methods=["GET"])
def ac_status():
    try:
        ac_status = ac_status_getter()
        return (
            jsonify(ac_status)
            if ac_status is not None
            else ({"error": "ac_status"}, 404)
        )
    except Exception as esc:
        print(esc, file=sys.stderr)


@app.route("/ac_set", methods=["POST"])
def ac_set():
    try:
        json_ac_settings = request.get_json()
        ac_settings = dict(json_ac_settings)

        state = ac_status_setter(ac_settings)
        if not state:
            response_data = {"error": "Bad request"}
            return jsonify(response_data), 400

        return jsonify(state), 200
    except Exception as esc:
        print(esc, file=sys.stderr)


@app.route("/setup", methods=["GET", "POST"])
def setup_page():
    if is_config():
        return redirect(url_for("home"))

    ac_form = AC_login_setup()

    if request.method == "POST":
        set_dotenv_ac(request)
        init_dotenv()
        return redirect(url_for("home"))

    return render_template("setup.html", form=ac_form)


@app.route("/ping", methods=["GET"])
def is_webserver_running():
    return {"is_webserver_running": True}


init_dotenv()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
