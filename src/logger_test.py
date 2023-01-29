import os
import sys
from datetime import datetime, timedelta, date
import pytz

import dotenv

from database import AC_LOG, query_last_row

env_path = ("./env/")
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)

time_zone = os.getenv("TIME_ZONE")
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"
debug = (os.getenv("DEBUG") == "True")


def open_log_file(path: str):
    with open(path, "r") as f1:
        return f1.readlines()[-1]


def clean_log_file(log_file):
    split_list = log_file.split(",")
    return [i.strip() for i in split_list]


def string_to_datetime(time_stamp: str):
    return datetime.fromisoformat(time_stamp)


def main():
    logs_path = "./logs/"
    log_type = "ac"
    ac_query_dict = query_last_row(db_url, AC_LOG).__dict__
    ac_query_time = ac_query_dict["date_time"].replace(tzinfo=pytz.UTC)
    time_to_compare = ac_query_time + timedelta(minutes=2)
    now = datetime.now(pytz.timezone(time_zone))

    if debug:
        print(f"Plus time: {time_to_compare}")
        print(f"Current time: {now}")

    if time_to_compare < now:
        print("System exited with : 1")
        sys.exit(1)
    else:
        print("System exited with : 0")
        sys.exit(0)


if __name__ == "__main__":
    main()
