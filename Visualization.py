from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import altair as alt
import random

# Sample data for different selections
data = {
    'Article': ['Apple', 'Orange', 'Cherry', 'Tomato', 'Elderberry', 'Banana', 'Grapes', 'Strawberry', 'Pineapple', 'Watermelon', 'Mango', 'Peach', 'Kiwi', 'Blueberry', 'Raspberry'],
    'Quantity': [10, 5, 7, 3, 2, 8, 6, 4, 9, 5, 7, 3, 6, 4, 5],
}

# Ensure there are 15 different articles and 3 owners
owners = ['A', 'B', 'C']
data['Owner'] = [random.choice(owners) for _ in range(len(data['Article']))]

# Create a DataFrame with a separate row for each unit and a unique expiration date
rows = []
for i in range(len(data['Article'])):
    expiration_dates = [datetime.now() + timedelta(days=random.randint(1, 7)) for _ in range(data['Quantity'][i])]
    for expiration_date in expiration_dates:
        row = {
            'Article': data['Article'][i],
            'Quantity': 1,
            'Owner': data['Owner'][i],
            'Expiration Date': expiration_date,
        }
        rows.append(row)

df = pd.DataFrame(rows)

# Expand the DataFrame to have one row for each unique combination of Article and Expiration Date
expanded_df = df.explode('Expiration Date')

# Create a Streamlit app
st.title('Fridge Overview')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', ['Owner', 'Article', 'Expiration Date'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    # Store the DataFrame outside the block to keep it constant
    chart_df_owner = df.groupby('Owner').size().reset_index(name='Count')
    x_title_owner, y_title_owner = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = expanded_df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

elif selected_option == 'Expiration Date':
    # Create a new DataFrame for the selected Expiration Date
    next_7_days = [datetime.now() + timedelta(days=i) for i in range(7)]
    next_7_days_str = [date.date() for date in next_7_days]
    chart_df = expanded_df[expanded_df['Expiration Date'].dt.date.isin(next_7_days_str)].groupby(['Expiration Date']).size().reset_index(name='Count')
    x_title, y_title = 'Expiration Date', 'Count'

# Create a bar chart with Altair
if selected_option == 'Owner':
    chart = alt.Chart(chart_df_owner).mark_bar().encode(
        x=alt.X(f'{x_title_owner}:O', title=x_title_owner),
        y=alt.Y(f'{y_title_owner}:Q', title=y_title_owner),
        color=alt.value('blue'),
        tooltip=[x_title_owner, y_title_owner]
    )
else:
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X(f'{x_title}:O', title=x_title),
        y=alt.Y(f'{y_title}:Q', title=y_title),
        color=alt.value('blue'),
        tooltip=[x_title, y_title, alt.Tooltip('Expiration Date:T', format='%Y-%m-%d')]
    )

# Apply changes only when 'Expiration Date' is chosen
if selected_option == 'Expiration Date':
    chart = chart.encode(
        x=alt.X(f'{x_title}:T', title=x_title, axis=alt.Axis(labels=True, format='%d/%m')),
    )

# Set chart properties
chart = chart.properties(
    width=400,
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
st.title('Ownership')

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