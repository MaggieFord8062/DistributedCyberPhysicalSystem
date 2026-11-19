
import json
import os

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sensor_settings.json"
)

DEFAULT_INTERVAL = 1.0


def set_reporting_interval(interval):
    """Save the reporting interval for the sensor server."""
    settings = {"reporting_interval": float(interval)}

    temp_file = CONFIG_FILE + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(settings, file)

    os.replace(temp_file, CONFIG_FILE)


def get_reporting_interval():
    """Read the current reporting interval."""
    try:
        with open(CONFIG_FILE, "r") as file:
            settings = json.load(file)

        interval = float(settings["reporting_interval"])

        if interval > 0:
            return interval

    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError):
        pass

    return DEFAULT_INTERVAL
