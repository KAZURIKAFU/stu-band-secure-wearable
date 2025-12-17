import csv
from datetime import datetime

LOG_FILE = "../data/sample_logs.csv"

def log_sensor_data(device_id, proximity_value):
    timestamp = datetime.now().isoformat()
    row = [device_id, proximity_value, timestamp]

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print(f"Logged data: {row}")

def analyze_presence(device_id):
    entries = []
    exits = []

    with open(LOG_FILE, "r") as file:
        reader = csv.DictReader(file)
        last_state = None

        for row in reader:
            if row["device_id"] == device_id:
                state = row["proximity_status"]
                time = row["timestamp"]

                if last_state == "0" and state == "1":
                    entries.append(time)
                if last_state == "1" and state == "0":
                    exits.append(time)

                last_state = state

    return entries, exits

if __name__ == "__main__":
    # Simulated sensor data
    log_sensor_data("STUBAND_001", "1")
    log_sensor_data("STUBAND_001", "0")
    log_sensor_data("STUBAND_001", "1")

    entries, exits = analyze_presence("STUBAND_001")

    print("Entry events:", entries)
    print("Exit events:", exits)
