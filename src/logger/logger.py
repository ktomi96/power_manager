import contextlib
from ac import ac_logging
from solar import solar_logging
import dotenv
import os
from datetime import datetime
from datetime import date
import time


from apscheduler.schedulers.asyncio import AsyncIOScheduler


try:
    import asyncio
except ImportError:
    import trollius as asyncio

dotenv.load_dotenv(".env")
address = os.getenv("ADDRESS")
token = os.getenv("TOKEN")
key = os.getenv("KEY")
location_id = os.getenv("LOCATION_ID")
solar_api_key = os.getenv("SOLAR_API_KEY")
csv_path = "logs/"


def tick():
    print(f'Tick! The time is: {datetime.now()}')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(ac_logging, args=[address, token, key,
                      csv_path], trigger='interval', minutes=5)
    scheduler.add_job(solar_logging, args=[
                      csv_path, location_id, solar_api_key], trigger='cron', hour=1, minute=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.get_event_loop().run_forever()
