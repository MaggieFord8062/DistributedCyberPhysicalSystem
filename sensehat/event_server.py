
import socket
import json
import threading
from datetime import datetime

HOST = "0.0.0.0"
TCP_PORT = 5094
UDP_PORT = 5095

# Stores the current HMI connection
hmi_connection = None
connection_lock = threading.Lock()


def send_to_hmi(event):
    """Forward an event to the connected HMI."""
    global hmi_connection

    message = json.dumps(event) + "\n"

    with connection_lock:
        if hmi_connection is None:
            print("No HMI connected. Event not forwarded:", event["event"])
            return

        try:
            hmi_connection.sendall(message.encode("utf-8"))
            print("Forwarded event to HMI:", event)

        except OSError as error:
            print("Could not send event to HMI:", error)
            hmi_connection = None


def receive_local_events():
    """Receive events from sensor_server.py over local UDP."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind(("127.0.0.1", UDP_PORT))

    print(f"Listening for local sensor events on UDP port {UDP_PORT}...")

    while True:
        message, address = udp_socket.recvfrom(4096)

        try:
            event = json.loads(message.decode("utf-8"))
            print("Received local event:", event)
            send_to_hmi(event)

        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            print("Invalid local event:", error)


# Start the local UDP event receiver in the background
udp_thread = threading.Thread(
    target=receive_local_events,
    daemon=True
)
udp_thread.start()

# Start the TCP event server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, TCP_PORT))
server.listen(1)

print(f"Event server listening on TCP port {TCP_PORT}...")
print("Waiting for HMI connection...")

try:
    while True:
        connection, address = server.accept()

        with connection_lock:
            hmi_connection = connection

        print(f"HMI connected: {address}")

        # Notify HMI that event communication is established
        startup_event = {
            "timestamp": datetime.now().isoformat(),
            "event": "SENSOR_SERVER_CONNECTED",
            "details": "Sense HAT event communication established."
        }

        send_to_hmi(startup_event)

except KeyboardInterrupt:
    print("\nEvent server stopped.")

finally:
    server.close()
