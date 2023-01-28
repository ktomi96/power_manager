
import os
import csv
from datetime import datetime
import pytz

import dotenv

from database import AC_LOG, SOLAR_LOG, append_to_db, query_last_row


env_path = ("./env/")
env_file = f"{env_path}.env"

dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)

time_zone = os.getenv("TIME_ZONE")
log_path = os.getenv("LOG_PATH")
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"


def migrate_to_database(log_path, db_url):
    paths = [f"{log_path}solar/", f"{log_path}ac/"]
    obj_list = []
    time_zone_obj = pytz.timezone(time_zone)
    for path in paths:
        dir_list = os.listdir(path)

        for log in dir_list:
            with open(path+log) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if path == paths[0]:
                        row["date_time"] = time_zone_obj.localize(datetime.strptime(
                            str(row["date_time"]), "%Y-%m-%d"))

                        obj_list.append(SOLAR_LOG(**row))

                    elif path == paths[1]:
                        row["date_time"] = time_zone_obj.localize(datetime.strptime(
                            str(row["date_time"]), "%Y-%m-%d %H:%M:%S.%f"))
                        row["running"] = row["running"] == "True"
                        obj_list.append(AC_LOG(**row))
                        test_data = row

    append_to_db(obj_list, db_url)
    test_query = query_last_row(db_url, AC_LOG).__dict__

    if test_query["date_time"].ctime() != test_data["date_time"].ctime():
        print("Corrupted migration to database")
        return None
    print("Appended to database")


def main():
    migrate_to_database(log_path, db_url)


if __name__ == "__main__":
    main()
