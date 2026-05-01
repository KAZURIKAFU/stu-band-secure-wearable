# STU-Band Hardware Components

## Wearable Band — Component Specifications

| Component | Part / Spec | Purpose |
|-----------|------------|---------|
| Microcontroller (SoC) | Nordic nRF52840 | BLE 5.0 + NFC, ARM Cortex-M4 @ 64 MHz, 256 KB SRAM, 1 MB Flash |
| BLE Module | Integrated in nRF52840 | 2.4 GHz advertisement at 1 Hz duty cycle, ~0.3 mW avg power |
| NFC Tag | Integrated in nRF52840 (13.56 MHz) | Passive NFC Type 2 tag for secure identity confirmation |
| TEG Module | Bi₂Te₃ Thermoelectric Generator | Harvests body heat; ΔT ≈ 3°C → ~1.0 mW output under matched load |
| Boost Converter | TI TPS61099 | Steps up TEG output (0.3–0.8 V) to stable 3.3 V rail |
| Secure Element | Microchip ATECC608A | Encrypted personnel ID storage and attestation |
| Form Factor | Wristband / Badge | Wearable, low-profile, field-deployable |

---

## Zone Reader Node — Component Specifications

| Component | Spec | Purpose |
|-----------|------|---------|
| BLE Scanner | nRF52840 DK or RPi + BLE HAT | Scans for wearable advertisements; logs RSSI + UUID |
| NFC Reader | PN532 module (13.56 MHz) | Reads NFC tap for Zone D two-factor confirmation |
| MCU / SBC | Raspberry Pi 4 (per zone) | Runs data_collector.py; writes to shared CSV log |
| Network | LAN / Wi-Fi | Syncs zone logs to backend server |

---

## Design Considerations

- **Ultra-low power operation:** TEG harvesting sustains BLE beacon without a primary battery in steady state
- **Passive NFC tag:** Zero active power draw on the wearable for NFC reads
- **No cloud dependency:** All inference runs on-device; only session metadata is logged
- **Field deployability:** Wristband form factor, no charging required during normal wear
- **Minimal infrastructure:** Only one reader node per zone required

---

## Energy Budget (Estimated)

| Component | Current Draw | Duty Cycle | Average Power |
|-----------|-------------|------------|--------------|
| BLE advertisement | 7 mA | 0.5% (1 Hz, 10 ms tx) | ~0.035 mW |
| MCU active (inference) | 6 mA | ~5% | ~0.3 mW |
| MCU sleep | 2 µA | ~95% | ~0.006 mW |
| **Total estimated** | — | — | **~0.34 mW** |
| **TEG harvest (ΔT=3°C)** | — | continuous | **~1.0 mW** |

TEG output exceeds system demand at steady state → **net energy positive operation** during continuous wear.

---

## Future Hardware Additions

- AES-128-CCM hardware encryption (nRF52840 CCM peripheral)
- MEMS IMU for motion-based presence validation
- e-Paper display for zone entry confirmation feedback
