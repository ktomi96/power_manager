import glob
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.express as px
from plotly import utils
import json
from dateutil.parser import parse
from memoization import cached

# internal import
from database import AC_LOG, SOLAR_LOG


def ac_plot(df):
    try:
        pio.templates.default = "plotly_white"
        # df = pd.read_csv('logs/ac/2022-12-19_ac_log.csv')
        df = df.set_index('date_time')
        cols = df.columns[:3]
        ncols = len(cols)

        # fig = px.line(df, x='date_time', y='indoor_temperature',
        #              title='AC temperature')
        fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

        for i, col in enumerate(cols, start=1):
            fig.add_trace(go.Scatter(x=df[col].index,
                                     y=df[col].values, name=col), row=i, col=1)

        return json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    except Exception:
        return None


def solar_plot(df):
    try:

        pio.templates.default = "plotly_white"
        df = df.set_index('date_time')
        cols = df.columns[1:3]
        ncols = len(cols)
        fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

        for i, col in enumerate(cols, start=1):
            fig.add_trace(go.Bar(x=df[col].index,
                                 y=df[col].values, name=col), row=i, col=1,)

        return json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    except Exception:
        return None


@cached(ttl=60)
def ac_plotter(range_to_plot: str):
    ac_log = AC_LOG()

    if range_to_plot == "all":
        ac_df = ac_log.query_to_df()
        return ac_plot(ac_df)

    elif date_time_validator(range_to_plot) == True:
        try:
            ac_df = merge_csv("./logs/ac", f'/{range_to_plot}_ac_log.csv')
            return ac_plot(ac_df)

        except ValueError:
            return None


@cached(ttl=60)
def solar_plotter():
    solar_log = SOLAR_LOG()
    solar_df = solar_log.query_to_df()
    return solar_plot(solar_df)


def merge_csv(folder, filename):
    csv_files = glob.glob(f"{folder}{filename}")
    df_list = (pd.read_csv(file) for file in csv_files)
    df = pd.concat(df_list, ignore_index=False, sort=True)
    # df['date_time'] = pd.to_datetime(df['date_time'])
    df.sort_values(by='date_time', inplace=True)
    return df


def date_time_validator(date: str):
    try:
        parse(date, fuzzy=False)
        return True

    except ValueError:
        return False


if __name__ == "__main__":
    path = "./logs/ac"
    csv_files = glob.glob(f"{path}/*_ac_log.csv")
    df_list = (pd.read_csv(file) for file in csv_files)
    # df = pd.concat(df_list, ignore_index=True)
    # ac_plot(df)
    # path = "./logs/solar"
    ac_plotter("all")
