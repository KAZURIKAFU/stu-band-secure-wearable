# System Architecture

This folder contains the STU-Band system architecture diagram.

## system_architecture.jpg

The block diagram illustrates the full system stack:

```
┌─────────────────────────────────────────────────────────────┐
│                     WEARABLE LAYER                          │
│                                                             │
│   [Body Heat] → [TEG Array] → [Boost Converter 3.3V]       │
│                                    ↓                        │
│              [ATECC608A Secure Element]                     │
│                    ↓ (Encrypted ID)                         │
│   [nRF52840 SoC] ←→ [BLE 5.0 Beacon] + [NFC Tag]          │
└──────────────────────────┬──────────────────────────────────┘
                           │ BLE Advertisement (1 Hz)
              ┌────────────▼────────────┐
              │     ZONE READER LAYER   │
              │                         │
              │  ZONE_A   ZONE_B        │
              │  ZONE_C   ZONE_D (NFC)  │
              └────────────┬────────────┘
                           │ CSV Proximity Logs
              ┌────────────▼────────────┐
              │     BACKEND PIPELINE    │
              │                         │
              │  generate_data.py       │
              │  data_collector.py      │
              │  anomaly_detection.py   │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  ANALYTICS + OUTPUTS    │
              │                         │
              │  visualize_presence.py  │
              │  6 output figures       │
              │  anomaly_report.csv     │
              │  attendance_summary.csv │
              └─────────────────────────┘
```

## Zones

| Zone ID | Zone Name | Access Level |
|---------|-----------|-------------|
| ZONE_A | Lecture Hall | Open |
| ZONE_B | Laboratory | Open |
| ZONE_C | Library | Open |
| ZONE_D | Restricted Area | Authorized + NFC required |
