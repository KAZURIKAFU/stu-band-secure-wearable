# STU-Band: Secure Low-Power Wearable for Personnel Monitoring

> Final Year B.Tech Major Project — Data Science and Engineering  
> Manipal University Jaipur | Academic Year 2025–26

---

## Overview

STU-Band is a low-power wearable system designed for **secure personnel identification and zone presence monitoring** in defense training academies, restricted industrial environments, and secure campuses.

The system uses **BLE (Bluetooth Low Energy)** proximity sensing to automatically log personnel entry and exit events across monitored zones, and applies a **rule-based anomaly detection pipeline** to flag unauthorized access, excessive dwell times, and irregular movement patterns — all without manual intervention.

---

## Problem Statement

Manual and card-based attendance systems in large campuses and defense facilities are vulnerable to:
- **Proxy attendance** and identity fraud
- **Scalability failures** across hundreds of personnel
- **Power constraints** limiting continuous wearable operation
- **No real-time anomaly alerting** for zone violations

---

## Solution

STU-Band automates personnel monitoring via a wearable BLE beacon that continuously broadcasts a unique device identifier. Fixed zone readers log presence events to a backend pipeline that computes sessions, detects anomalies, and produces analytics reports.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  STU-Band Wearable                       │
│   [TEG Energy Harvester] → [MCU] → [BLE Beacon / NFC]  │
└──────────────────────┬──────────────────────────────────┘
                       │ BLE Advertisement (1 Hz)
              ┌────────▼────────┐
              │  Zone Readers   │  (ZONE_A / B / C / D)
              └────────┬────────┘
                       │ Proximity Logs (CSV)
              ┌────────▼────────┐
              │ Backend Pipeline│
              │ generate_data   │
              │ data_collector  │
              │ anomaly_detect  │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Visualizations │
              │  + Reports      │
              └─────────────────┘
```

See `architecture/system_architecture.jpg` for the full block diagram.

---

## Repository Structure

```
stu-band-secure-wearable/
│
├── backend/
│   ├── generate_data.py        # Simulated multi-device presence dataset generator
│   ├── data_collector.py       # Real-time BLE log ingestion and entry/exit detection
│   └── anomaly_detection.py    # Rule-based anomaly detection engine
│
├── data/
│   ├── sample_logs.csv         # Raw BLE proximity log (sample — 50 records)
│   ├── session_logs.csv        # Full simulated dataset (1,616 records, 30 days)
│   ├── sessions.csv            # Computed session pairs with dwell times
│   ├── anomaly_report.csv      # Flagged anomaly events with descriptions
│   └── attendance_summary.csv  # Daily attendance per device
│
├── outputs/
│   ├── fig1_presence_timeline.png   # Personnel presence timeline (STUBAND_001)
│   ├── fig2_zone_heatmap.png        # Zone dwell time heatmap (all devices)
│   ├── fig3_anomaly_summary.png     # Anomaly detection bar chart
│   ├── fig4_daily_attendance.png    # Daily attendance trend (30 days)
│   ├── fig5_dwell_distribution.png  # Dwell time box plots per zone
│   └── fig6_rssi_distribution.png   # BLE RSSI distribution per zone
│
├── architecture/
│   └── system_architecture.jpg     # Hardware + software block diagram
│
├── hardware/
│   └── components.md               # BLE module, MCU, TEG, NFC specs
│
├── docs/
│   ├── technical_brief.md          # System design and analytics description
│   └── project_report.pdf          # Full B.Tech project report (submitted)
│
├── demo/
│   └── demo_notes.md               # How to run the demo end-to-end
│
├── index.html                      # Edge Intelligence Dashboard (browser-based)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Programming | Python 3.11 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| Communication | BLE 5.0, NFC |
| Hardware (planned) | nRF52840 SoC, Bi₂Te₃ TEG, ATECC608A |
| Dashboard | HTML5, JavaScript (Canvas API) |
| Version Control | Git, GitHub |

---

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total log records | 1,616 |
| Computed sessions | 808 |
| Devices monitored | 15 |
| Zones monitored | 4 |
| Days simulated | 30 |
| Total anomalies flagged | 81 |
| — Excessive dwell time | 74 (MEDIUM) |
| — Unauthorized Zone D access | 7 (HIGH) |
| Average session dwell time | 120.4 minutes |

---

## Anomaly Detection Rules

| Rule | Severity | Trigger Condition |
|------|----------|------------------|
| UNAUTHORIZED_ZONE_D_ACCESS | HIGH | Non-authorized device detected in restricted zone |
| NFC_NOT_CONFIRMED | HIGH | Authorized device enters Zone D without NFC tap |
| EXCESSIVE_DWELL_TIME | MEDIUM | Session dwell > 240 minutes |
| SUSPICIOUS_SHORT_DWELL | LOW | Session dwell < 1 minute (relay attack indicator) |
| RSSI_SPOOF_SUSPICION | MEDIUM | RSSI > −40 dBm (abnormally strong signal) |

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/KAZURIKAFU/stu-band-secure-wearable.git
cd stu-band-secure-wearable

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset
python backend/generate_data.py

# 4. Run anomaly detection
python backend/anomaly_detection.py

# 5. Generate all visualizations
python backend/visualize_presence.py

# 6. Open dashboard
open index.html   # or double-click in file explorer
```

---

## Output Figures

| Figure | Description |
|--------|-------------|
| Fig 1 | Personnel presence timeline — STUBAND_001, first 5 days |
| Fig 2 | Zone presence heatmap — cumulative dwell per device (30 days) |
| Fig 3 | Anomaly detection summary — event count by rule type |
| Fig 4 | Daily attendance count — all 15 devices over 30 days |
| Fig 5 | Dwell time distribution — box plots per zone |
| Fig 6 | BLE RSSI distribution — signal strength per zone |

---

## Publication

This project has been submitted as a research paper titled:

> **"Energy-efficient Wearable IoT Information System for Sustainable and Privacy-Preserving Data Collection with AI-Driven Decision Support"**

**Authors:** Abhay Sharma, Dr. Gaurav Kumawat  
**Conference:** ISDIA 2025, Sofitel Jumeirah Hotel, Dubai  
**Status:** Accepted — In process of publication in **Springer SCOPUS**

---

## Current Status

- [x] System architecture finalized
- [x] Backend data pipeline implemented
- [x] Anomaly detection engine implemented  
- [x] All visualizations generated from real data
- [x] Edge intelligence dashboard (browser-based)
- [x] Research paper accepted (Springer SCOPUS)
- [ ] Hardware prototype (planned — future work)
- [ ] Encrypted BLE communication (planned)
- [ ] Command-center dashboard integration (planned)

---

## Future Enhancements

1. Physical hardware prototype with Nordic nRF52840 + TEG integration
2. AES-128-CCM encrypted BLE advertisement payloads
3. Federated learning across multiple wearable devices
4. Real-time command-center dashboard with map-based zone visualization
5. Integration with OSDP-compliant access control systems

---

## Author

**Abhay Sharma**  
Final Year B.Tech — Data Science and Engineering (Batch 2022–26)  
Registration No.: 229303310  
Manipal University Jaipur

---

## License

This project is submitted as academic work for Manipal University Jaipur.  
© 2026 Abhay Sharma. All rights reserved.
