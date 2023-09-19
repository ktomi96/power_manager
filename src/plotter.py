import glob
import os
import json
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.express as px
from plotly import utils
from dateutil.parser import parse
from memoization import cached
import dotenv

# internal import
from database import AC_LOG, SOLAR_LOG, query_to_df, ac_query_to_df, query_to_df_agr

env_path = "./env/"
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"
debug = os.getenv("DEBUG") == "True"


def ac_plot(df):
    try:
        pio.templates.default = "plotly_white"
        # df = pd.read_csv('logs/ac/2022-12-19_ac_log.csv')
        df = df.set_index("date_time")
        cols = df.columns[1:]
        ncols = len(cols)

        # fig = px.line(df, x='date_time', y='indoor_temperature',
        #              title='AC temperature')
        fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

        for i, col in enumerate(cols, start=1):
            fig.add_trace(
                go.Scatter(x=df[col].index, y=df[col].values, name=col), row=i, col=1
            )

        return json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    except Exception:
        return None


def solar_plot(df):
    try:
        pio.templates.default = "plotly_white"
        df = df.set_index("date_time")
        cols = df.columns[1:3]
        ncols = len(cols)
        fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

        for i, col in enumerate(cols, start=1):
            fig.add_trace(
                go.Bar(x=df[col].index, y=df[col].values, name=col),
                row=i,
                col=1,
            )
        # fig.show()
        return json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    except Exception:
        return None


@cached(ttl=60)
def ac_plotter(range_to_plot: list):
    if date_time_validator(range_to_plot) != True:
        return None

    try:
        range_to_plot[1] = (
            datetime.strptime(range_to_plot[1], "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        ac_df = ac_query_to_df(db_url, AC_LOG, range_to_plot[0], range_to_plot[1])
        if debug:
            print(ac_df)
        return None if ac_df.empty else ac_df.to_json(orient="records")

    except (TypeError, AttributeError, ValueError) as e:
        print("An error occurred:", e)
        return None


@cached(ttl=60)
def solar_plotter(range_to_plot: list):
    if date_time_validator(range_to_plot) != True:
        return None
    try:
        range_to_plot[1] = (
            datetime.strptime(range_to_plot[1], "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        solar_df = query_to_df(db_url, SOLAR_LOG, range_to_plot[0], range_to_plot[1])
        solar_df["date_time"] = solar_df["date_time"].dt.strftime("%Y-%m-%d")
        if debug:
            print(solar_df)
        return None if solar_df.empty else solar_df.to_json(orient="records")
    except (TypeError, AttributeError, ValueError) as e:
        print("An error occurred:", e)
        return None


@cached(ttl=60)
def solar_produce_agr(range_to_agr: list):
    if date_time_validator(range_to_agr) != True:
        return None
    try:
        range_to_agr[1] = (
            datetime.strptime(range_to_agr[1], "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        solar_df = query_to_df_agr(
            db_url, SOLAR_LOG, "power_generated", range_to_agr[0], range_to_agr[1]
        )
        if debug:
            print(solar_df)
        return None if solar_df.empty else solar_df["sum"]
    except (TypeError, AttributeError, ValueError) as e:
        print("An error occurred:", e)
        return None


def merge_csv(folder, filename):
    csv_files = glob.glob(f"{folder}{filename}")
    df_list = (pd.read_csv(file) for file in csv_files)
    df = pd.concat(df_list, ignore_index=False, sort=True)
    # df['date_time'] = pd.to_datetime(df['date_time'])
    df.sort_values(by="date_time", inplace=True)
    return df


def date_time_validator(dates: str):
    try:
        for date in dates:
            parse(date, fuzzy=False)
        return True

    except ValueError:
        return False


if __name__ == "__main__":
    # df = pd.concat(df_list, ignore_index=True)
    # ac_plot(df)
    path = "./logs/solar"
    # plot = ac_plotter(["2023-09-18", "2023-09-18"])
    # print(plot)
