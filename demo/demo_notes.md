# STU-Band — Demo Notes

## Prerequisites

```bash
pip install -r requirements.txt
# Requires: pandas, numpy, matplotlib
```

---

## Running the Full Demo

From the root of the repository:

```bash
python backend/visualize_presence.py
```

This single command:
1. Generates 1,616 BLE proximity log records for 15 devices across 4 zones over 30 days
2. Computes 808 entry/exit sessions with dwell times
3. Runs all 5 anomaly detection rules — flags 81 events
4. Saves 6 publication-quality figures to `outputs/`
5. Prints the full results summary to the terminal

---

## Running Individual Steps

```bash
# Generate data only
python backend/generate_data.py

# Run anomaly detection only (requires session_logs.csv to exist)
python backend/anomaly_detection.py

# Simulate live BLE data collection
python backend/data_collector.py
```

---

## Opening the Dashboard

Open `index.html` in any modern browser (Chrome, Firefox, Edge).  
No server required. The dashboard runs entirely in the browser.

---

## Expected Terminal Output

```
[1/3] Generating dataset...
[+] Generated 1616 records | 30 days | 15 devices
[+] Saved to: data/session_logs.csv

[2/3] Running anomaly detection...
=======================================================
  STU-Band | Presence Analytics Engine
=======================================================
  Log records  : 1616
  Devices      : 15
  Zones        : 4
  Date range   : 2025-12-01 → 2025-12-30
  Sessions computed : 808
  Anomalies detected : 81
    [MEDIUM]  EXCESSIVE_DWELL_TIME: 74
    [HIGH  ]  UNAUTHORIZED_ZONE_D_ACCESS: 7

[3/3] Generating figures...
[+] outputs/fig1_presence_timeline.png
[+] outputs/fig2_zone_heatmap.png
[+] outputs/fig3_anomaly_summary.png
[+] outputs/fig4_daily_attendance.png
[+] outputs/fig5_dwell_distribution.png
[+] outputs/fig6_rssi_distribution.png

=======================================================
  RESULTS SUMMARY
  Log records       : 1616
  Sessions          : 808
  Devices           : 15
  Anomalies flagged : 81
  Avg dwell time    : 120.4 min
  Most visited zone : ZONE_C
=======================================================
[✓] All outputs saved to outputs/
```

---

## Data Files Generated

| File | Description |
|------|-------------|
| `data/session_logs.csv` | Raw BLE proximity log (1,616 records) |
| `data/sessions.csv` | Computed sessions with dwell times (808 rows) |
| `data/anomaly_report.csv` | Flagged anomaly events with descriptions |
| `data/attendance_summary.csv` | Daily attendance per device |
