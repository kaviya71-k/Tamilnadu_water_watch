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

- Historical Chennai reservoir