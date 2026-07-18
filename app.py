import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tamil Nadu Reservoir Watch", layout="wide")

st.title("🌊 Tamil Nadu Reservoir Watch")
st.write("Tracking Chennai's historical water levels and live Tamil Nadu reservoir data.")

# ---- Connect to database ----
conn = sqlite3.connect("chennai_water.db")

# ---- SECTION 1: Historical Chennai Trend ----
st.header("📈 Chennai Historical Reservoir Trends (2003-2021)")

hist_df = pd.read_sql("SELECT * FROM reservoir_levels", conn)
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

conn.close()