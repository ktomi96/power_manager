#!/usr/bin/env python
try:
    import os
    import requests
    import glob

    from flask import Flask, redirect, request, url_for, render_template, escape, flash, session, jsonify
    from livereload import Server, shell
    import dotenv
    import pandas as pd
    from datetime import date, timedelta, datetime

    from forms import AC_login_setup
    from plotter import ac_plotter, solar_plotter
    from migrate_csv_to_sql import migrate_to_database
except ImportError:
    print("Exited with import error")
    sys.exit(1)

env_path = ("./env/")
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)

logs_dir = ["ac", "solar"]

logs_path = os.getenv("LOG_PATH")
db_path = os.getenv("DB_PATH")
db_url = f"{os.getenv('DB')}{db_path}"
debug = (os.getenv("DEBUG") == "True")

app = Flask(__name__, template_folder="templates/")

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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
        dotenv.set_key(env_file, key,
                       value)


@app.route("/")
def home():
    if not is_config() or not is_database():
        return redirect(url_for("setup_page"))

    today = date.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    month_first_day = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    if debug:
        print(f"AC plot date: {today}")
        print(f"Solar plot From: {month_first_day}, To: {yesterday}")
    ac_fig = ac_plotter([today, now])
    solar_fig = solar_plotter([month_first_day, yesterday])

    return render_template("home.html", ac_fig=ac_fig, solar_fig=solar_fig)


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
    if not is_config() or not is_database():
        return redirect(url_for("setup_page"))

    response = {"is_webserver_running": True}
    return jsonify(response)


init_dotenv()
if __name__ == "__main__":

    server = Server(app.wsgi_app)
    server.watch(env_file)
    server.serve(host="localhost", port=5000)
