import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data for different selections
data_dict = {
    'Option 1': [10, 15, 20, 25, 30],
    'Option 2': [5, 10, 15, 20, 25],
    'Option 3': [8, 12, 16, 20, 24],
}

# Create a Streamlit app
st.title('Dropdown Selection and Bar Chart')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', list(data_dict.keys()))

# Get data for the selected option
selected_data = data_dict[selected_option]

# Create a bar chart based on the selected data
fig, ax = plt.subplots()
ax.bar(range(1, len(selected_data)+1), selected_data, color='blue')
ax.set_xlabel('X-Axis Label')
ax.set_ylabel('Y-Axis Label')
ax.set_title(f'Bar Chart - {selected_option}')

# Display the bar chart using Streamlit
st.pyplot(fig)
