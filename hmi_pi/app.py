from datetime import datetime
import json
import socket
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

latest_data = {
    "timestamp": "Waiting for data...",
    "temperature": "--",
    "humidity": "--",
    "pressure": "--",
    "status": "OFFLINE",
}

# TCP Socket Listener for Sensor Data (Port 5091)
def start_tcp_listener():
    HOST = "0.0.0.0"  # Listen on all local interfaces
    PORT = 5091

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"TCP Sensor Listener started on port {PORT}...")

    while True:
        try:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    payload = json.loads(data.decode("utf-8"))
                    # Update global state with incoming data
                    latest_data["timestamp"] = payload.get("timestamp")
                    latest_data["temperature"] = payload.get("temperature")
                    latest_data["humidity"] = payload.get("humidity")
                    latest_data["pressure"] = payload.get("pressure")
                    latest_data["status"] = "ONLINE"
        except Exception as e:
            print(f"Error receiving data: {e}")

@app.route("/")
def index():
    return render_template("index.html", data=latest_data)

@app.route("/api/data")
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_tcp_listener, daemon=True)
    listener_thread.start()

    app.run(host="0.0.0.0", port=8090, debug=False)