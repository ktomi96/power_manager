
import os
import csv

from database import AC_LOG, SOLAR_LOG
paths = ["logs/solar/", "logs/ac/"]


def migrate_to_database(paths):

    for path in paths:

        dir_list = os.listdir(path)

        for log in dir_list:
            with open(path+log) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # print(row)
                    if path == "logs/solar/":
                        solar_log = SOLAR_LOG()
                        solar_log.append_to_db(**row)
                    elif path == "logs/ac/":
                        if row["running"] == "True":
                            row["running"] = True
                        else:
                            row["running"] = False
                        ac_log = AC_LOG()
                        ac_log.append_to_db(**row)
        print(f"Appended {path} to database")


def main():
    migrate_to_database(paths)


if __name__ == "__main__":
    main()
