
from sense_hat import SenseHat
from datetime import datetime
import socket
import json
import time

from sensor_config import get_reporting_interval

sense = SenseHat()

HOST = "0.0.0.0"
PORT = 5091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"Sensor server listening on port {PORT}...")
print("Waiting for HMI connection...")

try:
    while True:
        connection, address = server.accept()
        print(f"HMI connected: {address}")

        try:
            while True:
                # Read the latest interval from shared settings
                interval = get_reporting_interval()

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

                time.sleep(interval)

        except (BrokenPipeError, ConnectionResetError, OSError):
            print("HMI disconnected.")

        finally:
            connection.close()

except KeyboardInterrupt:
    print("\nSensor server stopped.")

finally:
    server.close()
