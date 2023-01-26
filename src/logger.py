try:
    import contextlib
    from ac import AC
    from solar import SOLAR
    from database import AC_LOG, SOLAR_LOG
    import dotenv
    import os
    from datetime import datetime

    from apscheduler.schedulers.blocking import BlockingScheduler
except ImportError:
    print("Import Error")


env_path = ("./env/")
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)
address = os.getenv("ADDRESS")
token = os.getenv("TOKEN")
key = os.getenv("KEY")
location_id = os.getenv("LOCATION_ID")
solar_api_key = os.getenv("SOLAR_API_KEY")
log_path = os.getenv("LOG_PATH")
solar_logger_triger_value = os.getenv("SOLAR_LOGGER_TRIGGER_VALUE")
ac_logger_trigger_value = os.getenv("AC_LOGGER_TRIGGER_VALUE")
time_zone = os.getenv("TIME_ZONE")


def removechar(str1, n):
    x = str1[: n]
    y = str1[n + 1:]
    return x + y


def convert_trigger_value(solar_logger_triger_value, ac_logger_trigger_value):
    if solar_logger_triger_value.find(":") < 1 or len(solar_logger_triger_value) != 5:
        raise ValueError("Not proper time format")

    time_value = solar_logger_triger_value.split(":")
    hour_value = time_value[0]
    minute_value = time_value[1]
    if hour_value[0] == "0":
        hour_value = removechar(hour_value, 0)

    if minute_value[0] == "0":
        minute_value = removechar(minute_value, 0)

    if ac_logger_trigger_value[0] == "0":
        ac_logger_trigger_value = removechar(ac_logger_trigger_value, 0)

    return int(ac_logger_trigger_value), int(hour_value), int(minute_value)


def logger_schulder(*args, ac, solar, ac_log, solar_log, hour_value, minute_value):
    scheduler = BlockingScheduler(timezone=time_zone)
    scheduler.add_job(ac_logging, args=[
                      ac, ac_log], trigger='interval', minutes=int(ac_logger_trigger_value))
    scheduler.add_job(solar_logging, args=[
                      solar, solar_log], trigger='cron', hour=hour_value, minute=minute_value)
    print('Press Ctrl+C to exit')
    try:
        scheduler.start()
    except SystemExit:
        print('SystemExit, shutdown down')
    except KeyboardInterrupt:
        print('Ctrl+C was pressed, shutdown down')


def ac_status(ac: object):
    status = ac.ac_status(ac.get_status())
    now = datetime.now()

    status.update({"date_time": datetime.now().__str__()})
    return status


def ac_logging(ac, ac_log):  # sourcery skip: extract-duplicate-method
    global status_mem
    print(f"Status mem: {status_mem}")
    status = ac_status(ac)
    print(f"Status: {status}")
    if len(status_mem) == 0:
        pre_status = ac_status(ac)
        if pre_status["indoor_temperature"] <= -23.0:
            pre_status["indoor_temperature"] = 0.0
        print(f"Pre status: {pre_status}")
        if (abs(status["indoor_temperature"] - pre_status["indoor_temperature"]) <= 20 and
                abs(status["out_door_temperature"] - pre_status["out_door_temperature"]) <= 20):

            ac_log.append_to_db(**status)
            status_mem = status
            print(f"Logged data: {datetime.now()}")
        else:
            print(f"Not valid data, didn't logged it: {datetime.now()}")

    elif (status_mem["indoor_temperature"] + 20 >= status["indoor_temperature"] and
          status_mem["out_door_temperature"] + 20 >= status["out_door_temperature"]):

        ac_log.append_to_db(**status)
        status_mem = status
        print(f"logged valid data: {datetime.now()}")
    else:
        print(f"Not valid data, didn't logged it: {datetime.now()}")


def solar_logging(solar, solar_log):
    status = solar.solar_data()
    solar_log.append_to_db(**status)
    print(f"Logged solar data: {datetime.now()}")


def main(ac_logger_trigger_value, solar_logger_triger_value):
    ac = AC(address=address, token=token, key=key)
    solar = SOLAR(location_id=location_id, solar_api_key=solar_api_key)
    ac_log = AC_LOG()
    solar_log = SOLAR_LOG()
    # status = ac_status(ac)

    ac_logger_trigger_value, hour_value, minute_value = convert_trigger_value(
        solar_logger_triger_value, ac_logger_trigger_value)

    logger_schulder(ac_logger_trigger_value, hour_value,
                    minute_value, time_zone, ac=ac, solar=solar, ac_log=ac_log, solar_log=solar_log, hour_value=hour_value, minute_value=minute_value)


if __name__ == '__main__':
    status_mem = {}
    main(ac_logger_trigger_value, solar_logger_triger_value)
