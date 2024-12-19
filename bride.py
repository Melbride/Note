import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# Load the trained model and assets
model = joblib.load('model.pkl')
country_freq = joblib.load('country_freq.pkl')
difficulty_encoder = joblib.load('difficulty_encoder.pkl')
problem_names_encoder = joblib.load('problem_names_encoder.pkl')
prog_lang_encoder = joblib.load('prog_lang_encoder.pkl')

# Prepare options for dropdowns
available_countries = list(country_freq.keys())
available_problem_names = list(problem_names_encoder.classes_)
programming_languages = list(prog_lang_encoder.classes_)

# Theme selection
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

theme_toggle = st.sidebar.button("Toggle Theme")
if theme_toggle:
    st.session_state.dark_mode = not st.session_state.dark_mode
    
# Apply custom CSS based on theme
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            .stTextInput, .stNumberInput, .stSelectbox {
                color: #ffffff;
            }
            label {
                color: #ffffff !important;
            }
            .header {
                color: #4CAF50;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stSubheader {
                color: #ffffff !important; /* Ensuring subheader is visible in dark mode */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f9f9f9;
                color: #000000;
            }
            .header {
                color: #4CAF50;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stSubheader {
                color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# App title and description
st.markdown("<div class='header'>Coding Challenge Pass/Fail Predictor</div>", unsafe_allow_html=True)
st.subheader("Predict outcomes for coding problems with ease!")

# Input fields
problem_id = st.number_input("Problem ID", min_value=1, step=1)
country_input = st.selectbox("Country", options=["Select a Country"] + available_countries)
count = st.number_input("Count", min_value=0, step=1)
difficulty_input = st.selectbox("Difficulty", options=list(difficulty_encoder.classes_))
max_score = st.number_input("Max Score", min_value=0, step=1)
problem_type_data_structures = st.selectbox("Problem Type", options=["Data Structures", "Other"])
skills_input = st.selectbox("Skills", options=["Basic", "Intermediate", "Advanced"])
problem_name_input = st.selectbox("Problem Name", options=["Select a Problem"] + available_problem_names)
prog_lang_input = st.selectbox("Programming Language", options=programming_languages)

# Check if essential inputs are selected
if country_input == "Select a Country" or problem_name_input == "Select a Problem":
    st.error("Please input all fields.")
else:
    # Encode inputs
    country_encoded = country_freq.get(country_input, 0)
    difficulty_encoded = difficulty_encoder.transform([difficulty_input])[0]
    problem_name_encoded = -1 if problem_name_input == "Select a Problem" else problem_names_encoder.transform([problem_name_input])[0]
    problem_type_encoded = 1 if problem_type_data_structures == "Data Structures" else 0
    skills_encoded = {"Basic": 0, "Intermediate": 1, "Advanced": 2}[skills_input]
    prog_lang_encoded = {lang: idx for idx, lang in enumerate(programming_languages)}[prog_lang_input]

    # Collect inputs into a DataFrame
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

    # Predict and visualize
    if st.button("Predict"):
        try:
            # Convert input data to numpy array without column names to avoid warning
            input_data_values = input_data.values
            
            prediction = model.predict(input_data_values)
            prob = model.predict_proba(input_data_values)

            # Display results
            result_text = "Pass ✅" if prediction[0] == 0 else "Fail ❌"
            prob_text = f"Probability of Pass: {prob[0][0]:.2f}, Probability of Fail: {prob[0][1]:.2f}"
            st.markdown(f"<div class='header'>Prediction Result: {result_text}</div>", unsafe_allow_html=True)
            st.write(prob_text)

            # Visualization
            fig = go.Figure(data=[ 
                go.Bar(name="Pass", x=["Prediction"], y=[prob[0][0]], marker_color="green"),
                go.Bar(name="Fail", x=["Prediction"], y=[prob[0][1]], marker_color="red")
            ])
            fig.update_layout(title="Prediction Probabilities", barmode="group")
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error during prediction: {e}")
