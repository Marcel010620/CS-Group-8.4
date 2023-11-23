import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Sample data for different selections
data_dict = {
    'Owner': ['A', 'A', 'C', 'A', 'B'],
    'Article': ['Apple', 'Apple', 'Cherry', 'Tomato', 'Elderberry'],
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

# Create a Streamlit app
st.title('Custom Step Size on X-axis - Bar Chart')

# Set the figure size
plt.figure(figsize=(8, 4))

# Create a bar chart using Matplotlib
plt.bar(df['X'], df['Y'], width=step_size, align='edge')

# Set the x-axis ticks with the desired step size
x_ticks = np.arange(df['X'].min(), df['X'].max() + 1, step_size)
plt.xticks(x_ticks)

# Display the plot using Streamlit
st.pyplot(plt)

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
    'Article': ['Apple', 'Apple', 'Cherry', 'Tomato', 'Elderberry'],
    'Quantity': [10, 5, 7, 3, 2],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit'],
    'Owner': ['A', 'A', 'C', 'A', 'B'],
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
    selected_owner = st.selectbox('Select an owner:', owners_list)
    st.write(f'Selected owner: {selected_owner}')
    
    # Filter and calculate total count of products belonging to the selected owner
    owner_products = df[df['Owner'] == selected_owner]
    total_count_dict = owner_products.groupby('Article')['Quantity'].sum().to_dict()
    
    st.write(f'Total count of products owned by {selected_owner}:')
    
    for article, total_count in total_count_dict.items():
        st.write(f'{article}: {total_count}')

elif selection_option == 'Expires soon':
    expiration_threshold = datetime.now() + timedelta(days=2)
    expiring_articles = df[df['Expiration Date'] <= expiration_threshold]['Article'].tolist()
    st.write("Articles that expire soon:")
    st.write(expiring_articles)