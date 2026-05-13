from pathlib import Path
import sys

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

st.title("NEFILIM v3 Dashboard")
st.caption("Visual layer for reviewing history, states, and recent trends.")


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

st.write(f"Notes: {latest.get('notes', '')}")

# Show the full visible history
st.subheader("History")
st.dataframe(df, use_container_width=True)