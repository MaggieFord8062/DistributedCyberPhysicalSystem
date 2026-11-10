
from sense_hat import SenseHat
from datetime import datetime
import time

# Connect to the Sense HAT
sense = SenseHat()

print("Starting environmental monitoring...")
print("Press CTRL+C to stop.\n")

try:
    while True:
        # Read sensor values
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()

        # Record the timestamp
        timestamp = datetime.now().isoformat(timespec="seconds")

        # Display the readings
        print(f"Timestamp: {timestamp}")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Pressure: {pressure:.2f} hPa")
        print("-" * 40)

        # Wait one second before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("\nEnvironmental monitoring stopped.")
