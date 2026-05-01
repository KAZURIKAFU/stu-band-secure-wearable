"""
STU-Band | generate_data.py
============================
Generates a realistic multi-device, multi-zone BLE proximity dataset
simulating 15 personnel wearables across 4 monitored zones over 30 days.

Zones:
    ZONE_A  Lecture Hall
    ZONE_B  Laboratory
    ZONE_C  Library
    ZONE_D  Restricted Area (requires NFC confirmation)

Output:
    data/session_logs.csv  — raw BLE proximity log entries

Usage:
    python backend/generate_data.py

Author: Abhay Sharma | Reg. No. 229303310
Project: STU-Band, Manipal University Jaipur, 2025-26
"""

import csv
import random
import os
from datetime import datetime, timedelta

OUTPUT_FILE = "data/session_logs.csv"

DEVICES = [
    "STUBAND_001", "STUBAND_002", "STUBAND_003", "STUBAND_004", "STUBAND_005",
    "STUBAND_006", "STUBAND_007", "STUBAND_008", "STUBAND_009", "STUBAND_010",
    "STUBAND_011", "STUBAND_012", "STUBAND_013", "STUBAND_014", "STUBAND_015",
]

ZONES = {
    "ZONE_A": "Lecture Hall",
    "ZONE_B": "Laboratory",
    "ZONE_C": "Library",
    "ZONE_D": "Restricted Area",
}

# Devices authorized for Zone D (restricted access)
ZONE_D_AUTHORIZED = {"STUBAND_001", "STUBAND_002", "STUBAND_003"}

# Realistic RSSI ranges per zone (dBm) based on expected reader distances
RSSI_RANGE = {
    "ZONE_A": (-60, -45),
    "ZONE_B": (-70, -50),
    "ZONE_C": (-75, -55),
    "ZONE_D": (-65, -48),
}


def generate_logs(num_days=30, seed=42):
    """
    Generate BLE proximity logs for all devices over num_days.
    Injects realistic anomalies:
      - 15% daily absence rate per device
      - 8% chance of excessive dwell (>4 hours)
      - 10% chance of unauthorized Zone D access for non-authorized devices
    """
    random.seed(seed)
    os.makedirs("data", exist_ok=True)

    rows = []
    start_date = datetime(2025, 12, 1, 8, 0, 0)

    for day_offset in range(num_days):
        day_start = start_date + timedelta(days=day_offset)

        # Skip Sundays
        if day_start.weekday() == 6:
            continue

        for device_id in DEVICES:
            # 15% chance of absence on any given day
            if random.random() < 0.15:
                continue

            zones_today = random.sample(list(ZONES.keys()), k=random.randint(2, 4))
            current_time = day_start + timedelta(minutes=random.randint(0, 30))

            for zone_id in zones_today:
                rssi_lo, rssi_hi = RSSI_RANGE[zone_id]
                rssi = random.randint(rssi_lo, rssi_hi)

                # Handle Zone D access control
                is_anomaly = False
                if zone_id == "ZONE_D" and device_id not in ZONE_D_AUTHORIZED:
                    if random.random() > 0.90:
                        # 10% of non-authorized devices breach Zone D — anomaly
                        is_anomaly = True
                    else:
                        # Skip Zone D for this device today
                        continue

                nfc_confirmed = (
                    1 if (zone_id != "ZONE_D" or device_id in ZONE_D_AUTHORIZED) else 0
                )

                # Dwell time: normal 20–180 min, or excessive >240 min (8% chance)
                if random.random() < 0.08:
                    dwell_minutes = random.randint(260, 360)
                else:
                    dwell_minutes = random.randint(20, 180)

                entry_time = current_time
                exit_time = current_time + timedelta(minutes=dwell_minutes)

                # Entry event
                rows.append({
                    "device_id": device_id,
                    "zone_id": zone_id,
                    "zone_name": ZONES[zone_id],
                    "proximity_status": 1,
                    "rssi_dbm": rssi,
                    "nfc_confirmed": nfc_confirmed,
                    "timestamp": entry_time.isoformat(),
                    "is_anomaly": int(is_anomaly),
                })

                # Exit event
                rows.append({
                    "device_id": device_id,
                    "zone_id": zone_id,
                    "zone_name": ZONES[zone_id],
                    "proximity_status": 0,
                    "rssi_dbm": rssi,
                    "nfc_confirmed": nfc_confirmed,
                    "timestamp": exit_time.isoformat(),
                    "is_anomaly": int(is_anomaly),
                })

                current_time = exit_time + timedelta(minutes=random.randint(5, 30))

    rows.sort(key=lambda r: r["timestamp"])

    fieldnames = [
        "device_id", "zone_id", "zone_name", "proximity_status",
        "rssi_dbm", "nfc_confirmed", "timestamp", "is_anomaly",
    ]

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Generated {len(rows)} records | {num_days} days | {len(DEVICES)} devices")
    print(f"[+] Saved to: {OUTPUT_FILE}")
    return rows


if __name__ == "__main__":
    generate_logs()
