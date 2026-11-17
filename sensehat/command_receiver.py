
import socket
import json
from sense_hat import SenseHat

HMI_HOST = "0.0.0.0"
COMMAND_PORT = 5093

sense = SenseHat()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HMI_HOST, COMMAND_PORT))
server.listen(5)

print(f"Command receiver listening on port {COMMAND_PORT}...")

try:
    while True:
        connection, address = server.accept()

        print(f"HMI connected: {address}")

        with connection:
            reader = connection.makefile("r", encoding="utf-8")

            for line in reader:
                if not line.strip():
                    continue

                try:
                    command_data = json.loads(line)

                    command = command_data.get("command", "").upper()

                    if command == "DISPLAY":
                        message = str(command_data.get("message", "Hello"))[:80]

                        sense.show_message(
                            message,
                            scroll_speed=0.08
                        )

                        response = {
                            "status": "SUCCESS",
                            "message": f"Displayed: {message}"
                        }

                        print("Displayed message:", message)

                    elif command == "CLEAR":
                        sense.clear()

                        response = {
                            "status": "SUCCESS",
                            "message": "LED matrix cleared"
                        }

                        print("LED matrix cleared.")

                    else:
                        response = {
                            "status": "ERROR",
                            "message": "Unknown command"
                        }

                        print("Unknown command:", command)

                    connection.sendall(
                        (json.dumps(response) + "\n").encode("utf-8")
                    )

                except json.JSONDecodeError:
                    response = {
                        "status": "ERROR",
                        "message": "Invalid JSON"
                    }

                    connection.sendall(
                        (json.dumps(response) + "\n").encode("utf-8")
                    )

except KeyboardInterrupt:
    print("\nCommand receiver stopped.")

finally:
    sense.clear()
    server.close()
