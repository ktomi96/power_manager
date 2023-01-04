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


def ac_plot(df):
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


def solar_plot(df):
    pio.templates.default = "plotly_white"
    df = df.set_index('date_time')
    cols = df.columns[2:]
    ncols = len(cols)
    fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

    for i, col in enumerate(cols, start=1):
        fig.add_trace(go.Bar(x=df[col].index,
                      y=df[col].values, name=col), row=i, col=1,)

    return json.dumps(fig, cls=utils.PlotlyJSONEncoder)


@cached(ttl=60)
def graph_plotter(range_to_plot: str):
    if range_to_plot == "all":
        ac_df = merge_csv("./logs/ac", '/*_ac_log.csv')
        solar_df = merge_csv("./logs/solar", '/*_solar_log.csv')
        ac_fig = ac_plot(ac_df)
        solar_fig = solar_plot(solar_df)
        return [ac_fig, solar_fig]

    elif date_time_validator(range_to_plot) == True:
        ac_df = merge_csv("./logs/ac", f'/{range_to_plot}_ac_log.csv')
        solar_df = merge_csv("./logs/solar", '/*_solar_log.csv')
        ac_fig = ac_plot(ac_df)
        solar_fig = solar_plot(solar_df)
        return [ac_fig, solar_fig]


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


if __name__ == '__main__':
    path = "./logs/ac"
    csv_files = glob.glob(f"{path}/*_ac_log.csv")
    df_list = (pd.read_csv(file) for file in csv_files)
    # df = pd.concat(df_list, ignore_index=True)
    # ac_plot(df)
    # path = "./logs/solar"
    df = graph_plotter("all")
