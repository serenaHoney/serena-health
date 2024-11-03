import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go

st.title("Patient Monitoring")
st.write(
    "Monitor the health of individual patients and view their clinical record, using their ID"
)

st.sidebar.header("Patient Biometric Data")
st.write(
    """Individual patient biometric data"""
)

# Temperature

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()


from sqlalchemy import create_engine
import pandas as pd

# Create SQLAlchemy engine
engine = create_engine('sqlite:///hospital_data.db')

# Query the patient IDs
query = "SELECT ID FROM Patients"
with engine.connect() as conn:
    patient_data = pd.read_sql(query, conn)

# Display the patient data as a DataFrame
st.dataframe(patient_data)


# creating a single-element container
placeholder = st.empty()

#a random ecg waveform
def generate_ecg_data():
    t = np.linspace(1, np.random.choice(range(8, 10)), np.random.choice(range(900, 1000)))
    p_wave = 0.1 * np.sin(2 * np.pi * t)
    qrs_wave = np.sin(2 * np.pi * t) + 0.5 * np.sin(20 * np.pi * t)
    s_wave = -0.2 * np.sin(2 * np.pi * t)
    ecg = p_wave + qrs_wave + s_wave
    return t, ecg

while True:

    t, ecg = generate_ecg_data()

    with placeholder.container():
        fig = go.Figure(data=go.Scatter(x=t, y=ecg))
        fig.update_layout(
            title="ECG Waveform",
            xaxis_title="Time",
            yaxis_title="Amplitude",
            template="plotly_white"
        )
        st.plotly_chart(fig)
        time.sleep(1)





