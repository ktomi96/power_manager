import os
import dotenv

from midea_beautiful import appliance_state

from pprint import pprint


class AC(object):
    def __init__(self, address: str, token: str, key: str):
        """
        Initializes an AC object.

        Args:
            address (str): The address of the AC unit.
            token (str): The token for authentication.
            key (str): The key for accessing the AC unit.

        """
        self.address = address
        self.token = token
        self.key = key

        self.ac_modes = {
            0: "fan_mode",
            1: "auto_mode",
            2: "cooling_mode",
            3: "drying_mode",
            4: "heating_mode",
        }

    def get_status(self):
        """
        Retrieves the current status of the AC unit.

        Returns:
            dict: The status of the AC unit, including running state, indoor temperature, and outdoor temperature.

        """
        return appliance_state(address=self.address, token=self.token, key=self.key)

    def ac_status(self):
        """
        Retrieves the AC unit's status.

        Returns:
            dict: The status of the AC unit, including running state, indoor temperature, and outdoor temperature.

        """
        status = self.get_status()
        return {
            "running": status.state.running,
            "indoor_temperature": round(status.state.indoor_temperature, 1),
            "out_door_temperature": round(status.state.outdoor_temperature, 1),
        }

    def convert_modes(self, mode):
        forward_mapping = self.ac_modes
        reverse_mapping = {v: k for k, v in forward_mapping.items()}

        if mode in forward_mapping:
            return forward_mapping[mode]
        elif mode in reverse_mapping:
            return reverse_mapping[mode]

    def set_ac_status(self, **kwargs):
        """
        Sets the status of the AC unit.

        Args:
            **kwargs: Keyword arguments representing the desired state of the AC unit.

        """
        status = self.get_status()
        status.set_state(**kwargs)
        pprint(status)

    def set_temperature(self, temp: float):
        """
        Sets the target temperature of the AC unit.

        Args:
            temp (float): The desired target temperature.

        """
        target_temp = {"target_temperature": temp}
        self.set_ac_status(**target_temp)

    def change_ac_state(self, state: bool):
        """
        Turns the AC unit on or off.

        Args:
            state (bool): True to turn on the AC unit, False to turn it off.

        """
        ac_state = {"running": state}
        self.set_ac_status(**ac_state)

    def set_mode(self, mode: int):
        """
        Sets the mode of the AC unit.

        Args:
            mode (int): The desired mode for the AC unit.
                Supported modes:
                - 0: Fan mode
                - 1: Auto mode
                - 2: Cooling mode
                - 3: Drying mode
                - 4: Heating mode

        Raises:
            ValueError: If the mode is not a supported mode.

        """
        if mode not in [0, 1, 2, 3, 4]:
            raise ValueError(
                "Unsupported mode. Please choose a valid mode between 0 and 4."
            )

        set_mode = {"mode": mode}
        self.set_ac_status(**set_mode)


def main():
    env_path = "./env/"
    env_file = f"{env_path}.env"

    dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
    dotenv.load_dotenv(env_file)

    address = os.getenv("AC_IP_ADDRESS")
    token = os.getenv("TOKEN")
    key = os.getenv("KEY")
    log_path = os.getenv("LOG_PATH")
    ac = AC(address, token, key)
    ac.set_mode(4)
    status = ac.get_status()


if __name__ == "__main__":
    main()
