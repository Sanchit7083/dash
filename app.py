import streamlit as st
import numpy as np
import plotly.express as px

# Title for the Streamlit app
st.title("Interactive Plot using Plotly")

# Create some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Add a slider to adjust the frequency
frequency = st.slider("Frequency", 1, 10, 1)

# Update y values based on the frequency
y_updated = np.sin(frequency * x)

# Create an interactive Plotly chart
fig = px.line(x=x, y=y_updated, labels={'x': 'X-axis', 'y': 'Y-axis'},
              title=f'Sine Wave with Frequency {frequency}')

# Display the plot in Streamlit
st.plotly_chart(fig)

# Add some text
st.write(f"Current frequency: {frequency}")
