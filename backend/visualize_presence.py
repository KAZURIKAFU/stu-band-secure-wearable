"""
STU-Band | visualize_presence.py
==================================
End-to-end runner: generates data → runs analysis → produces all figures.

Output figures saved to outputs/:
    fig1_presence_timeline.png   Personnel presence timeline
    fig2_zone_heatmap.png        Zone dwell time heatmap
    fig3_anomaly_summary.png     Anomaly detection bar chart
    fig4_daily_attendance.png    Daily attendance trend
    fig5_dwell_distribution.png  Dwell time box plots
    fig6_rssi_distribution.png   BLE RSSI distribution

Usage:
    python backend/visualize_presence.py

Author: Abhay Sharma | Reg. No. 229303310
Project: STU-Band, Manipal University Jaipur, 2025-26
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

from generate_data import generate_logs
from anomaly_detection import run_full_analysis

os.makedirs("outputs", exist_ok=True)

# ── Colour palette ──────────────────────────────────────────────────────────
ZONE_COLORS = {
    "ZONE_A": "#2196F3",
    "ZONE_B": "#4CAF50",
    "ZONE_C": "#FF9800",
    "ZONE_D": "#F44336",
}
SEVERITY_COLORS = {"HIGH": "#F44336", "MEDIUM": "#FF9800", "LOW": "#FFC107"}

plt.rcParams.update({
    "font.family"      : "DejaVu Sans",
    "font.size"        : 11,
    "axes.titlesize"   : 13,
    "axes.titleweight" : "bold",
    "axes.spines.top"  : False,
    "axes.spines.right": False,
    "figure.dpi"       : 150,
})


# ── Figure 1 ─────────────────────────────────────────────────────────────────
def fig1_presence_timeline(df):
    device_df = df[df["device_id"] == "STUBAND_001"].copy()
    cutoff = device_df["timestamp"].min() + pd.Timedelta(days=5)
    device_df = device_df[device_df["timestamp"] < cutoff]

    fig, ax = plt.subplots(figsize=(12, 4))
    for zone_id, color in ZONE_COLORS.items():
        z = device_df[device_df["zone_id"] == zone_id]
        if len(z):
            ax.scatter(z["timestamp"], z["proximity_status"],
                       color=color, label=zone_id, s=45, zorder=3)
    ax.plot(device_df["timestamp"], device_df["proximity_status"],
            color="#ccc", linewidth=0.8, zorder=1)

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Absent", "Present"])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Proximity Status")
    ax.set_title("Figure 1: Personnel Presence Timeline — STUBAND_001 (First 5 Days)")
    ax.legend(title="Zone", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("outputs/fig1_presence_timeline.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig1_presence_timeline.png")


# ── Figure 2 ─────────────────────────────────────────────────────────────────
def fig2_zone_heatmap(sessions):
    pivot = (sessions
             .groupby(["device_id", "zone_id"])["dwell_minutes"]
             .sum()
             .unstack(fill_value=0))

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = pivot.values[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                    fontsize=8, color="black" if v < 800 else "white")

    plt.colorbar(im, ax=ax, label="Total Dwell Time (minutes)")
    ax.set_title("Figure 2: Zone Presence Heatmap — Cumulative Dwell Time per Device (30 Days)")
    ax.set_xlabel("Zone")
    ax.set_ylabel("Device ID")
    plt.tight_layout()
    plt.savefig("outputs/fig2_zone_heatmap.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig2_zone_heatmap.png")


# ── Figure 3 ─────────────────────────────────────────────────────────────────
def fig3_anomaly_summary(anomalies):
    summary = (anomalies
               .groupby(["anomaly_type", "severity"])
               .size()
               .reset_index(name="count")
               .sort_values("count", ascending=True))

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(summary["anomaly_type"], summary["count"],
                   color=[SEVERITY_COLORS[s] for s in summary["severity"]],
                   edgecolor="white", height=0.55)

    for bar, (_, row) in zip(bars, summary.iterrows()):
        ax.text(bar.get_width() + 0.3,
                bar.get_y() + bar.get_height() / 2,
                f"  {int(row['count'])}  [{row['severity']}]",
                va="center", fontsize=10)

    ax.set_xlabel("Number of Flagged Events")
    ax.set_title("Figure 3: Anomaly Detection Results — Event Count by Rule Type")
    ax.set_xlim(0, summary["count"].max() * 1.3)
    legend_els = [Patch(facecolor=c, label=s) for s, c in SEVERITY_COLORS.items()]
    ax.legend(handles=legend_els, title="Severity", loc="lower right")
    plt.tight_layout()
    plt.savefig("outputs/fig3_anomaly_summary.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig3_anomaly_summary.png")


# ── Figure 4 ─────────────────────────────────────────────────────────────────
def fig4_daily_attendance(attendance):
    daily = attendance.groupby("date")["device_id"].nunique().reset_index()
    daily.columns = ["date", "devices_present"]
    daily["date"] = pd.to_datetime(daily["date"])

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(daily["date"], daily["devices_present"], alpha=0.25, color="#2196F3")
    ax.plot(daily["date"], daily["devices_present"],
            color="#1565C0", linewidth=2, marker="o", markersize=4)
    ax.axhline(y=daily["devices_present"].mean(), color="#F44336",
               linestyle="--", linewidth=1.5,
               label=f"Average: {daily['devices_present'].mean():.1f}")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=30)
    ax.set_xlabel("Date")
    ax.set_ylabel("Devices Present")
    ax.set_title("Figure 4: Daily Attendance Count — All Devices (30-Day Period)")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_ylim(0, 16)
    plt.tight_layout()
    plt.savefig("outputs/fig4_daily_attendance.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig4_daily_attendance.png")


# ── Figure 5 ─────────────────────────────────────────────────────────────────
def fig5_dwell_distribution(sessions):
    zone_data   = [sessions[sessions["zone_id"] == z]["dwell_minutes"].values
                   for z in ["ZONE_A", "ZONE_B", "ZONE_C", "ZONE_D"]]
    zone_labels = ["Zone A\n(Lecture Hall)", "Zone B\n(Laboratory)",
                   "Zone C\n(Library)",      "Zone D\n(Restricted)"]

    fig, ax = plt.subplots(figsize=(9, 5))
    bp = ax.boxplot(zone_data, tick_labels=zone_labels, patch_artist=True,
                    medianprops={"color": "black", "linewidth": 2})

    for patch, color in zip(bp["boxes"], ZONE_COLORS.values()):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel("Dwell Time (minutes)")
    ax.set_title("Figure 5: Dwell Time Distribution per Zone")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("outputs/fig5_dwell_distribution.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig5_dwell_distribution.png")


# ── Figure 6 ─────────────────────────────────────────────────────────────────
def fig6_rssi_distribution(sessions):
    fig, ax = plt.subplots(figsize=(10, 5))
    for zone_id, color in ZONE_COLORS.items():
        rssi = sessions[sessions["zone_id"] == zone_id]["rssi_dbm"]
        name = sessions[sessions["zone_id"] == zone_id]["zone_name"].iloc[0]
        ax.hist(rssi, bins=20, alpha=0.6, color=color,
                label=f"{zone_id} ({name})", edgecolor="white")

    ax.axvline(x=-40, color="black", linestyle="--", linewidth=1.5,
               label="RSSI Spoof Threshold (−40 dBm)")
    ax.set_xlabel("RSSI (dBm)")
    ax.set_ylabel("Frequency")
    ax.set_title("Figure 6: BLE RSSI Signal Strength Distribution per Zone")
    ax.legend(fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("outputs/fig6_rssi_distribution.png", bbox_inches="tight")
    plt.close()
    print("[+] outputs/fig6_rssi_distribution.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n[1/3] Generating dataset...")
    generate_logs()

    print("\n[2/3] Running anomaly detection...")
    df, sessions, anomalies, attendance = run_full_analysis()

    print("\n[3/3] Generating figures...")
    fig1_presence_timeline(df)
    fig2_zone_heatmap(sessions)
    fig3_anomaly_summary(anomalies)
    fig4_daily_attendance(attendance)
    fig5_dwell_distribution(sessions)
    fig6_rssi_distribution(sessions)

    print("\n" + "=" * 55)
    print("  RESULTS SUMMARY")
    print("=" * 55)
    print(f"  Log records       : {len(df)}")
    print(f"  Sessions          : {len(sessions)}")
    print(f"  Devices           : {df['device_id'].nunique()}")
    print(f"  Zones             : {df['zone_id'].nunique()}")
    print(f"  Anomalies flagged : {len(anomalies)}")
    for atype in anomalies["anomaly_type"].unique():
        n = len(anomalies[anomalies["anomaly_type"] == atype])
        print(f"    - {atype}: {n}")
    print(f"  Avg dwell time    : {sessions['dwell_minutes'].mean():.1f} min")
    print(f"  Most visited zone : {sessions.groupby('zone_id').size().idxmax()}")
    print("=" * 55)
    print("\n[✓] All outputs saved to outputs/")
