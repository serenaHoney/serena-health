import streamlit as st
import time
import numpy as np

st.title("Patient Monitoring")
st.write(
    "Monitor the health of individual patients and view their clinical record, using their ID"
)

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

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

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

import time
import streamlit as st
import plotly.graph_objects as go
import numpy as np

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
        st.title("ECG Waveform")

        fig = go.Figure(data=go.Scatter(x=t, y=ecg))
        fig.update_layout(
            title="ECG Waveform",
            xaxis_title="Time",
            yaxis_title="Amplitude",
            template="plotly_white"
        )
        st.plotly_chart(fig)
        time.sleep(1)

