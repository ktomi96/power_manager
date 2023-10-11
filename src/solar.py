import math
import os
from datetime import datetime, date

from solaredge.api.client import Client
import requests


# TODO read location from env variable


class SOLAR(object):
    def __init__(self, location_id, solar_api_key):
        self.location_id = location_id
        self.solar_api_key = solar_api_key

    def get_daytime(self):
        payload = {"lat": "47.1611615", "lng": "19.5057541", "formatted": "0"}

        r = requests.get("https://api.sunrise-sunset.org/json", params=payload)
        got_json = (r.json())["results"]

        return got_json["day_length"] / 3600

    def get_data(self, date_str=None):
        se_client = Client()
        se_client.set_api_key(self.solar_api_key)
        if date_str is None:
            date_str = date.today().strftime("%Y-%m-%d")
        print(date_str)
        number_of_sites = se_client.sites.get_energy(
            self.location_id, date_str, date_str, "QUARTER_OF_AN_HOUR"
        )
        return (number_of_sites["energy"])["values"]

    # sourcery skip: for-append-to-extend, list-comprehension

    def filter_data(self, date_str=None):
        if date_str is None:
            date_str = date.today().strftime("%Y-%m-%d")

        filtered = self.get_data(date_str)
        new_list = []
        num_prod_time = 96
        for fo in filtered:
            foo = list(fo.values())
            strp = datetime.strptime(foo[0], "%Y-%m-%d %H:%M:%S")
            foo[0] = strp
            if foo[1] is None:
                num_prod_time -= 1
                foo[1] = 0
            else:
                foo[1] = int(foo[1])
            new_list.append(foo)

        y = [n[1] for n in new_list]
        return y, num_prod_time

    def solar_data(self, date_str=None):
        y, num_prod_time = self.filter_data(date_str)
        power_balance = math.fsum(y)
        prod_time = (num_prod_time * 15) / 60
        daytime = self.get_daytime()

        return {
            "power_generated": round(power_balance, 2),
            "production_time": round(prod_time, 2),
            "daytime": round(daytime, 2),
            "efficeny": round((prod_time / daytime), 2),
        }


if __name__ == "__main__":
    import argparse
    import dotenv
    import re

    from database import SOLAR_LOG, append_to_db

    dotenv.load_dotenv("./env/.env")
    location_id = os.getenv("LOCATION_ID")
    solar_api_key = os.getenv("SOLAR_API_KEY")
    db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"
    csv_path = "./logs/"
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Solar Data Logger")
    # Add a command-line argument for specifying the date
    parser.add_argument(
        "--date", type=str, help="Specify the date in YYYY-MM-DD format"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the date_str from the command-line arguments or use the default
    date_str = args.date or None
    solar = SOLAR(location_id=location_id, solar_api_key=solar_api_key)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")
    status = solar.solar_data(date_str=date_str)
    solar_log = SOLAR_LOG(**status)
    print(f"AC log: {status}")
    append_to_db([solar_log], db_url)
    print(f"Logged solar data: {date_str}")
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(solar_logging, args=[
                      csv_path, location_id, solar_api_key], trigger='cron', hour=13, minute=29)
    scheduler.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
    """
