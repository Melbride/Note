import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('model.pkl')

# App title
st.title("Pass/Fail Prediction App")

# User input
st.header("Input Features")
col1, col2 = st.columns(2)

# Add input fields for features (adjust according to your dataset)
feature1 = col1.number_input("Feature 1", min_value=0.0, step=0.1)
feature2 = col2.number_input("Feature 2", min_value=0.0, step=0.1)
feature3 = st.number_input("Feature 3", min_value=0.0, step=0.1)

# Collect inputs into a DataFrame
input_data = pd.DataFrame({
    'Feature1': [feature1],
    'Feature2': [feature2],
    'Feature3': [feature3]
})

# Predict button
if st.button("Predict"):
    prediction = model.predict(input_data)
    prob = model.predict_proba(input_data)
    
    if prediction[0] == 1:
        st.success(f"The prediction is: **Fail** (Probability: {prob[0][1]:.2f})")
    else:
        st.success(f"The prediction is: **Pass** (Probability: {prob[0][0]:.2f})")
