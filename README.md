# 🌊 Tamil Nadu Reservoir Watch

A real-time and historical water reservoir monitoring dashboard for Tamil Nadu — tracking Chennai's reservoirs since 2003 and live data for 19 major TN reservoirs, updated automatically every day.

🔗 **Live Dashboard:** [tamilnaduwaterwatch.streamlit.app](https://tamilnaduwaterwatch-e4w6onylffwodbrvbdxmql.streamlit.app)

## Why This Project

Chennai faced a severe water crisis in 2019, when reservoirs ran critically low. This project tracks reservoir health over time — historically and live — to make water scarcity visible and understandable through data.

## Features

- 📈 **Historical trends** — Interactive charts of Chennai's 5 reservoirs from 2003–2021, showing the 2019 crisis clearly
- 🚦 **Live risk scoring** — Real-time status (Safe / Watch / Critical) for 19 Tamil Nadu reservoirs, based on current storage vs. full capacity
- 🌍 **Regional analysis** — Reservoirs grouped by river basin to identify which regions face the most water stress
- 🤖 **Fully automated** — A daily GitHub Actions workflow scrapes live government data and updates the database with zero manual effort

## Tech Stack

- **Python** — pandas, matplotlib
- **Database** — SQLite
- **Web scraping** — requests, BeautifulSoup, pandas.read_html
- **Automation** — GitHub Actions (scheduled daily scraping)
- **Dashboard** — Streamlit, deployed on Streamlit Community Cloud

## Data Sources

- Historical Chennai reservoir data (2003–2021): [OpenCity.in](https://data.opencity.in)
- Live Tamil Nadu reservoir data: [Tamil Nadu Agriculture Department](https://tnagriculture.in/ARS/home/reservoir)

## What I Learned / Challenges Solved

- Fixed inconsistent column naming and a comma-corrupted data type across 5 real government CSVs
- Debugged malformed HTML from a live government website by switching to `pandas.read_html()`
- Resolved GitHub Actions authentication and push-permission issues to enable full daily automation
- Designed a risk-scoring and regional-grouping system to turn raw numbers into actionable insight

## Screenshots

*(Add 2-3 screenshots here — historical chart, risk table, regional chart)*

## Run It Locally

```bash
git clone https://github.com/kaviya71-k/Tamilnadu_water_watch.git
cd Tamilnadu_water_watch
pip install -r requirements.txt
streamlit run app.py
```