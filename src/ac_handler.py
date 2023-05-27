import os
import sys
import dotenv

from ac import AC

env_path = "./env/"
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)
address = os.getenv("AC_IP_ADDRESS")
token = os.getenv("TOKEN")
key = os.getenv("KEY")
log_path = os.getenv("LOG_PATH")


def ac_status_getter():
    # TODO: Implement this at class level, workaround for now not to interfere with the logger
    try:
        ac = AC(address, token, key)
        status = ac.get_status()
        return {
            "running": status.state.running,
            "mode": ac.convert_modes(status.state.mode),
            "target_temperature": status.state.target_temperature,
            "indoor_temperature": round(status.state.indoor_temperature, 1),
            "out_door_temperature": round(status.state.outdoor_temperature, 1),
        }
    except Exception as esc:
        print(esc, file=sys.stderr)


def ac_status_setter(ac_settings):
    try:
        # TODO: Changing ac status takes 8s, only should HTTP 200 if its running. There should be a check portion in this function for that
        ac = AC(address, token, key)
        ac_settings["mode"] = ac.convert_modes(ac_settings.get("mode"))
        ac.set_ac_status(**ac_settings)

    except Exception as esc:
        print(esc, file=sys.stderr)


def main():
    ac_test = {"mode": "cooling_mode", "running": True, "target_temperature": 22.0}
    ac_status_setter(ac_test)


if __name__ == "__main__":
    main()
