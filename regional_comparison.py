import sqlite3
import pandas as pd

conn = sqlite3.connect("chennai_water.db")
df = pd.read_sql("SELECT * FROM live_reservoir_snapshots", conn)
conn.close()

latest_date = df["Date_Collected"].max()
latest = df[df["Date_Collected"] == latest_date]
latest = latest.drop_duplicates(subset=["Reservoirs"])

# Clean up irregular whitespace in reservoir names before matching
latest["Reservoirs"] = latest["Reservoirs"].str.strip().str.replace(r"\s+", " ", regex=True)

latest["Percent_Full"] = (latest["Current Year Storage (M.Cft.)"] / latest["Full Capacity (M.Cft.)"]) * 100

def get_risk_level(pct):
    if pct >= 50:
        return "Safe"
    elif pct >= 20:
        return "Watch"
    else:
        return "Critical"

latest["Risk_Level"] = latest["Percent_Full"].apply(get_risk_level)

# Map each reservoir to its river basin (grouping by hydrology, not just district)
basin_map = {
    "METTUR": "Cauvery Basin",
    "Krishna Raja Sagar": "Cauvery Basin",
    "Kabini": "Cauvery Basin",
    "Harangi": "Cauvery Basin",
    "Hemavathy": "Cauvery Basin",
    "BHAVANISAGAR": "Cauvery Basin",
    "Vaigai": "Vaigai Basin",
    "Periyar**": "Vaigai Basin",
    "Papanasam (TN EB Dam)": "Tamiraparani Basin",
    "Manimuthar": "Tamiraparani Basin",
    "Parambikulam": "PAP Basin",
    "Aliyar": "PAP Basin",
    "Thirumurthy": "PAP Basin",
    "Sholayar": "PAP Basin",
    "AMARAVATHI*": "PAP Basin",
    "Pechiparai": "Kanyakumari Basin",
    "Perunchani": "Kanyakumari Basin",
    "Krishnagiri": "Pennaiyar Basin",
    "Sathanur": "Pennaiyar Basin",
}

latest["Basin"] = latest["Reservoirs"].map(basin_map)

# Check if any reservoir didn't get matched (name mismatch check)
print("Unmatched reservoirs (should be empty):")
print(latest[latest["Basin"].isna()]["Reservoirs"].tolist())

# Group by basin and calculate average percent full
basin_summary = latest.groupby("Basin")["Percent_Full"].mean().sort_values()

print("\nAverage % Full by River Basin:")
print(basin_summary)