# CCMOON Scraper – Setup Guide

This guide explains how to set up the CCMOON Scraper and Dashboard on your own machine.

The project has two main parts:

1. ccmoon_scraper.py – collects Reddit data and stores it in moon_data.db
2. moon_dashboard.py – Streamlit dashboard that visualizes the data

---

## 1. Prerequisites

* Python 3.10 or higher. NOTE- 3.14 did not work (too new) so I use 3.12 
  Download from: [https://www.python.org/downloads/]

* A Reddit account and Reddit API app credentials

---

## 2. Clone the repository

From a terminal or Command Prompt:

git clone [https://github.com/your-username/ccmoon-scraper.git]
cd ccmoon-scraper

Replace "your-username" with your GitHub username.

---

## 3. Create and activate a virtual environment (recommended)

Windows:

python -m venv .venv
.venv\Scripts\activate

You should see (.venv) at the start of your prompt when it’s active.

---

## 4. Install dependencies

With the virtual environment active, install all required packages:

pip install -r requirements.txt

---

## 5. Create a Reddit API app and add credentials

1. Go to [https://www.reddit.com/prefs/apps]
2. Click "create another app"
3. Fill in:

   * Name: CCMOON Scraper
   * Type: script
   * Redirect URI: [http://localhost:8080]
4. Save and copy:

   * client id (under the app name)
   * secret (the long text labeled “secret”)

Then open ccmoon_scraper.py and edit the configuration section near the top:

CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
USER_AGENT = "ccmoon snapshot script by /u/YOUR_USERNAME_HERE"

Replace the placeholders with your actual credentials.
(Do not push real credentials to GitHub.)

---

## 6. Configure the time range

In ccmoon_scraper.py you can choose between two modes:

Option A – Fixed dates (good for Moon Weeks):

USE_FIXED_DATES = True
START_DATE_STR = "2025-11-01"
END_DATE_STR   = "2025-11-11"

Option B – Rolling window (for last N days):

USE_FIXED_DATES = False
DAYS_BACK = 1

---

## 7. Run the scraper

python ccmoon_scraper.py

After it runs, you should see:

* A SQLite database file named moon_data.db
* CSV exports for snapshot data and user summary

The database contains all posts and comments collected from r/CryptoCurrency.

---

## 8. Run the dashboard

streamlit run moon_dashboard.py

Then open your browser and go to:

[http://localhost:8501]

You’ll see:

* A dropdown to select a Moon Week
* The Top 50 Adjusted Score earners
* Daily activity charts (posts/comments)
* Flair statistics
* A user lookup tool

---

## 9. Automate daily runs (Windows Task Scheduler)

1. Open Task Scheduler (search in Start Menu).
2. Click "Create Basic Task".
3. Name it something like "CCMOON Daily Data Collection".
4. Trigger: Daily → choose a time (e.g. 3:00 AM).
5. Action: Start a program.

   * Program/script:
     C:\path\to\your\project.venv\Scripts\python.exe
   * Add arguments:
     ccmoon_scraper.py
   * Start in:
     C:\path\to\your\project
6. Finish and optionally test by right-clicking the task → Run.

This will automatically update moon_data.db once per day.

---

## 10. Troubleshooting

**Problem:** "pip" or "streamlit" not recognized
**Fix:** Activate the virtual environment first with
.venv\Scripts\activate

**Problem:** "401 Unauthorized" or authentication errors
**Fix:** Check your CLIENT_ID, CLIENT_SECRET, and USER_AGENT, and confirm your Reddit app type is "script".

**Problem:** Dashboard shows no data
**Fix:** Make sure ccmoon_scraper.py has been run at least once so that moon_data.db and the reddit_activity table exist.

---

If you encounter any other issues, open an Issue on the GitHub repository or contact the maintainers with your error message and setup details.
