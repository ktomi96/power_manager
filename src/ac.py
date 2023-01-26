from midea_beautiful import appliance_state
from datetime import datetime
from datetime import date
import pandas as pd
import os
import dotenv
from pprint import pprint
from database import AC_LOG


class AC(object):
    def __init__(self, address: str, token: str, key: str):
        self.address = address
        self.token = token
        self.key = key

    def get_status(self):
        return appliance_state(address=self.address, token=self.token, key=self.key)

    def ac_status(self, status):

        return {"running": status.state.running, "indoor_temperature": round(status.state.indoor_temperature, 1),
                "out_door_temperature": round(status.state.outdoor_temperature, 1)}

    def ac_logging(self, csv_path: str):
        status = self.ac_status(self.get_status())
        now = datetime.now()
        status.update({"date_time": datetime.now().__str__()})
        print(status)
        self.save_to_csv(status, csv_path)

    def save_to_csv(self, status, csv_path: str):
        df = pd.DataFrame([status])
        file_path = f"{csv_path}"+f"ac/{date.today()}_ac_log.csv"
        if os.path.exists(file_path):
            df.to_csv(file_path, mode="a", index=False, header=False)

        else:
            df.to_csv(file_path, mode="w", index=False, header=True)

    def save_to_db(self, status):
        print(status)
        ac_data = AC_LOG.append_to_db(**status)

    def set_ac_status(self, **kwargs):
        status = self.get_status()
        status.set_state(**kwargs)
        pprint(status)

    def set_tempature(self, temp: float):
        targer_temp = {"target_temperature": temp}
        self.set_ac_status(**targer_temp)

    def turn_ac_on(self, state: bool):
        ac_state = {"running": state}
        self.set_ac_status(**ac_state)


def main():
    env_path = ("./env/")
    env_file = f"{env_path}.env"

    dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
    dotenv.load_dotenv(env_file)

    address = os.getenv("ADDRESS")
    token = os.getenv("TOKEN")
    key = os.getenv("KEY")
    log_path = os.getenv("LOG_PATH")
    ac = AC(address, token, key)
    # status = ac_status(address, token, key)
    # pprint(ac_logging(address, token, key, log_path))
    # ac.set_tempature(22.0)
    # print(ac.get_status())


if __name__ == "__main__":
    main()
