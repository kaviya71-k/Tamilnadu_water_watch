import sqlite3
import pandas as pd

conn = sqlite3.connect("chennai_water.db")
df = pd.read_sql("SELECT * FROM live_reservoir_snapshots", conn)
conn.close()

# Keep only the latest date's data, and remove duplicates
latest_date = df["Date_Collected"].max()
latest = df[df["Date_Collected"] == latest_date]
latest = latest.drop_duplicates(subset=["Reservoirs"])

# Calculate percentage full
latest["Percent_Full"] = (latest["Current Year Storage (M.Cft.)"] / latest["Full Capacity (M.Cft.)"]) * 100

# Define a function that converts percentage into a risk category
def get_risk_level(pct):
    if pct >= 50:
        return "Safe"
    elif pct >= 20:
        return "Watch"
    else:
        return "Critical"

# Apply that function to every row
latest["Risk_Level"] = latest["Percent_Full"].apply(get_risk_level)

# Sort by percentage, lowest (most critical) first
latest = latest.sort_values("Percent_Full")

print(latest[["Reservoirs", "Percent_Full", "Risk_Level"]].to_string(index=False))