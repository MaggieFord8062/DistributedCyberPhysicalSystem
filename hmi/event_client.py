import socket
import json
import time

SENSEHAT_HOST = "192.168.5.83"
EVENT_PORT = 5094

print("HMI event client starting...")

while True:
    try:
        print(f"Connecting to Sense HAT at {SENSEHAT_HOST}:{EVENT_PORT}...")

        with socket.create_connection(
            (SENSEHAT_HOST, EVENT_PORT), timeout=10
        ) as connection:

            connection.settimeout(None)

            print("Connected to Sense HAT event server!")

            reader = connection.makefile("r", encoding="utf-8")

            for line in reader:
                if not line.strip():
                    continue

                event = json.loads(line)

                print("\n--- RECEIVED SENSOR EVENT ---")
                print(f"Timestamp: {event.get('timestamp')}")
                print(f"Event: {event.get('event')}")
                print(f"Details: {event.get('details')}")

    except (ConnectionError, OSError) as error:
        print(f"Event connection unavailable: {error}")

    except json.JSONDecodeError as error:
        print(f"Invalid event received: {error}")

    print("Retrying connection in 3 seconds...")
    time.sleep(3)