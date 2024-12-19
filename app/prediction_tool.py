import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', 'model', 'model.pkl')
model = joblib.load(model_path)
country_freq = joblib.load('model/country_freq.pkl')
difficulty_encoder = joblib.load('model/difficulty_encoder.pkl')
prog_lang_encoder = joblib.load('model/prog_lang_encoder.pkl')
problem_names_encoder = joblib.load('model/problem_names_encoder.pkl')


available_countries = list(country_freq.keys())
available_problem_names = list(problem_names_encoder.classes_)
programming_languages = list(prog_lang_encoder.classes_)


def prediction_tool():
    st.subheader("Challenge Pass/Fail Predictor")

    # Inputs with unique keys to avoid DuplicateWidgetID errors
    problem_id = st.number_input("Problem ID", min_value=1, step=1, key="problem_id_input")
    country_input = st.selectbox("Country", options=["Select a Country"] + available_countries, key="country_input")
    count = st.number_input("Count", min_value=0, step=1, key="count_input")
    difficulty_input = st.selectbox("Difficulty", options=list(difficulty_encoder.classes_), key="difficulty_input")
    max_score = st.number_input("Max Score", min_value=0, step=1, key="max_score_input")
    problem_type_data_structures = st.selectbox("Problem Type", options=["Data Structures", "Other"], key="problem_type_input")
    skills_input = st.selectbox("Skills", options=["Basic", "Intermediate", "Advanced"], key="skills_input")
    problem_name_input = st.selectbox("Problem Name", options=["Select a Problem"] + available_problem_names, key="problem_name_input")
    prog_lang_input = st.selectbox("Programming Language", options=programming_languages, key="prog_lang_input")

    # Goal Selection (if goal_progress exists)
    goal_selected = st.selectbox("Select Related Goal", options=["None"] + list(st.session_state["goal_progress"].keys()), key="goal_selected_input")
    goal_progress_value = 0
    if goal_selected != "None":
        goal_progress_value = st.session_state["goal_progress"][goal_selected]
        st.write(f"Progress for '{goal_selected}': {goal_progress_value}%")

    # Predict Button
    if st.button("Predict", key="predict_button"):
        if country_input == "Select a Country":
            st.error("Please select a valid country.")
        else:
            # Prepare input data for prediction (only 9 features, no goal_progress)
            country_encoded = country_freq.get(country_input, 0)
            difficulty_encoded = difficulty_encoder.transform([difficulty_input])[0]
            problem_name_encoded = -1 if problem_name_input == "Select a Problem" else problem_names_encoder.transform([problem_name_input])[0]
            problem_type_encoded = 1 if problem_type_data_structures == "Data Structures" else 0
            skills_encoded = {"Basic": 0, "Intermediate": 1, "Advanced": 2}[skills_input]
            prog_lang_encoded = {lang: idx for idx, lang in enumerate(programming_languages)}[prog_lang_input]

            # Creating input data with 9 features (excluding goal_progress)
            input_data = pd.DataFrame({
                'problem_id': [problem_id],
                'country': [country_encoded],
                'count': [count],
                'difficulty': [difficulty_encoded],
                'max_score': [max_score],
                'problem_type_data_structures': [problem_type_encoded],
                'skills_encoded': [skills_encoded],
                'problem_name_encoded': [problem_name_encoded],
                'prog_lang_encoded': [prog_lang_encoded]
            })

            # Predict
            prediction = model.predict(input_data.values)
            prob = model.predict_proba(input_data.values)

            # Display Results
            result_text = "Pass ✅" if prediction[0] == 0 else "Fail ❌"
            st.write(f"Prediction: {result_text}")
            st.write(f"Probability - Pass: {prob[0][0]:.2f}, Fail: {prob[0][1]:.2f}")
