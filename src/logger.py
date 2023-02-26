try:
    import contextlib
    from ac import AC
    from solar import SOLAR
    from power_meter import power_meter_logger
    from database import AC_LOG, SOLAR_LOG, append_to_db
    import dotenv
    import os
    from datetime import datetime

    from apscheduler.schedulers.blocking import BlockingScheduler
except ImportError:
    print("Import Error")


env_path = "./env/"
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)
address = os.getenv("AC_IP_ADDRESS")
token = os.getenv("TOKEN")
key = os.getenv("KEY")
location_id = os.getenv("LOCATION_ID")
solar_api_key = os.getenv("SOLAR_API_KEY")
log_path = os.getenv("LOG_PATH")
solar_logger_triger_value = os.getenv("SOLAR_LOGGER_TRIGGER_VALUE")
ac_logger_trigger_value = os.getenv("AC_LOGGER_TRIGGER_VALUE")
time_zone = os.getenv("TIME_ZONE")
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"
debug = os.getenv("DEBUG") == "True"
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
install_date = os.getenv("INSTALL_DATE")
power_logger_trigger_value = os.getenv("POWER_LOGGER_TRIGGER_VALUE")


def removechar(str1, n):
    x = str1[:n]
    y = str1[n + 1 :]
    return x + y


def convert_trigger_value(
    solar_logger_triger_value, ac_logger_trigger_value, power_logger_trigger_value
):
    if solar_logger_triger_value.find(":") < 1 or len(solar_logger_triger_value) != 5:
        raise ValueError("Not proper time format")

    solar_time_value = solar_logger_triger_value.split(":")
    solar_logger_trigger_hour = solar_time_value[0]
    solar_logger_trigger_minute = solar_time_value[1]
    if solar_logger_trigger_hour[0] == "0":
        solar_logger_trigger_hour = removechar(solar_logger_trigger_hour, 0)

    if solar_logger_trigger_minute[0] == "0":
        solar_logger_trigger_minute = removechar(solar_logger_trigger_minute, 0)

    power_time_value = power_logger_trigger_value.split(":")
    power_logger_trigger_hour = power_time_value[0]
    power_logger_trigger_minute = power_time_value[1]
    if power_logger_trigger_hour[0] == "0":
        power_logger_trigger_hour = removechar(power_logger_trigger_hour, 0)

    if power_logger_trigger_minute[0] == "0":
        power_logger_trigger_minute = removechar(power_logger_trigger_minute, 0)

    if ac_logger_trigger_value[0] == "0":
        ac_logger_trigger_value = removechar(ac_logger_trigger_value, 0)
    return {
        "ac_logger_trigger_value": ac_logger_trigger_value,
        "solar_logger_trigger_hour": solar_logger_trigger_hour,
        "solar_logger_trigger_minute": solar_logger_trigger_minute,
        "power_logger_trigger_hour": power_logger_trigger_hour,
        "power_logger_trigger_minute": power_logger_trigger_minute,
    }
    # return int(ac_logger_trigger_value), int(hour_value), int(minute_value)


def logger_schulder(*args, ac, solar, trigger_values_dict):
    scheduler = BlockingScheduler(timezone=time_zone)
    scheduler.add_job(
        ac_logging, args=[ac], trigger="interval", minutes=int(ac_logger_trigger_value)
    )
    scheduler.add_job(
        solar_logging,
        args=[solar],
        trigger="cron",
        hour=trigger_values_dict["solar_logger_trigger_hour"],
        minute=trigger_values_dict["solar_logger_trigger_minute"],
    )
    scheduler.add_job(
        power_meter_logging,
        args=[username, password, install_date],
        trigger="cron",
        hour=trigger_values_dict["power_logger_trigger_hour"],
        minute=trigger_values_dict["power_logger_trigger_minute"],
    )
    print("Press Ctrl+C to exit")
    try:
        scheduler.start()
    except SystemExit:
        print("SystemExit, shutdown down")
    except KeyboardInterrupt:
        print("Ctrl+C was pressed, shutdown down")


def ac_logging(ac):  # sourcery skip: extract-duplicate-method
    try:
        global status_mem

        # print(f"Status mem: {status_mem}")
        status = ac.ac_status()
        # print(f"Status: {status}")
        if len(status_mem) == 0:
            pre_status = ac.ac_status()
            if pre_status["indoor_temperature"] <= -23.0:
                pre_status["indoor_temperature"] = 0.0

            if (
                abs(status["indoor_temperature"] - pre_status["indoor_temperature"])
                <= 20
                and abs(
                    status["out_door_temperature"] - pre_status["out_door_temperature"]
                )
                <= 20
            ):
                ac_log = AC_LOG(**status)
                if debug:
                    print(f"AC log: {status}")
                append_to_db([ac_log], db_url)
                status_mem = status
                print(f"Logged data: {datetime.now()}")
            else:
                print(f"Not valid data, didn't logged it: {datetime.now()}")

        elif (
            status_mem["indoor_temperature"] + 20 >= status["indoor_temperature"]
            and status_mem["out_door_temperature"] + 20
            >= status["out_door_temperature"]
        ):

            ac_log = AC_LOG(**status)
            if debug:
                print(f"AC log: {status}")
            append_to_db([ac_log], db_url)
            status_mem = status
            print(f"logged valid data: {datetime.now()}")
        else:
            print(f"Not valid data, didn't logged it: {datetime.now()}")

    except Exception:
        print(f"Coulnd't log ac data: {datetime.now()}")


def solar_logging(solar):
    try:
        status = solar.solar_data()
        solar_log = SOLAR_LOG(**status)
        if debug:
            print(f"AC log: {status}")
        append_to_db([solar_log], db_url)
        print(f"Logged solar data: {datetime.now()}")
    except Exception:
        print(f"Coulnd't log solar data: {datetime.now()}")


def power_meter_logging(username: str, password: str, install_date: str):
    try:
        power_meter_logger(username, password, install_date)

    except Exception:
        print(f"Coulnd't log power meter: {datetime.now()}")


def main(
    ac_logger_trigger_value: str,
    solar_logger_triger_value: str,
    power_logger_trigger_value: str,
):

    ac = AC(address=address, token=token, key=key)
    solar = SOLAR(location_id=location_id, solar_api_key=solar_api_key)

    trigger_values_dict = convert_trigger_value(
        solar_logger_triger_value, ac_logger_trigger_value, power_logger_trigger_value
    )

    logger_schulder(ac=ac, solar=solar, trigger_values_dict=trigger_values_dict)


if __name__ == "__main__":
    status_mem = {}
    main(ac_logger_trigger_value, solar_logger_triger_value, power_logger_trigger_value)
    # ac = AC(address=address, token=token, key=key)
    # ac_logging(ac)
