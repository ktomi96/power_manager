import contextlib
from ac import ac_logging
from solar import solar_logging
import dotenv
import os


from apscheduler.schedulers.blocking import BlockingScheduler


try:
    import asyncio
except ImportError:
    import trollius as asyncio

env_path = ("./env/.env")
dotenv.find_dotenv(filename=env_path, raise_error_if_not_found=True)
dotenv.load_dotenv(env_path)
address = os.getenv("ADDRESS")
token = os.getenv("TOKEN")
key = os.getenv("KEY")
location_id = os.getenv("LOCATION_ID")
solar_api_key = os.getenv("SOLAR_API_KEY")
csv_path = "./logs/"

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(ac_logging, args=[address, token, key,
                      csv_path], trigger='interval', seconds=5)
    scheduler.add_job(solar_logging, args=[
                      csv_path, location_id, solar_api_key], trigger='cron', hour=23, minute=00)
    print('Press Ctrl+C to exit')
    try:
        scheduler.start()
    except SystemExit:
        print('SystemExit, shutdown down')
    except KeyboardInterrupt:
        print('Ctrl+C was pressed, shutdown down')
