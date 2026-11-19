
import socket
import json

HOST = "0.0.0.0"
PORT = 5093

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"HMI command server listening on port {PORT}...")
print("Waiting for Sense HAT Pi...")

try:
    while True:
        connection, address = server.accept()
        print(f"Sense HAT connected: {address}")

        with connection:
            reader = connection.makefile("r", encoding="utf-8")

            while True:
                print("\n--- Sense HAT Commands ---")
                print("1. Change sensor reporting interval")
                print("2. Request a fresh sensor reading")
                print("3. Disconnect")

                choice = input("Choose an option: ")

                if choice == "1":
                    try:
                        interval = float(
                            input("Enter interval in seconds: ")
                        )

                        if interval <= 0:
                            print("Interval must be greater than zero.")
                            continue

                        command = {
                            "command": "SET_INTERVAL",
                            "interval": interval
                        }

                    except ValueError:
                        print("Please enter a valid number.")
                        continue

                elif choice == "2":
                    command = {
                        "command": "REQUEST_READING"
                    }

                elif choice == "3":
                    print("Sending disconnect command...")
                    command = {
                        "command": "DISCONNECT"
                    }

                else:
                    print("Invalid option.")
                    continue

                connection.sendall(
                    (json.dumps(command) + "\n").encode("utf-8")
                )

                response_line = reader.readline()

                if not response_line:
                    print("Sense HAT disconnected.")
                    break

                response = json.loads(response_line)
                print("\nResponse from Sense HAT:")
                print(json.dumps(response, indent=4))

                if command.get("command") == "DISCONNECT":
                    print("Sense HAT command client disconnected.")
                    break

except KeyboardInterrupt:
    print("\nHMI command server stopped.")

finally:
    server.close()
