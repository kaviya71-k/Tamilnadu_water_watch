import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your database and pull ALL reservoirs' historical data
conn = sqlite3.connect("chennai_water.db")
df = pd.read_sql("SELECT * FROM reservoir_levels", conn)
conn.close()

print("Rows loaded:", df.shape)

# Combine Year and Month into a proper date column
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"], format="%Y-%b")
df = df.sort_values("Date")

# Plot each reservoir as its own line on the same chart
plt.figure(figsize=(13, 7))

for reservoir in df["Reservoir"].unique():
    subset = df[df["Reservoir"] == reservoir]
    plt.plot(subset["Date"], subset["Level"], label=reservoir)

plt.title("All Chennai Reservoirs — Water Level Over Time (2003-2021)")
plt.xlabel("Year")
plt.ylabel("Water Level (M.Cft)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("all_reservoirs_trend.png")
print("\nChart saved as all_reservoirs_trend.png")
plt.show()