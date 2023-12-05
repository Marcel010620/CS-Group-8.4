import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from google.oauth2 import service_account

# Get the absolute path to the directory containing your script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file
json_path = os.path.join(script_dir, "projekt-cs-32b2fba1e1ff.json")

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file(json_path, scopes=scope)


# Open the Google Sheets file by URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1CLDAFhtriXEMnylxTfOqF27-GH5S9hXELq0WCl-8kb4/edit#gid=0"
spreadsheet = client.open_by_url(spreadsheet_url)

# Get the data from the Google Sheets
worksheet = spreadsheet.get_worksheet(0)  # assuming data is in the first worksheet
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Ensure there are 15 different articles and 3 owners
owners = ['A', 'B', 'C']
df['Owner'] = df['Owner'].fillna(random.choice(owners))

# Create a Streamlit app
st.title('Fridge Overview')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', ['Owner', 'Article', 'Expiration'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

elif selected_option == 'Expiration':
    today = datetime.now()
    expiration_dates = [today + timedelta(days=i) for i in range(5)]
    df['Expiration Date'] = [random.choice(expiration_dates) for _ in range(len(df))]
    chart_df = df.groupby('Expiration Date').size().reset_index(name='Count')
    x_title, y_title = 'Expiration Date', 'Count'

# Create a bar chart with Altair
chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X(f'{x_title}:O', title=x_title),
    y=alt.Y(f'{y_title}:Q', title=y_title),
    color=alt.value('blue')
)

# Set chart properties
chart = chart.properties(
    width=400,
    title=f'Bar Chart - {selected_option}'
)

# Display the bar chart using Streamlit
st.altair_chart(chart, use_container_width=True)
