import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "../data/sample_logs.csv"

df = pd.read_csv(LOG_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

device_df = df[df["device_id"] == "STUBAND_001"]

plt.figure()
plt.plot(device_df["timestamp"], device_df["proximity_status"], marker="o")
plt.xlabel("Time")
plt.ylabel("Proximity Status (1 = Present, 0 = Absent)")
plt.title("Personnel Presence Timeline")

plt.show()
