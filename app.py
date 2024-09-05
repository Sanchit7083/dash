import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title for the Streamlit app
st.title("Sample Graph Deployment on Streamlit")

# Create some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Add a slider to adjust the frequency
frequency = st.slider("Frequency", 1, 10, 1)

# Plot the graph
fig, ax = plt.subplots()
ax.plot(x, np.sin(frequency * x), label=f'Sin({frequency} * x)')
ax.legend()

# Display the plot
st.pyplot(fig)

# Add some text
st.write(f"Current frequency: {frequency}")
