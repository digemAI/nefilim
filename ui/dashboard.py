from pathlib import Path
import sys

import altair as alt
import pandas as pd
import streamlit as st


# Add the project root so dashboard imports can find NEFILIM modules
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from config import HISTORY_FILE_PATH
from core.state_detector import detect_state
from data.schema import record_from_dict
from data.storage import load_history


# Configure the dashboard page and main header
st.set_page_config(
    page_title="NEFILIM Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# Apply small visual adjustments for better dashboard readability
st.markdown(
    """
    <style>
    .dashboard-caption {
        font-size: 18px;
        color: #a8adb7;
        margin-top: -8px;
        margin-bottom: 28px;
    }

    .dashboard-notes {
        font-size: 18px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    div[data-testid="stAlert"] {
        font-size: 18px;
    }

    div[data-testid="stSelectbox"] label {
        font-size: 18px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("NEFILIM v3 Dashboard")

st.markdown(
    '<p class="dashboard-caption">Visual layer for reviewing history, states, and recent trends.</p>',
    unsafe_allow_html=True,
)


# Load the stored history for dashboard rendering
history = load_history(HISTORY_FILE_PATH)

if not history:
    st.warning("No history found yet. Run NEFILIM from the CLI first.")
    st.stop()


# Convert stored records into a tabular view
df = pd.DataFrame(history)

st.subheader("Latest record")

latest = df.iloc[-1]
latest_record = record_from_dict(latest.to_dict())

if latest_record is None:
    st.error("Latest record could not be converted into a valid NEFILIM record.")
    st.stop()


# Detect the current state from the latest stored record
latest_state = detect_state(latest_record)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("State", latest_state.state)

with col2:
    st.metric("Sleep", latest.get("sleep_hours", "N/A"))

with col3:
    st.metric("Mood", latest.get("mood", "N/A"))

with col4:
    st.metric("Anxiety", latest.get("anxiety", "N/A"))

with col5:
    st.metric("Energy", latest.get("energy", "N/A"))

with col6:
    st.metric("Focus", latest.get("focus", "N/A"))


# Show the main reason behind the latest state
st.info(f"Reason: {latest_state.reason}")

# Show the latest notes if available
notes = latest.get("notes", "")

if notes:
    st.markdown(
        f'<p class="dashboard-notes">Notes: {notes}</p>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<p class="dashboard-notes">Notes: No notes added.</p>',
        unsafe_allow_html=True,
    )


# Prepare history data for visible trend charts
trend_df = df.copy()
trend_df["timestamp"] = pd.to_datetime(trend_df["timestamp"], errors="coerce")
trend_df = trend_df.dropna(subset=["timestamp"])
trend_df = trend_df.sort_values("timestamp")

st.subheader("Visible trends")

metric_columns = [
    "sleep_hours",
    "mood",
    "anxiety",
    "energy",
    "focus",
]

if len(trend_df) < 2:
    st.warning("At least two records are needed to show visible trends.")

else:
    # Let the user review one specific metric as a clean trend chart
    trend_view = st.selectbox(
        "Select trend view",
        metric_columns,
    )

    chart_df = trend_df.tail(7).copy()
    chart_df["record"] = [f"Record {i + 1}" for i in range(len(chart_df))]

    # Keep sleep visually aligned with the 0-10 dashboard scale
    chart_df["sleep_hours_visual"] = chart_df["sleep_hours"].clip(upper=10)

    chart_metric = trend_view

    if trend_view == "sleep_hours":
        chart_metric = "sleep_hours_visual"

    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("record:N", title="Record"),
            y=alt.Y(
                f"{chart_metric}:Q",
                title=f"{trend_view} 0-10",
                scale=alt.Scale(domain=[0, 10]),
                axis=alt.Axis(values=list(range(0, 11))),
            ),
            tooltip=[
                "record:N",
                alt.Tooltip(f"{chart_metric}:Q", title=trend_view),
            ],
        )
        .properties(height=260)
    )

    st.altair_chart(chart, use_container_width=True)


# Keep the full history available without making it the main view
with st.expander("Show full history"):
    st.dataframe(df, use_container_width=True)