
import socket
import json
import time
from datetime import datetime

HMI_HOST = "192.168.5.82"
HEARTBEAT_PORT = 5092

heartbeat_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

print("Sense HAT heartbeat client starting...")
print(f"Sending heartbeats to {HMI_HOST}:{HEARTBEAT_PORT}")

try:
    while True:

        heartbeat = {
            "device": "RPiSH8",
            "status": "ALIVE",
            "timestamp": datetime.now().isoformat()
        }

        message = json.dumps(heartbeat)

        heartbeat_socket.sendto(
            message.encode("utf-8"),
            (HMI_HOST, HEARTBEAT_PORT)
        )

        print("Heartbeat sent:", heartbeat)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nHeartbeat client stopped.")

finally:
    heartbeat_socket.close()
