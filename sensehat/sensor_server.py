
from sense_hat import SenseHat
from datetime import datetime
import socket
import json
import time

sense = SenseHat()

HOST = "0.0.0.0"
PORT = 5091

# Create the TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print(f"Sensor server listening on port {PORT}...")

try:
    while True:
        # Wait for the HMI Raspberry Pi to connect
        connection, address = server.accept()

        print(f"HMI connected: {address}")

        try:
            while True:
                # Read sensor values
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "temperature": sense.get_temperature(),
                    "humidity": sense.get_humidity(),
                    "pressure": sense.get_pressure()
                }

                # Convert readings to JSON
                message = json.dumps(data) + "\n"

                # Send readings to the HMI
                connection.sendall(message.encode("utf-8"))

                print("Sent:", message.strip())

                time.sleep(1)

        except (BrokenPipeError, ConnectionResetError):
            print("HMI disconnected.")

        finally:
            connection.close()

except KeyboardInterrupt:
    print("Sensor server stopped.")

finally:
    server.close()
