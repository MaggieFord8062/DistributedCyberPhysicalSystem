
import socket
import json
import time

# Sense HAT Pi information
SERVER_HOST = "192.168.5.83"
SERVER_PORT = 5091

print("Starting sensor receiver...")

while True:
    try:
        # Connect to the Sense HAT Pi
        with socket.create_connection(
            (SERVER_HOST, SERVER_PORT),
            timeout=10
        ) as connection:

            print("Connected to Sense HAT Pi!")

            # Read incoming messages one line at a time
            with connection.makefile("r", encoding="utf-8") as reader:
                for line in reader:
                    if not line.strip():
                        continue

                    # Convert JSON into a Python dictionary
                    data = json.loads(line)

                    # Display received readings
                    print("\nReceived sensor data:")
                    print(f"Timestamp: {data['timestamp']}")
                    print(f"Temperature: {data['temperature']:.2f} °C")
                    print(f"Humidity: {data['humidity']:.2f} %")
                    print(f"Pressure: {data['pressure']:.2f} hPa")

    except (ConnectionError, OSError) as error:
        print(f"Connection lost or unavailable: {error}")
        print("Retrying in 2 seconds...")

    except json.JSONDecodeError as error:
        print(f"Invalid JSON received: {error}")

    time.sleep(2)
