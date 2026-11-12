
import socket
import time
from datetime import datetime

HMI_HOST = "192.168.5.82"
HMI_PORT = 5092

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Heartbeat sender started...")

try:
    while True:
        heartbeat = f"SenseHAT,{datetime.now().isoformat()}"

        client.sendto(
            heartbeat.encode("utf-8"),
            (HMI_HOST, HMI_PORT)
        )

        print("Heartbeat sent:", heartbeat)

        time.sleep(2)

except KeyboardInterrupt:
    print("Heartbeat sender stopped.")

finally:
    client.close()
