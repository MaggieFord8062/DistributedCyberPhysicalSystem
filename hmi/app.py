
import socket
import json
import threading
import time

from flask import Flask, render_template, jsonify

app = Flask(__name__)

SENSOR_HOST = "192.168.5.83"
SENSOR_PORT = 5091

latest_data = {
    "timestamp": "Waiting for data...",
    "temperature": "--",
    "humidity": "--",
    "pressure": "--",
    "status": "OFFLINE",
}

last_received_time = None
data_lock = threading.Lock()


# Receive sensor readings from the Sense HAT Pi
def start_sensor_receiver():

    global last_received_time

    print("Starting sensor receiver...")

    while True:
        try:
            with socket.create_connection(
                (SENSOR_HOST, SENSOR_PORT),
                timeout=10
            ) as connection:

                print("Connected to Sense HAT Pi!")

                with connection.makefile(
                    "r",
                    encoding="utf-8"
                ) as reader:

                    for line in reader:

                        if not line.strip():
                            continue

                        payload = json.loads(line)

                        with data_lock:
                            latest_data["timestamp"] = payload.get("timestamp")
                            latest_data["temperature"] = payload.get("temperature")
                            latest_data["humidity"] = payload.get("humidity")
                            latest_data["pressure"] = payload.get("pressure")
                            latest_data["status"] = "ONLINE"

                            last_received_time = time.monotonic()

                        print("Received sensor data:", payload)

        except (ConnectionError, OSError) as error:
            print(f"Sensor connection lost: {error}")

        except json.JSONDecodeError as error:
            print(f"Invalid JSON received: {error}")

        with data_lock:
            if (
                last_received_time is None
                or time.monotonic() - last_received_time > 6
            ):
                latest_data["status"] = "OFFLINE"

        print("Retrying connection in 2 seconds...")
        time.sleep(2)


# Get the latest readings and check sensor status
def get_current_data():

    with data_lock:
        data = latest_data.copy()

        if (
            last_received_time is None
            or time.monotonic() - last_received_time > 6
        ):
            data["status"] = "OFFLINE"

        return data


# Display dashboard
@app.route("/")
def index():
    return render_template(
        "index.html",
        data=get_current_data()
    )


# Provide sensor readings to dashboard JavaScript
@app.route("/api/data")
def get_data():
    return jsonify(get_current_data())


if __name__ == "__main__":

    receiver_thread = threading.Thread(
        target=start_sensor_receiver,
        daemon=True
    )

    receiver_thread.start()

    app.run(
        host="0.0.0.0",
        port=8090,
        debug=False
    )
