import streamlit as st
import plotly.express as px
import pandas as pd

def trends_component():
    st.subheader("Historical Trends")

    # Example trend data (replace with actual data)
    trend_data = pd.DataFrame({
        'Date': ['2023-01-01', '2023-02-01', '2023-03-01'],
        'Submissions': [50, 75, 100]
    })
    
    # Plotting the trends
    fig = px.line(trend_data, x='Date', y='Submissions', title='Submissions Over Time')
    st.plotly_chart(fig)
