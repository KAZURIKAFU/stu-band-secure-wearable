import csv
from datetime import datetime

def log_sensor_data(device_id, proximity_value):
    timestamp = datetime.now().isoformat()
    row = [device_id, proximity_value, timestamp]

    with open("../data/sample_logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print(f"Logged data: {row}")

if __name__ == "__main__":
    # Simulated sensor readings
    log_sensor_data("STUBAND_001", 1)
    log_sensor_data("STUBAND_001", 0)

