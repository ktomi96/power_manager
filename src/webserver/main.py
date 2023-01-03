#!/usr/bin/env python
import os
import requests
import glob

from flask import Flask, redirect, request, url_for, render_template, escape, flash, session
from livereload import Server, shell
import dotenv
import pandas as pd

from forms import AC_login_setup
from plotter import graph_plotter
from datetime import date



dotenv_path = "./env/.env"
logs_dir = ["ac", "solar"]
logs_path = "./logs/"

app = Flask(__name__, template_folder="templates/")

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def is_config():
    return os.path.exists(dotenv_path)


def init_dotenv():
    dotenv.load_dotenv(dotenv_path)


def set_dotenv_ac(request):
    dotenv.set_key(dotenv_path, "ADDRESS",
                   request.form['ADDRESS'])

    dotenv.set_key(dotenv_path, "TOKEN",
                   request.form['TOKEN'])

    dotenv.set_key(dotenv_path, "KEY",
                   request.form['KEY'])


@app.route("/")
def home():
    if not is_config():
        return redirect(url_for("setup_page"))

    if os.listdir(logs_path+logs_dir[0]) and os.listdir(logs_path+logs_dir[1]):
        #  TODO probably needs caching no to render in every refresh
        figs = graph_plotter(date.today().strftime('%Y-%m-%d'))
        return render_template("home.html", figs=figs)

    else:
        return "No logs yet"


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


init_dotenv()
if __name__ == "__main__":

    server = Server(app.wsgi_app)
    server.watch(dotenv_path)
    server.serve(host="localhost", port=5500)
