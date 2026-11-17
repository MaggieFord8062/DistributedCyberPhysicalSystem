import json
import socket
from datetime import datetime
import time

HMI_IP = "127.0.0.1"  # Localhost since your server is running on your machine
PORT = 5091

# Simulated sensor reading
data = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "temperature": 23.50,
    "humidity": 45.20,
    "pressure": 1013.25,
}

try:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HMI_IP, PORT))
    s.sendall(json.dumps(data).encode("utf-8"))
    print("Successfully sent test sensor data to HMI server!")
except Exception as e:
  print(f"Failed to connect: {e}")