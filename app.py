import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tamil Nadu Reservoir Watch", layout="wide")

st.title("🌊 Tamil Nadu Reservoir Watch")
st.write("Tracking Chennai's historical water levels and live Tamil Nadu reservoir data.")

# ---- SECTION 1: Historical Chennai Trend ----
st.header("📈 Chennai Historical Reservoir Trends (2003-2021)")

conn = sqlite3.connect("chennai_water.db")
hist_df = pd.read_sql("SELECT * FROM reservoir_levels", conn)
conn.close()

hist_df["Date"] = pd.to_datetime(hist_df["Year"].astype(str) + "-" + hist_df["Month"], format="%Y-%b")
hist_df = hist_df.sort_values("Date")

selected_reservoir = st.selectbox("Choose a reservoir:", hist_df["Reservoir"].unique())
filtered = hist_df[hist_df["Reservoir"] == selected_reservoir]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(filtered["Date"], filtered["Level"], color="steelblue")
ax.set_title(f"{selected_reservoir} Water Level Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Water Level (M.Cft)")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ---- SECTION 2: Live Tamil Nadu Snapshot with Risk Scores ----
st.header("🚦 Live Tamil Nadu Reservoir Status")

conn = sqlite3.connect("chennai_water.db")
live_df = pd.read_sql("SELECT * FROM live_reservoir_snapshots", conn)
conn.close()

latest_date = live_df["Date_Collected"].max()
latest = live_df[live_df["Date_Collected"] == latest_date]
latest = latest.drop_duplicates(subset=["Reservoirs"])
latest["Reservoirs"] = latest["Reservoirs"].str.strip().str.replace(r"\s+", " ", regex=True)

latest["Percent_Full"] = (latest["Current Year Storage (M.Cft.)"] / latest["Full Capacity (M.Cft.)"]) * 100

def get_risk_level(pct):
    if pct >= 50:
        return "🟢 Safe"
    elif pct >= 20:
        return "🟡 Watch"
    else:
        return "🔴 Critical"

latest["Risk_Level"] = latest["Percent_Full"].apply(get_risk_level)
latest = latest.sort_values("Percent_Full")

st.write(f"Showing data collected on: **{latest_date}**")

st.dataframe(
    latest[["Reservoirs", "Percent_Full", "Risk_Level"]].reset_index(drop=True),
    use_container_width=True
)