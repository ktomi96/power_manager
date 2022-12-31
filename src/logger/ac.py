from midea_beautiful import appliance_state
from datetime import datetime
from datetime import date
import pandas as pd
import os
from pprint import pprint


def get_status(address: str, token: str, key: str):
    return appliance_state(address=address, token=token, key=key)


def ac_status(status):

    return {"running": status.state.running, "indoor_temperature": round(status.state.indoor_temperature, 1),
            "out_door_temperature": round(status.state.outdoor_temperature, 1)}


def ac_logging(address, token, key, csv_path: str):
    status = ac_status(get_status(address, token, key))
    now = datetime.now()
    status.update({"date_time": datetime.now().__str__()})
    print(status)
    save_to_csv(status, csv_path)


def save_to_csv(status, csv_path: str):
    df = pd.DataFrame([status])
    file_path = f"{csv_path}"+f"ac/{date.today()}_ac_log.csv"
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", index=False, header=False)

    else:
        df.to_csv(file_path, mode="w", index=False, header=True)


def set_ac_status(*args, status):
    # status.set_state()
    for arg in args:
        print(arg)


if __name__ == '__main__':
    import dotenv

    env_path = ("./env/.env")

    dotenv.find_dotenv(filename=env_path, raise_error_if_not_found=True)
    dotenv.load_dotenv(env_path)

    address = os.getenv("ADDRESS")
    token = os.getenv("TOKEN")
    key = os.getenv("KEY")
    csv_path = "./logs/"
    # status = ac_status(address, token, key)
    pprint(ac_logging(address, token, key, csv_path))
