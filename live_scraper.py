import pandas as pd
import sqlite3
from datetime import date

url = "https://tnagriculture.in/ARS/home/reservoir"

tables = pd.read_html(url)
df_live = tables[0]

# Drop rows where 'Reservoirs' is empty/NaN
df_live = df_live.dropna(subset=["Reservoirs"])

# Add today's date so we know when this snapshot was taken
df_live["Date_Collected"] = date.today()

print("Shape after cleaning:", df_live.shape)
print(df_live.head())

# Save into the same database, in a NEW table called 'live_reservoir_snapshots'
conn = sqlite3.connect("chennai_water.db")
df_live.to_sql("live_reservoir_snapshots", conn, if_exists="append", index=False)
conn.close()

print("\nSaved today's snapshot to database!")