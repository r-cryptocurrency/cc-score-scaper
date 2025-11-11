CCMOON Scraper

A daily Reddit data collection script and dashboard for tracking user activity and MOON distribution on the r/CryptoCurrency
 subreddit.

This tool automatically pulls posts and comments from Reddit’s API using PRAW, calculates adjusted user scores (based on flair and rewards rules), and stores everything in a local SQLite database. It also includes a Streamlit dashboard for visualization.

# Features

Collects posts and comments within a date range or Moon Week window

Adjusts scores for:
-Rewards Exempt users ([deleted], coinfeeds-bot)
-MEME flair posts (0.25x weighting)

Automatically stores data in a persistent SQLite database (moon_data.db)

Generates CSV exports for Google Sheets or DAO transparency

Streamlit dashboard for:
- Top 50 earners per Moon Week
- User lookup by username
- Daily activity charts (posts/comments)
- Flair-based post and score analytics

# Project Structure

rcc-scripts/
│
├── ccmoon_scraper.py — Main Reddit data scraper
├── moon_dashboard.py — Streamlit dashboard
├── moon_data.db — SQLite database (auto-created)
├── .venv/ — Virtual environment (optional)
├── README.md — Project documentation
├── LICENSE — License file
└── .gitignore — Git exclusions

# Installation
Clone the repository:
git clone https://github.com/your-username/ccmoon-scraper.git

cd ccmoon-scraper

(Optional) Create a virtual environment:
python -m venv .venv
.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
(Or install manually: pip install praw pandas streamlit)

Add your Reddit app credentials at the top of ccmoon_scraper.py:

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
USER_AGENT = "ccmoon snapshot script by /u/YOUR_USERNAME"

# Running the scraper
To collect data for a specific Moon Week:
python ccmoon_scraper.py
To collect daily:
python ccmoon_scraper.py
(Adjust USE_FIXED_DATES or DAYS_BACK in the config section.)

# Dashboard
Launch the dashboard:
streamlit run moon_dashboard.py
It opens in your browser at http://localhost:8501.

# Automating daily runs
Use Windows Task Scheduler to run ccmoon_scraper.py daily:
Program: path to .venv\Scripts\python.exe
Arguments: "ccmoon_scraper.py"
Start in: your project folder
This ensures daily updates to your moon_data.db without manual action.

# License
This project is open-source under the MIT License. See the LICENSE file for details.

# Credits
Created for the CCMOON DAO by u/002_timmy to track Moon distribution transparently.
