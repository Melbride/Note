import streamlit as st
import plotly.express as px
import pandas as pd

def visualize_progress(goals_df):
    st.subheader("Your Progress")

    if not goals_df.empty:
        # Generate enough unique colors for all progress entries
        num_rows = len(goals_df)
        colors = px.colors.qualitative.Set3 * (num_rows // len(px.colors.qualitative.Set3) + 1)

        # Assign a unique color to each row
        goals_df["Color"] = colors[:num_rows]

        # Plot with unique colors for each progress entry
        fig = px.bar(
            goals_df,
            x="Goal Name",
            y="Progress",
            color="Color",  # Use unique colors explicitly
            color_discrete_map="identity",  # Ensures colors are used as provided
            title="Progress on Goals",
            labels={"Progress": "Current Progress"}
        )
        st.plotly_chart(fig)
    else:
        st.info("No goals added yet. Go to the Goal Tracker tab to add goals.")
