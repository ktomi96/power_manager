import os
import sys
from datetime import datetime, timedelta, date


def open_log_file(path: str):
    with open(path, "r") as f1:
        return f1.readlines()[-1]


def clean_log_file(log_file):
    split_list = log_file.split(",")
    return [i.strip() for i in split_list]


def string_to_datetime(time_stamp: str):
    return datetime.fromisoformat(time_stamp)


if __name__ == "__main__":
    logs_path = "./logs/"
    log_type = "ac"
    log_file = open_log_file(
        f"{logs_path}{log_type}/{date.today()}_{log_type}_log.csv")
    clean_log = clean_log_file(log_file)
    datetime_log = string_to_datetime(clean_log[-1])
    print(datetime_log + timedelta(minutes=2))

    if (datetime_log + timedelta(minutes=2)) < datetime.now():
        print("System exited with : 1")
        sys.exit(1)
    else:
        print("System exited with : 0")
        sys.exit(0)
