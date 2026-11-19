
import socket
import json
import time

from sense_hat import SenseHat
from sensor_config import set_reporting_interval

HMI_HOST = "192.168.5.82"
COMMAND_PORT = 5093

sense = SenseHat()
running = True

print("Sense HAT command client starting...")

while running:
    try:
        print(f"Connecting to HMI at {HMI_HOST}:{COMMAND_PORT}...")

        with socket.create_connection(
            (HMI_HOST, COMMAND_PORT), timeout=10
        ) as connection:

            connection.settimeout(None)

            print("Connected to HMI command server!")

            reader = connection.makefile("r", encoding="utf-8")

            for line in reader:
                if not line.strip():
                    continue

                command_data = json.loads(line)
                command = command_data.get("command", "").upper()

                if command == "SET_INTERVAL":
                    interval = float(command_data.get("interval", 1))

                    if interval <= 0:
                        response = {
                            "status": "ERROR",
                            "message": "Interval must be greater than zero."
                        }
                    else:
                        set_reporting_interval(interval)

                        response = {
                            "status": "SUCCESS",
                            "message": f"Reporting interval changed to {interval} seconds."
                        }

                        print(response["message"])

                elif command == "REQUEST_READING":
                    reading = {
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "temperature": round(sense.get_temperature(), 2),
                        "humidity": round(sense.get_humidity(), 2),
                        "pressure": round(sense.get_pressure(), 2)
                    }

                    response = {
                        "status": "SUCCESS",
                        "message": "Fresh sensor reading",
                        "reading": reading
                    }

                    print("Fresh reading:", reading)

                elif command == "DISCONNECT":
                    response = {
                        "status": "SUCCESS",
                        "message": "Command client disconnected."
                    }

                    connection.sendall(
                        (json.dumps(response) + "\n").encode("utf-8")
                    )

                    print("Disconnected by HMI. Staying disconnected.")
                    running = False
                    break

                else:
                    response = {
                        "status": "ERROR",
                        "message": f"Unknown command: {command}"
                    }

                if command != "DISCONNECT":
                    connection.sendall(
                        (json.dumps(response) + "\n").encode("utf-8")
                    )

    except (ConnectionError, OSError) as error:
        print(f"HMI connection unavailable: {error}")

    except (ValueError, json.JSONDecodeError) as error:
        print(f"Invalid command: {error}")

    except KeyboardInterrupt:
        print("\nCommand client stopped.")
        break

    if running:
        print("Retrying in 3 seconds...")
        time.sleep(3)
