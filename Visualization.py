import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import random

# Sample data for different selections
data_dict = {
    'Owner': ['A', 'A', 'C', 'A', 'B', 'C', 'B', 'A', 'D', 'D', 'B', 'C', 'D', 'B', 'C'],
    'Article': ['Apple', 'Orange', 'Cherry', 'Tomato', 'Elderberry', 'Banana', 'Cherry', 'Apple', 'Orange', 'Grapes', 'Banana', 'Cherry', 'Orange', 'Grapes', 'Milk'],
}

# Make sure the number of expiry dates matches the number of articles
expiry_dates = [datetime.now() + timedelta(days=random.randint(1, 7)) for _ in range(len(data_dict['Article']))]
data_dict['Expiry Date'] = [date.date() for date in expiry_dates]

df = pd.DataFrame(data_dict)

# Create a Streamlit app
st.title('Fridge Overview')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', ['Owner', 'Article', 'Expiry Date'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

elif selected_option == 'Expiry Date':
    next_5_days = [datetime.now() + timedelta(days=i) for i in range(1, 6)]
    next_5_days_str = [date.date() for date in next_5_days]
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date'])
    chart_df = df[df['Expiry Date'].dt.date.isin(next_5_days_str)].groupby(df['Expiry Date'].dt.date).size().reset_index(name='Count')

# Create a bar chart with Altair
chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X(f'{x_title}:O', title=x_title),
    y=alt.Y(f'{y_title}:Q', title=y_title),
    color=alt.value('blue'),
    tooltip=[x_title, y_title, alt.Tooltip('Expiry Date:T', format='%Y-%m-%d')]
)

# Set chart properties
chart = chart.properties(
    width=400,
    title=f'Bar Chart - {selected_option}'
)

# Display the bar chart using Streamlit
st.altair_chart(chart, use_container_width=True)


from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import altair as alt

# Sample data for different selections
data = {
    'Article': ['Apple', 'Apple', 'Cherry', 'Tomato', 'Elderberry', 'Apple', 'Apple'],
    'Quantity': [10, 5, 7, 3, 2, 4, 6],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit'],
    'Owner': ['A', 'A', 'C', 'A', 'B', 'A', 'B'],
    'Expiration Date': [
        datetime(2023, 12, 1),
        datetime(2023, 12, 3),
        datetime(2023, 12, 5),
        datetime(2023, 11, 25),
        datetime(2023, 12, 7),
        datetime(2023, 12, 8),
        datetime(2023, 12, 10),
    ],
}

# Create a DataFrame with a separate row for each unit with its own expiration date
rows = []
for i in range(len(data['Article'])):
    for j in range(data['Quantity'][i]):
        row = {
            'Article': data['Article'][i],
            'Quantity': 1,
            'Category': data['Category'][i],
            'Owner': data['Owner'][i],
            'Expiration Date': data['Expiration Date'][i],
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
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = expanded_df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

elif selected_option == 'Expiration Date':
    # Create a new DataFrame for the selected Expiration Date
    next_5_days = [datetime.now() + timedelta(days=i) for i in range(1, 6)]
    next_5_days_str = [date.date() for date in next_5_days]
    chart_df = expanded_df[expanded_df['Expiration Date'].dt.date.isin(next_5_days_str)].groupby(['Expiration Date']).size().reset_index(name='Count')
    chart_df = chart_df.head(5) if not chart_df.empty else chart_df  # Limit to 5 bars
    x_title, y_title = 'Expiration Date', 'Count'

# Create a bar chart with Altair
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
