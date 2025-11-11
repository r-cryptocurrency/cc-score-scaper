import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path("moon_data.db")

# ---------------------------
# Helper: DB query with cache
# ---------------------------

@st.cache_data(ttl=300)
def run_query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


def get_moon_weeks():
    df = run_query(
        """
        SELECT DISTINCT moon_week
        FROM reddit_activity
        WHERE moon_week IS NOT NULL
        ORDER BY moon_week
        """
    )
    return df["moon_week"].dropna().tolist()


# ---------------------------
# Streamlit page config
# ---------------------------

st.set_page_config(
    page_title="r/CryptoCurrency Moon Dashboard",
    layout="wide",
)

st.title("🌕 r/CryptoCurrency Moon Dashboard")
st.caption("Backed by local SQLite DB: moon_data.db")

if not DB_PATH.exists():
    st.error(f"Database file {DB_PATH} not found in current directory.")
    st.stop()

# ---------------------------
# Sidebar controls
# ---------------------------

moon_weeks = get_moon_weeks()
if not moon_weeks:
    st.warning("No Moon Weeks found in the database yet.")
    st.stop()

# default to latest Moon Week
default_week = moon_weeks[-1]

selected_week = st.sidebar.selectbox(
    "Select Moon Week",
    moon_weeks,
    index=moon_weeks.index(default_week),
)

st.sidebar.markdown("---")

search_user = st.sidebar.text_input(
    "Search username", value="", placeholder="e.g. 002_timmy"
)

st.sidebar.markdown(
    "Scores are based on **Adjusted Score** (meme penalty + rewards exemptions)."
)

# ---------------------------
# Top 50 earners in week
# ---------------------------

top50_df = run_query(
    """
    SELECT author,
           SUM(adjusted_score) AS total_score
    FROM reddit_activity
    WHERE moon_week = ?
    GROUP BY author
    ORDER BY total_score DESC
    LIMIT 50;
    """,
    (selected_week,),
)

st.subheader(f"Top 50 Adjusted Score Earners – Moon Week {selected_week}")

if top50_df.empty:
    st.info("No data for this Moon Week yet.")
else:
    top50_df = top50_df.rename(columns={"author": "Username", "total_score": "Total Score"})
    st.dataframe(top50_df, use_container_width=True)

    st.bar_chart(
        top50_df.set_index("Username")["Total Score"],
        use_container_width=True,
    )

# ---------------------------
# Daily activity for week
# ---------------------------

st.subheader(f"Daily Activity – Moon Week {selected_week}")

daily_df = run_query(
    """
    SELECT created_date,
           COUNT(*) AS total_items,
           SUM(CASE WHEN post_type = 'post' THEN 1 ELSE 0 END) AS posts,
           SUM(CASE WHEN post_type = 'comment' THEN 1 ELSE 0 END) AS comments
    FROM reddit_activity
    WHERE moon_week = ?
    GROUP BY created_date
    ORDER BY created_date;
    """,
    (selected_week,),
)

if daily_df.empty:
    st.info("No daily data for this Moon Week.")
else:
    total_items = int(daily_df["total_items"].sum())
    total_posts = int(daily_df["posts"].sum())
    total_comments = int(daily_df["comments"].sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Total submissions", f"{total_items:,}")
    c2.metric("Posts", f"{total_posts:,}")
    c3.metric("Comments", f"{total_comments:,}")

    st.line_chart(
        daily_df.set_index("created_date")[["posts", "comments"]],
        use_container_width=True,
    )

# ---------------------------
# Flair stats (posts only)
# ---------------------------

st.subheader(f"Post Flair Stats – Moon Week {selected_week}")

flair_df = run_query(
    """
    SELECT COALESCE(post_flair_type, '') AS flair,
           COUNT(*) AS post_count,
           SUM(adjusted_score) AS total_adjusted_score
    FROM reddit_activity
    WHERE moon_week = ?
      AND post_type = 'post'
    GROUP BY post_flair_type
    ORDER BY total_adjusted_score DESC;
    """,
    (selected_week,),
)

if flair_df.empty:
    st.info("No posts with flair found for this Moon Week.")
else:
    flair_df = flair_df.rename(
        columns={
            "flair": "Flair",
            "post_count": "Post Count",
            "total_adjusted_score": "Total Adjusted Score",
        }
    )
    st.dataframe(flair_df, use_container_width=True)

    st.bar_chart(
        flair_df.set_index("Flair")[["Post Count", "Total Adjusted Score"]],
        use_container_width=True,
    )

# ---------------------------
# User search
# ---------------------------

st.subheader("🔍 User Lookup")

if not search_user:
    st.info("Enter a username in the sidebar to look up their scores.")
else:
    username = search_user.strip()

    total_df = run_query(
        """
        SELECT COALESCE(SUM(adjusted_score), 0) AS total_score
        FROM reddit_activity
        WHERE author = ?;
        """,
        (username,),
    )
    overall_total = int(total_df["total_score"].iloc[0])

    st.markdown(f"### Results for **u/{username}**")
    st.metric("Overall Adjusted Score (all weeks)", f"{overall_total:,}")

    by_week_df = run_query(
        """
        SELECT moon_week,
               SUM(CASE WHEN post_type = 'post' THEN adjusted_score ELSE 0 END) AS post_score,
               SUM(CASE WHEN post_type = 'comment' THEN adjusted_score ELSE 0 END) AS comment_score,
               SUM(adjusted_score) AS total_score
        FROM reddit_activity
        WHERE author = ?
        GROUP BY moon_week
        ORDER BY moon_week;
        """,
        (username,),
    )

    if by_week_df.empty:
        st.info("No entries found for this user in the database.")
    else:
        by_week_df = by_week_df.rename(
            columns={
                "moon_week": "Moon Week",
                "post_score": "Post Score",
                "comment_score": "Comment Score",
                "total_score": "Total Score",
            }
        )
        st.dataframe(by_week_df, use_container_width=True)

        st.bar_chart(
            by_week_df.set_index("Moon Week")[["Post Score", "Comment Score"]],
            use_container_width=True,
        )
