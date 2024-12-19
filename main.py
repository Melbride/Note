import streamlit as st
from app.goal_tracker import goal_tracker
from app.prediction_tool import prediction_tool
from app.visualization import visualize_progress
import pandas as pd

if "goal_progress" not in st.session_state:
    st.session_state["goal_progress"] = {}  # Initialize with an empty dictionary

if "goals" not in st.session_state:
    st.session_state["goals"] = pd.DataFrame(columns=["Goal ID", "Goal Name", "Progress", "Target", "Deadline"])

# Load goals data
def load_goals():
    try:
        return pd.read_csv("data/goals.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Goal ID", "Goal Name", "Progress", "Target", "Deadline"])

# Streamlit App
st.title("Personalized Coding Goals and Progress Tracker")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Goal Tracker", "Prediction Tool", "Progress Visualization"])

# Goal Tracker
with tab1:
    goal_tracker()

# Prediction Tool
with tab2:
    prediction_tool()

# Progress Visualization
with tab3:
    visualize_progress(load_goals())
