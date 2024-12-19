# components/prediction.py
import pandas as pd
import joblib
import plotly.graph_objects as go
import streamlit as st

# Load the trained model and assets
@st.cache_resource
def load_assets():
    model = joblib.load('utils/model.pkl')  # Updated path to utils folder
    country_freq = joblib.load('utils/country_freq.pkl')  # Updated path to utils folder
    difficulty_encoder = joblib.load('utils/difficulty_encoder.pkl')  # Updated path to utils folder
    problem_names_encoder = joblib.load('utils/problem_names_encoder.pkl')  # Updated path to utils folder
    prog_lang_encoder = joblib.load('utils/prog_lang_encoder.pkl')  # Updated path to utils folder
    return model, country_freq, difficulty_encoder, problem_names_encoder, prog_lang_encoder

model, country_freq, difficulty_encoder, problem_names_encoder, prog_lang_encoder = load_assets()

# Prediction function
def make_prediction(problem_id, country, count, difficulty, max_score, problem_type, skills, problem_name, prog_lang):
    try:
        # Encode inputs
        country_encoded = country_freq.get(country, 0)
        difficulty_encoded = difficulty_encoder.transform([difficulty])[0]
        problem_name_encoded = problem_names_encoder.transform([problem_name])[0] if problem_name != "Select a Problem" else -1
        problem_type_encoded = 1 if problem_type == "Data Structures" else 0
        skills_encoded = {"Basic": 0, "Intermediate": 1, "Advanced": 2}[skills]
        prog_lang_encoded = prog_lang_encoder.transform([prog_lang])[0]

        # Prepare data for prediction
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

        # Make prediction
        prediction = model.predict(input_data.values)
        prob = model.predict_proba(input_data.values)

        return prediction, prob
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None

# Visualization function
def visualize_prediction(prob):
    fig = go.Figure(data=[
        go.Bar(name="Pass", x=["Prediction"], y=[prob[0][0]], marker_color="green"),
        go.Bar(name="Fail", x=["Prediction"], y=[prob[0][1]], marker_color="red")
    ])
    fig.update_layout(title="Prediction Probabilities", barmode="group")
    return fig
