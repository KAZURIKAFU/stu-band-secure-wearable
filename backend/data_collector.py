"""
STU-Band | data_collector.py
==============================
Real-time BLE proximity log ingestion.
Appends sensor readings to the session log and detects
entry/exit transitions for a given device.

This module simulates what the physical BLE reader node
would execute — reading RSSI advertisements and writing
timestamped proximity events to the shared CSV log.

Usage:
    python backend/data_collector.py

Author: Abhay Sharma | Reg. No. 229303310
Project: STU-Band, Manipal University Jaipur, 2025-26
"""

import csv
import os
from datetime import datetime

LOG_FILE = "data/sample_logs.csv"

FIELDNAMES = [
    "device_id", "zone_id", "zone_name",
    "proximity_status", "rssi_dbm", "nfc_confirmed", "timestamp", "is_anomaly",
]

ZONE_NAMES = {
    "ZONE_A": "Lecture Hall",
    "ZONE_B": "Laboratory",
    "ZONE_C": "Library",
    "ZONE_D": "Restricted Area",
}


def log_sensor_data(device_id, zone_id, proximity_status, rssi_dbm,
                    nfc_confirmed=1, is_anomaly=0):
    """
    Append a single BLE proximity event to the log file.

    Args:
        device_id       (str):  Wearable device identifier e.g. 'STUBAND_001'
        zone_id         (str):  Zone identifier e.g. 'ZONE_A'
        proximity_status(int):  1 = entered zone, 0 = exited zone
        rssi_dbm        (int):  BLE signal strength in dBm
        nfc_confirmed   (int):  1 = NFC tap confirmed, 0 = not confirmed
        is_anomaly      (int):  1 = flagged anomaly, 0 = normal
    """
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)
    timestamp = datetime.now().isoformat(timespec="seconds")
    zone_name = ZONE_NAMES.get(zone_id, "Unknown Zone")

    row = {
        "device_id": device_id,
        "zone_id": zone_id,
        "zone_name": zone_name,
        "proximity_status": proximity_status,
        "rssi_dbm": rssi_dbm,
        "nfc_confirmed": nfc_confirmed,
        "timestamp": timestamp,
        "is_anomaly": is_anomaly,
    }

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    status_str = "ENTERED" if proximity_status == 1 else "EXITED"
    flag = " [ANOMALY]" if is_anomaly else ""
    print(f"[{timestamp}] {device_id} {status_str} {zone_id} | RSSI: {rssi_dbm} dBm{flag}")
    return row


def analyze_presence(device_id, log_file=LOG_FILE):
    """
    Read the log file and compute entry/exit timestamps
    for a specific device by detecting 0→1 and 1→0 transitions.

    Returns:
        entries (list): Timestamps when device entered a zone
        exits   (list): Timestamps when device exited a zone
    """
    entries = []
    exits = []

    if not os.path.isfile(log_file):
        print(f"[!] Log file not found: {log_file}")
        return entries, exits

    with open(log_file, "r") as f:
        reader = csv.DictReader(f)
        last_state = None

        for row in reader:
            if row["device_id"] != device_id:
                continue

            state = row["proximity_status"]
            time = row["timestamp"]
            zone = row.get("zone_id", "UNKNOWN")

            if last_state == "0" and state == "1":
                entries.append((time, zone))
            elif last_state == "1" and state == "0":
                exits.append((time, zone))

            last_state = state

    return entries, exits


if __name__ == "__main__":
    print("=" * 50)
    print("  STU-Band | Data Collector — Live Demo")
    print("=" * 50)

    # Simulate a sequence of real-time BLE events
    print("\n[*] Simulating live BLE events...\n")

    log_sensor_data("STUBAND_001", "ZONE_A", 1, -52)   # Enter Lecture Hall
    log_sensor_data("STUBAND_001", "ZONE_A", 0, -52)   # Exit  Lecture Hall
    log_sensor_data("STUBAND_001", "ZONE_B", 1, -61)   # Enter Lab
    log_sensor_data("STUBAND_001", "ZONE_B", 0, -61)   # Exit  Lab
    log_sensor_data("STUBAND_007", "ZONE_D", 1, -55, nfc_confirmed=0, is_anomaly=1)  # Unauthorized

    print("\n[*] Analyzing presence for STUBAND_001...")
    entries, exits = analyze_presence("STUBAND_001")

    print(f"\n  Entry events ({len(entries)}):")
    for t, z in entries:
        print(f"    {t}  →  {z}")

    print(f"\n  Exit events ({len(exits)}):")
    for t, z in exits:
        print(f"    {t}  →  {z}")
