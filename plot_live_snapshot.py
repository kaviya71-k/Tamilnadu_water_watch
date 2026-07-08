import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your database and pull the LIVE Tamil Nadu data
conn = sqlite3.connect("chennai_water.db")
df = pd.read_sql("SELECT * FROM live_reservoir_snapshots", conn)
conn.close()

print("Rows loaded:", df.shape)
print(df["Date_Collected"].unique())  # show which dates we actually have

# Get only the MOST RECENT snapshot (in case you ran the scraper multiple times)
latest_date = df["Date_Collected"].max()
latest = df[df["Date_Collected"] == latest_date]

# Remove duplicate reservoirs from that date (keep just one reading per reservoir)
latest = latest.drop_duplicates(subset=["Reservoirs"])

print(f"\nShowing snapshot for: {latest_date}")
print(latest[["Reservoirs", "Current Year Storage (M.Cft.)"]])

# Sort reservoirs by storage size, biggest to smallest, for a cleaner chart
latest = latest.sort_values("Current Year Storage (M.Cft.)", ascending=True)

# Plot as a horizontal bar chart (easier to read reservoir names)
plt.figure(figsize=(10, 8))
plt.barh(latest["Reservoirs"], latest["Current Year Storage (M.Cft.)"], color="teal")
plt.title(f"Tamil Nadu Reservoir Levels — {latest_date}")
plt.xlabel("Current Storage (M.Cft)")
plt.tight_layout()
plt.savefig("tn_live_snapshot.png")
print("\nChart saved as tn_live_snapshot.png")
plt.show()