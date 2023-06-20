import os

import dotenv
import pandas
from datetime import date, datetime, timedelta
from sqlalchemy.exc import OperationalError

from mvm_smart_meter import get_load_curve, get_all_load_curve, sum_load_curve
from database import (
    POWER_METER,
    POWER_METER_AGGREGATE,
    append_to_db,
    query_last_row,
    df_to_db,
    is_table_exists,
    power_meter_last_entry,
)

env_path = "./env/"
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"
install_date = os.getenv("INSTALL_DATE")
start_mvm_metering_parse_all = os.getenv("START_MVM_METERING_PARSE_ALL")


def power_meter_logger(username: str, password: str, install_date: str):
    date_from = (date.today() - timedelta(1)).strftime("%Y.%m.%d")
    date_to = date_from

    if start_mvm_metering_parse_all == "True":
        print("Parsing all date from power meter installation date, it might take long")
        date_from = install_date

        log_power_data(username, password, date_from, date_to, is_initial_run=True)
        print(f"Imported and appended all power meter data: {datetime.now()}")
        return dotenv.set_key(env_file, "START_MVM_METERING_PARSE_ALL", "False")

    log_power_data(username, password, power_meter_last_entry(), date_to)
    return print(f"Logged power meter data: {datetime.now()}")


def log_power_data(
    username: str, password: str, date_from: str, date_to: str, is_initial_run=False
):
    df = (
        get_all_load_curve(
            username=username, password=password, date_from=date_from, date_to=date_to
        )
        if is_initial_run
        else get_load_curve(
            username=username, password=password, date_from=date_from, date_to=date_to
        )
    )

    df.rename(columns={"datetime": "date_time"}, inplace=True)
    df_to_db(df, db_url, tablename="power_meter")

    df = data_frame_group_by_datetime(df)
    dfs = aggregate_power_meter_response(df)
    for data in dfs:
        df_to_db(data, db_url, tablename="power_meter_aggregate")


def data_frame_group_by_datetime(df: pandas.DataFrame) -> pandas.DataFrame:
    return df.groupby(pandas.Grouper(key="date_time", freq="D"))


def aggregate_power_meter_response(df: pandas.DataFrame) -> pandas.DataFrame:
    dfs = []

    for name, group in df:
        group = group.drop("date_time", axis=1)
        group = group.agg(func=[sum])
        group = group.reset_index(drop=True)
        group["date_time"] = name
        dfs.append(group)
    return dfs


def main():
    try:
        power_meter_logger(username, password, install_date)
    except Exception as a:
        print(a)
        print(f"Coulnd't log: {datetime.now()}")


if __name__ == "__main__":
    main()
