from datetime import datetime
import json
import socket
import time
from sense_hat import SenseHat

# Network configuration from your project specifications
HMI_IP = "192.168.5.92"
SENSOR_PORT = 5091  # TCP port for sensor readings

# Connect to the Sense HAT
sense = SenseHat()

print("Starting environmental monitoring and network transmission...")
print(f"Target HMI IP: {HMI_IP}:{SENSOR_PORT}")
print("Press CTRL+C to stop.\n")

try:
  while True:
    # 1. Read sensor values
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    # 2. Record the timestamp
    timestamp = datetime.now().isoformat(timespec="seconds")

    # 3. Package data into a dictionary/JSON payload
    payload = {
        "timestamp": timestamp,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "pressure": round(pressure, 2),
    }

    # 4. Display local readings
    print(f"Timestamp: {timestamp}")
    print(f"Temperature: {payload['temperature']} °C")
    print(f"Humidity: {payload['humidity']} %")
    print(f"Pressure: {payload['pressure']} hPa")

    # 5. Transmit data over TCP socket
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((HMI_IP, SENSOR_PORT))
        s.sendall(json.dumps(payload).encode("utf-8"))
        print("Status: Successfully sent to HMI Pi[cite: 1]")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
      print(f"Status: Connection failed ({e}). Retrying in 2s...")

    print("-" * 40)

    # Wait two seconds before the next reading and retry
    time.sleep(2)

except KeyboardInterrupt:
  print("\nEnvironmental monitoring stopped.")