import pandas as pd
import sqlite3
from datetime import date
import sys

url = "https://tnagriculture.in/ARS/home/reservoir"

try:
    tables = pd.read_html(url)

    if len(tables) == 0:
        print("Error: No tables found on the page. The site's structure may have changed.")
        sys.exit(1)

    df_live = tables[0]
    df_live = df_live.dropna(subset=["Reservoirs"])

    if df_live.shape[0] == 0:
        print("Error: Table was found but contained no valid reservoir rows.")
        sys.exit(1)

    df_live["Date_Collected"] = date.today()

    print("Shape after cleaning:", df_live.shape)
    print(df_live.head())

    conn = sqlite3.connect("chennai_water.db")
    df_live.to_sql("live_reservoir_snapshots", conn, if_exists="append", index=False)
    conn.close()

    print("\nSaved today's snapshot to database!")

except Exception as e:
    print(f"Scraping failed with error: {e}")
    print("No data was saved. The site may be down or its structure may have changed.")
    sys.exit(1)