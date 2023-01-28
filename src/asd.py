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
try:

    time_zone = os.getenv("TIME_ZON",raise_error_if_not_found=True)
    db_url = f"{os.getenv('sa')}{os.getenv('sa')}"
    print(time_zone)
except TypeError:
    print("ass")

