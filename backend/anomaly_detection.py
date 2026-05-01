"""
STU-Band | anomaly_detection.py
=================================
Rule-based anomaly detection engine for BLE presence logs.

Detects the following anomaly types:
    UNAUTHORIZED_ZONE_D_ACCESS   — non-authorized device in restricted zone
    NFC_NOT_CONFIRMED            — authorized device entered Zone D without NFC
    EXCESSIVE_DWELL_TIME         — session duration exceeded threshold (240 min)
    SUSPICIOUS_SHORT_DWELL       — session duration under 1 minute (relay attack)
    RSSI_SPOOF_SUSPICION         — abnormally strong BLE signal (>-40 dBm)

Inputs:
    data/session_logs.csv

Outputs:
    data/sessions.csv            — computed session pairs with dwell times
    data/anomaly_report.csv      — all flagged events with descriptions
    data/attendance_summary.csv  — daily attendance per device

Usage:
    python backend/anomaly_detection.py

Author: Abhay Sharma | Reg. No. 229303310
Project: STU-Band, Manipal University Jaipur, 2025-26
"""

import pandas as pd
import os

LOG_FILE       = "data/session_logs.csv"
SESSION_FILE   = "data/sessions.csv"
ANOMALY_FILE   = "data/anomaly_report.csv"
ATTENDANCE_FILE= "data/attendance_summary.csv"

ZONE_D_AUTHORIZED   = {"STUBAND_001", "STUBAND_002", "STUBAND_003"}
MAX_DWELL_MINUTES   = 240    # 4 hours
MIN_DWELL_MINUTES   = 1      # 1 minute
RSSI_SPOOF_THRESHOLD= -40    # dBm


def load_logs(filepath=LOG_FILE):
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp").reset_index(drop=True)


def compute_sessions(df):
    """
    Pair each ENTRY (proximity_status=1) with the next EXIT (proximity_status=0)
    for the same device + zone to compute session dwell time.
    """
    sessions = []

    for (device_id, zone_id), group in df.groupby(["device_id", "zone_id"]):
        group = group.sort_values("timestamp").reset_index(drop=True)
        i = 0
        while i < len(group) - 1:
            row      = group.iloc[i]
            next_row = group.iloc[i + 1]
            if row["proximity_status"] == 1 and next_row["proximity_status"] == 0:
                dwell = (next_row["timestamp"] - row["timestamp"]).total_seconds() / 60
                sessions.append({
                    "device_id"    : device_id,
                    "zone_id"      : zone_id,
                    "zone_name"    : row["zone_name"],
                    "entry_time"   : row["timestamp"],
                    "exit_time"    : next_row["timestamp"],
                    "dwell_minutes": round(dwell, 1),
                    "rssi_dbm"     : row["rssi_dbm"],
                    "nfc_confirmed": row["nfc_confirmed"],
                    "date"         : row["timestamp"].date(),
                })
                i += 2
            else:
                i += 1

    return pd.DataFrame(sessions)


def detect_anomalies(sessions_df):
    """Apply all five detection rules. Returns DataFrame of flagged events."""
    anomalies = []

    for _, row in sessions_df.iterrows():

        # Rule 1: Unauthorized Zone D access
        if row["zone_id"] == "ZONE_D" and row["device_id"] not in ZONE_D_AUTHORIZED:
            anomalies.append({**row,
                "anomaly_type": "UNAUTHORIZED_ZONE_D_ACCESS",
                "severity"    : "HIGH",
                "description" : f"{row['device_id']} accessed Restricted Area without authorization.",
            })

        # Rule 2: Authorized device entered Zone D but NFC not confirmed
        elif row["zone_id"] == "ZONE_D" and row["nfc_confirmed"] == 0:
            anomalies.append({**row,
                "anomaly_type": "NFC_NOT_CONFIRMED",
                "severity"    : "HIGH",
                "description" : f"{row['device_id']} entered Zone D — NFC confirmation missing.",
            })

        # Rule 3: Excessive dwell time
        if row["dwell_minutes"] > MAX_DWELL_MINUTES:
            anomalies.append({**row,
                "anomaly_type": "EXCESSIVE_DWELL_TIME",
                "severity"    : "MEDIUM",
                "description" : (
                    f"{row['device_id']} in {row['zone_name']} for "
                    f"{row['dwell_minutes']:.0f} min (limit: {MAX_DWELL_MINUTES} min)."
                ),
            })

        # Rule 4: Suspiciously short dwell (possible badge relay)
        if row["dwell_minutes"] < MIN_DWELL_MINUTES:
            anomalies.append({**row,
                "anomaly_type": "SUSPICIOUS_SHORT_DWELL",
                "severity"    : "LOW",
                "description" : (
                    f"{row['device_id']} was in {row['zone_name']} "
                    f"for only {row['dwell_minutes']:.1f} min."
                ),
            })

        # Rule 5: RSSI spoofing suspicion
        if row["rssi_dbm"] > RSSI_SPOOF_THRESHOLD:
            anomalies.append({**row,
                "anomaly_type": "RSSI_SPOOF_SUSPICION",
                "severity"    : "MEDIUM",
                "description" : (
                    f"{row['device_id']} had abnormally strong RSSI "
                    f"({row['rssi_dbm']} dBm) in {row['zone_name']}."
                ),
            })

    return pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


def compute_daily_attendance(sessions_df):
    return sessions_df.groupby(["date", "device_id"]).agg(
        total_dwell_minutes=("dwell_minutes", "sum"),
        zones_visited=("zone_id",       "nunique"),
        sessions=("dwell_minutes",       "count"),
    ).reset_index()


def run_full_analysis(filepath=LOG_FILE):
    os.makedirs("data", exist_ok=True)

    print("=" * 55)
    print("  STU-Band | Presence Analytics Engine")
    print("=" * 55)

    df = load_logs(filepath)
    print(f"\n  Log records  : {len(df)}")
    print(f"  Devices      : {df['device_id'].nunique()}")
    print(f"  Zones        : {df['zone_id'].nunique()}")
    print(f"  Date range   : {df['timestamp'].min().date()} → {df['timestamp'].max().date()}")

    sessions = compute_sessions(df)
    sessions.to_csv(SESSION_FILE, index=False)
    print(f"\n  Sessions computed : {len(sessions)}")
    print(f"  Saved → {SESSION_FILE}")

    anomalies = detect_anomalies(sessions)
    if len(anomalies) > 0:
        summary = anomalies.groupby(["anomaly_type", "severity"]).size().reset_index(name="count")
        print(f"\n  Anomalies detected : {len(anomalies)}")
        for _, row in summary.iterrows():
            print(f"    [{row['severity']:6}]  {row['anomaly_type']}: {row['count']}")
        anomalies.to_csv(ANOMALY_FILE, index=False)
        print(f"  Saved → {ANOMALY_FILE}")
    else:
        print("\n  No anomalies detected.")

    attendance = compute_daily_attendance(sessions)
    attendance.to_csv(ATTENDANCE_FILE, index=False)
    print(f"\n  Attendance summary saved → {ATTENDANCE_FILE}")
    print("=" * 55)

    return df, sessions, anomalies, attendance


if __name__ == "__main__":
    run_full_analysis()
