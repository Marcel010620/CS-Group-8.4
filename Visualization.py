import streamlit as st
import pandas as pd
import altair as alt
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

# Create a DataFrame for Altair
df = pd.DataFrame({'X': range(1, len(selected_data)+1), 'Y': selected_data})

# Create a bar chart with Altair
chart = alt.Chart(df).mark_bar().encode(
    x='X',
    y='Y',
    color=alt.value('blue')
).properties(
    width=400,
    height=300,
    title=f'Bar Chart - {selected_option}'
)

# Display the bar chart using Streamlit
st.altair_chart(chart, use_container_width=True)
