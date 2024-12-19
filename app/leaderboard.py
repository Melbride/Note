import streamlit as st
import pandas as pd

def leaderboard_component():
    st.subheader("Leaderboard")

    # Example leaderboard data (replace with actual data)
    leaderboard_data = {
        'Username': ['User1', 'User2', 'User3'],
        'Points': [100, 90, 80]
    }

    df = pd.DataFrame(leaderboard_data)
    st.table(df)
