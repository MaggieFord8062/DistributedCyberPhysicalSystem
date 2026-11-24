
from sense_hat import SenseHat
from datetime import datetime
import socket
import json
import time

from sensor_config import get_reporting_interval

sense = SenseHat()

HOST = "0.0.0.0"
PORT = 5091

# Local event forwarding address
EVENT_HOST = "127.0.0.1"
EVENT_PORT = 5095


def send_event(event_name, details):
    """Send an event to the local event server."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "event": event_name,
        "details": details
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as event_socket:
            event_socket.sendto(
                json.dumps(event).encode("utf-8"),
                (EVENT_HOST, EVENT_PORT)
            )

        print(f"Sent event: {event_name}")

    except OSError as error:
        print(f"Could not send event: {error}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"Sensor server listening on port {PORT}...")
print("Waiting for HMI connection...")

# Report successful sensor initialization
send_event(
    "SENSOR_SERVER_STARTED",
    "Sense HAT initialized successfully."
)

try:
    while True:
        connection, address = server.accept()
        print(f"HMI connected: {address}")

        try:
            while True:
                interval = get_reporting_interval()

                try:
                    data = {
                        "timestamp": datetime.now().isoformat(),
                        "temperature": sense.get_temperature(),
                        "humidity": sense.get_humidity(),
                        "pressure": sense.get_pressure()
                    }

                    message = json.dumps(data) + "\n"
                    connection.sendall(message.encode("utf-8"))

                    print(
                        f"Sent sensor data | "
                        f"Temperature: {data['temperature']:.2f} °C | "
                        f"Interval: {interval} seconds"
                    )

                except Exception as error:
                    send_event(
                        "SENSOR_READ_ERROR",
                        str(error)
                    )

                    print(f"Sensor read error: {error}")

                time.sleep(interval)

        except (BrokenPipeError, ConnectionResetError, OSError):
            print("HMI disconnected.")

        finally:
            connection.close()

except KeyboardInterrupt:
    print("\nSensor server stopped.")

finally:
    server.close()
