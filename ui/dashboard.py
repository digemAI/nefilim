from pathlib import Path
import sys

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from config import HISTORY_FILE_PATH
from data.storage import load_history


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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("State", latest.get("state", "unknown"))

with col2:
    st.metric("Mood", latest.get("mood", "N/A"))

with col3:
    st.metric("Anxiety", latest.get("anxiety", "N/A"))


# Show the full visible history
st.subheader("History")
st.dataframe(df, use_container_width=True)
