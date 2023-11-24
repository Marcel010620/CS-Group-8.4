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
st.title('Dropdown Selection and Bar Chart')

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
    next_7_days = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
    next_7_days_str = [date.date() for date in next_7_days]
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date'])
    chart_df = df[df['Expiry Date'].dt.date.isin(next_7_days_str)].groupby('Expiry Date').size().reset_index(name='Count')
    chart_df = chart_df.head(5)  # Limit to 5 bars
    x_title, y_title = 'Expiry Date', 'Count'

# Create a bar chart with Altair
chart = alt.Chart(chart_df).mark_bar(size=30).encode(  # Adjust the size as needed
    x=alt.X(f'{x_title}:O', title=x_title),
    y=alt.Y(f'{y_title}:Q', title=y_title),
    color=alt.value('blue'),
    tooltip=[x_title, y_title, alt.Tooltip('Expiry Date:T', format='%Y-%m-%d')]
)

# Apply changes only when 'Expiry Date' is chosen
if selected_option == 'Expiry Date':
    chart = chart.transform_impute(
        impute='Count',
        key='Expiry Date',
        value=0
    ).encode(
        x=alt.X(f'{x_title}:T', title=x_title, axis=alt.Axis(labels=True, format='%d/%m')),
    ).transform_filter(
        alt.datum.Count > 0
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