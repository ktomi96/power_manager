from midea_beautiful import appliance_state
from datetime import datetime
from datetime import date
import pandas as pd
import os


def ac_status(address: str, token: str, key: str):
    status = appliance_state(address=address, token=token, key=key)
    # workaround where outdoor temp near 0˚C doesnt get rounded in the midea_beatufil libery
    if status.state.outdoor_temperature == 2.2250738585072014e-308:
        out_temp = 0
    else:
        out_temp = status.state.outdoor_temperature

    return {"running": status.state.running, "indoor_temperature": status.state.indoor_temperature,
            "out_door_temperature": out_temp}


def ac_logging(address: str, token: str, key: str, csv_path: str):
    status = ac_status(address, token, key)
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
