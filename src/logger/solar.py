from solaredge.api.client import Client
from datetime import datetime, timedelta, date
import numpy as np
import math
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time
import zoneinfo
import requests
import pandas as pd
import os

# TODO read location from env variable


def get_daytime():
    payload = {'lat': '47.1611615', 'lng': '19.5057541', 'formatted': '0'}

    r = requests.get('https://api.sunrise-sunset.org/json', params=payload)
    got_json = (r.json())['results']

    return got_json['day_length']/3600


def get_data(location_id, solar_api_key):
    se_client = Client()
    se_client.set_api_key(solar_api_key)
    today_str = date.today().strftime('%Y-%m-%d')
    number_of_sites = se_client.sites.get_energy(
        location_id, today_str, today_str, 'QUARTER_OF_AN_HOUR')
    return (number_of_sites['energy'])['values']


# sourcery skip: for-append-to-extend, list-comprehension
def filter_data(location_id, solar_api_key):
    filterd = get_data(location_id, solar_api_key)
    new_list = []
    num_prod_time = 96
    for fo in filterd:
        foo = list(fo.values())
        strp = datetime.strptime(foo[0], '%Y-%m-%d %H:%M:%S')
        foo[0] = strp
        if foo[1] is None:
            num_prod_time -= 1
            foo[1] = 0
        else:
            foo[1] = int(foo[1])
        new_list.append(foo)

    y = [n[1] for n in new_list]
    return y, num_prod_time


def solar_data(location_id, solar_api_key):
    y, num_prod_time = filter_data(location_id, solar_api_key)
    power_balance = math.fsum(y)
    prod_time = (num_prod_time*15)/60
    daytime = get_daytime()
    today_str = date.today().strftime('%Y-%m-%d')

    print(f'Power generated : {round(power_balance,2)} Wh')
    print(f'Production time: {round(prod_time, 2)} h')
    print(f'Daytime: {round(daytime, 2)} h')
    print(f'Efficeny {round((prod_time/daytime), 2)}')

    return {"date_time": today_str, "power_generated": round(power_balance, 2), "production_time": round(prod_time, 2),
            "daytime": round(daytime, 2), "efficeny": round((prod_time/daytime), 2)}


def solar_logging(csv_path: str, location_id: str, solar_api_key: str):
    data = solar_data(location_id, solar_api_key)
    today = datetime.now()
    datem = date(today.year, today.month, 1)
    print(datem)
    df = pd.DataFrame([data])
    file_path = f"{csv_path}"+f"solar/{datem}_solar_log.csv"

    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", index=False, header=False)

    else:
        df.to_csv(file_path, mode="w", index=False, header=True)


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv("./env/.env")
    location_id = os.getenv("LOCATION_ID")
    solar_api_key = os.getenv("SOLAR_API_KEY")
    csv_path = "./logs/"
    print(solar_data(location_id, solar_api_key).__repr__())
    '''
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
    '''
