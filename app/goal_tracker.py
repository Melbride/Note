import streamlit as st
import pandas as pd
import os

# Initialize session state for goals if not already initialized
if "goals" not in st.session_state:
    if os.path.exists("data/goals.csv"):
        st.session_state.goals = pd.read_csv("data/goals.csv")
    else:
        st.session_state.goals = pd.DataFrame(columns=["Goal ID", "Goal Name", "Progress", "Target", "Deadline"])

def goal_tracker():
    st.subheader("Set and Track Your Coding Goals")

    # Form for adding a new goal
    with st.form("goal_form", clear_on_submit=True):
        goal_name = st.text_input("Goal Name", key="goal_name_input")
        progress = st.slider("Progress", 0, 100, step=1, key="progress_slider")
        target = st.number_input("Target (e.g., 100 for 100%)", min_value=1, step=1, key="target_input")
        deadline = st.date_input("Deadline", key="deadline_input")

        submitted = st.form_submit_button("Add Goal")
        if submitted:
            if not goal_name:
                st.error("Goal Name cannot be empty.")
            else:
                # Generate unique Goal ID
                next_goal_id = (
                    st.session_state.goals["Goal ID"].max() + 1
                    if not st.session_state.goals.empty
                    else 1
                )

                # Add new goal to DataFrame
                new_goal = {
                    "Goal ID": next_goal_id,
                    "Goal Name": goal_name,
                    "Progress": progress,
                    "Target": target,
                    "Deadline": str(deadline),
                }
                st.session_state.goals = pd.concat(
                    [st.session_state.goals, pd.DataFrame([new_goal])],
                    ignore_index=True,
                )

                # Save to CSV
                os.makedirs("data", exist_ok=True)  # Ensure 'data' directory exists
                st.session_state.goals.to_csv("data/goals.csv", index=False)

                st.success(f"Goal '{goal_name}' added successfully!")

    # Display existing goals
    st.subheader("Your Goals")
    if not st.session_state.goals.empty:
        st.dataframe(st.session_state.goals)
    else:
        st.info("No goals added yet.")
