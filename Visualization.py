import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Sample data for different selections
data_dict = {
    'Owner': ['Ben', 'Jan', 'Sven', 'Diego', 'Mike'],
    'Article': ['Milk', 'Pepper', 'Salad', 'Ham', 'Wine'],
    'Expiry Date': [3, 2, 4, 7, 5],
}

# Create a Streamlit app
st.title('Dropdown Selection and Bar Chart')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', list(data_dict.keys()))

# Get data for the selected option
selected_data = data_dict[selected_option]

# Create a DataFrame for Altair
df = pd.DataFrame({'X': range(1, len(selected_data)+1), 'Y': selected_data})

# Define the step size on the x-axis
step_size = 1  # Change this value according to your preference


# Create a bar chart with Altair
chart = alt.Chart(df).mark_bar().encode(
    x='X',
    y='Y',
    color=alt.value('red')
).properties(
    width=400,
    height=300,
    title=f'Bar Chart - {selected_option}'
)

# Display the bar chart using Streamlit
st.altair_chart(chart, use_container_width=True)

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample data
data = {
    'Article': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
    'Quantity': [10, 5, 7, 3, 2],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit'],
    'Owner': ['A', 'B', 'C', 'A', 'B'],
    'Expiration Date': [datetime(2023, 12, 1), datetime(2023, 12, 3), datetime(2023, 12, 5), datetime(2023, 11, 25), datetime(2023, 12, 7)],
}

df = pd.DataFrame(data)

# Create a Streamlit app
st.title('List Based on Dropdown Selection')

# Create a dropdown to select either "Owner" or "Expires soon"
selection_option = st.selectbox('Select an option:', ['Owner', 'Expires soon'])

# Display the selected option
st.write(f'Selected option: {selection_option}')

# Based on the selected option, create and display the corresponding list
if selection_option == 'Owner':
    owners_list = df['Owner'].unique()
    selected_list = st.multiselect('Select owners:', owners_list)
    st.write(f'Selected owners: {selected_list}')

elif selection_option == 'Expires soon':
    expiration_threshold = datetime.now() + timedelta(days=2)
    expiring_articles = df[df['Expiration Date'] <= expiration_threshold]['Article'].tolist()
    st.write("Articles that expire soon:")
    st.write(expiring_articles)
