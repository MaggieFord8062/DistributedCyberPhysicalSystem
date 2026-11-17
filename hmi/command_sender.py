
import socket
import json

SENSEHAT_HOST = "192.168.5.83"
COMMAND_PORT = 5093


def send_command(command, message=None):

    command_data = {
        "command": command
    }

    if message:
        command_data["message"] = message

    try:
        with socket.create_connection(
            (SENSEHAT_HOST, COMMAND_PORT),
            timeout=5
        ) as connection:

            # Send command as newline-delimited JSON
            connection.sendall(
                (json.dumps(command_data) + "\n").encode("utf-8")
            )

            # Receive response from Sense HAT Pi
            reader = connection.makefile("r", encoding="utf-8")
            response = json.loads(reader.readline())

            print("Sense HAT response:", response)

    except (ConnectionError, OSError) as error:
        print("Could not send command:", error)


if __name__ == "__main__":

    print("Sense HAT Command Sender")
    print("1. Display a message")
    print("2. Clear LED display")
    print("3. Exit")

    while True:
        choice = input("\nChoose an option: ")

        if choice == "1":
            message = input("Enter a message: ")
            send_command("DISPLAY", message)

        elif choice == "2":
            send_command("CLEAR")

        elif choice == "3":
            print("Command sender stopped.")
            break

        else:
            print("Invalid option.")
python3 command_sender.py