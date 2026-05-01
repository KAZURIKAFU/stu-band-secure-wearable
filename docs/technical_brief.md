# STU-Band — Technical Brief

## 1. System Overview

STU-Band is a secure, low-power wearable system for automated personnel identification and zone presence monitoring. The system targets defense training academies, restricted industrial environments, and secure campuses where reliable identity verification and audit trails are operationally critical.

The core innovation is the integration of **BLE proximity-based automatic identification** with **TEG (Thermoelectric Generator) passive energy harvesting** from body heat, enabling continuous operation without battery charging.

---

## 2. Presence Analytics

The backend processes time-stamped BLE proximity logs (device_id, zone_id, rssi_dbm, nfc_confirmed, timestamp) to:

### 2.1 Session Computation
Entry/exit event pairs are matched per device per zone. Dwell time is computed as:

```
dwell_time = exit_timestamp - entry_timestamp  (in minutes)
```

### 2.2 Anomaly Detection Rules

Five rule-based detectors are applied to all computed sessions:

| Rule | Trigger | Severity |
|------|---------|----------|
| UNAUTHORIZED_ZONE_D_ACCESS | Non-authorized device in restricted zone | HIGH |
| NFC_NOT_CONFIRMED | Zone D entry without NFC tap | HIGH |
| EXCESSIVE_DWELL_TIME | Dwell > 240 minutes | MEDIUM |
| SUSPICIOUS_SHORT_DWELL | Dwell < 1 minute | LOW |
| RSSI_SPOOF_SUSPICION | RSSI > −40 dBm | MEDIUM |

### 2.3 Daily Attendance
Devices present per day are computed from session data.  
15% natural absence rate is modelled in the simulation dataset.

---

## 3. Dataset Summary

The simulation dataset models 15 devices across 4 zones over 30 working days (December 2025):

| Metric | Value |
|--------|-------|
| Log records | 1,616 |
| Sessions | 808 |
| Anomalies flagged | 81 |
| Average dwell time | 120.4 min |
| Most visited zone | ZONE_C (Library) |

---

## 4. BLE Communication

- **Protocol:** BLE 5.0 (2.4 GHz ISM band)
- **Role:** Wearable acts as BLE peripheral (advertiser); zone readers act as centrals (scanners)
- **Advertisement interval:** 1 Hz (1000 ms)
- **Payload:** UUID-encoded device identifier (16-byte)
- **RSSI range:** −45 to −75 dBm depending on zone reader placement
- **Range:** ~5–10 metres per zone reader

---

## 5. Privacy and Security

- No raw biometric data is transmitted or stored
- Personnel ID is encrypted in the ATECC608A secure element on the wearable
- NFC provides a second-factor confirmation for restricted zones
- All session data is stored locally on the backend server (no cloud)
- Future work: AES-128-CCM encryption of BLE advertisement payloads

---

## 6. Publication

This system architecture and analytics approach have been documented in a research paper accepted at:

**ISDIA 2025 International Conference**, Sofitel Jumeirah Hotel, Dubai  
**Title:** "Energy-efficient Wearable IoT Information System for Sustainable and Privacy-Preserving Data Collection with AI-Driven Decision Support"  
**Authors:** Abhay Sharma, Dr. Gaurav Kumawat  
**Status:** Accepted — in process of publication in **Springer SCOPUS**

---

## 7. Running the Pipeline

```bash
# Step 1: Generate 30-day simulated dataset
python backend/generate_data.py

# Step 2: Run anomaly detection + compute sessions + attendance
python backend/anomaly_detection.py

# Step 3: Generate all 6 output figures
python backend/visualize_presence.py

# All steps combined (recommended):
python backend/visualize_presence.py
```

All outputs are saved to `data/` and `outputs/`.
