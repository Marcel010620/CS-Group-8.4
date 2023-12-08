import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from datetime import datetime
from collections import defaultdict
import altair as alt
import random

if 'inventory_list' not in st.session_state:
    st.session_state.inventory_list = []

# Google Sheets Authentifizierungs-Scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Pfad zu deiner JSON-Anmeldedatei
SERVICE_ACCOUNT_FILE = 'C:\\Users\\marce\\Documents\\Fridge\\projekt-cs-32b2fba1e1ff.json'

# Deine Spreadsheet-ID aus der URL deines Google Sheets
SPREADSHEET_ID = '1CLDAFhtriXEMnylxTfOqF27-GH5S9hXELq0WCl-8kb4'

# Name of the sheets in the Google Sheets file
OWNER_SHEET_NAME = 'Owner_Register'
INVENTORY_SHEET_NAME = 'Fridge_Inventory'

# Funktion, um die Credentials zu erstellen und den Google Sheets Client zu autorisieren
def authenticate_gspread():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    return gc

# Funktion, um Daten von Google Sheets zu laden
def authenticate_gspread():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    return gc

# Function to write data to Google Sheets Owner Register
def write_to_google_sheets_Owner(data):
    gc = authenticate_gspread()

    # Open the Google Sheets document using its title
    document = gc.open_by_key(SPREADSHEET_ID)

    # Select the worksheet by title
    worksheet = document.worksheet('Owner_Register')

    # Append data to the worksheet
    worksheet.append_row(data)

# Function to write data to Google Sheets Owner Register
def write_to_google_sheets_inventory(data):
    gc = authenticate_gspread()

    # Open the Google Sheets document using its title
    document = gc.open_by_key(SPREADSHEET_ID)

    # Select the worksheet by title
    worksheet = document.worksheet('Fridge_Inventory')

    # Convert the date object to a string
    data[2] = data[2].strftime("%d.%m.%Y") if data[2] else None

    # Append data to the worksheet
    worksheet.append_row(data)
    

def remove_owner_row(owner_index):
    gc = authenticate_gspread()

    # Open the Google Sheets document using its title
    document = gc.open_by_key(SPREADSHEET_ID)

    # Select the worksheet by title (replace with the correct title)
    worksheet = document.worksheet(OWNER_SHEET_NAME)

    # Convert Int64Index to a list
    owner_index_list = owner_index.tolist()

    # Delete the rows at the specified indices
    worksheet.delete_rows(*[index + 2 for index in owner_index_list])  # Adding 2 because Google Sheets is 1-indexed and pandas is 0-indexed

def remove_item_row(item_index):
    gc = authenticate_gspread()

    # Open the Google Sheets document using its title
    document = gc.open_by_key(SPREADSHEET_ID)

    # Select the worksheet by title (replace with the correct title)
    worksheet = document.worksheet(INVENTORY_SHEET_NAME)

    # Convert Int64Index to a list
    item_index_list = item_index.tolist()

    # Delete the rows at the specified indices
    worksheet.delete_rows(*[index + 2 for index in item_index_list])  # Adding 2 because Google Sheets is 1-indexed and pandas is 0-indexed

gc = authenticate_gspread()

# Funktion, um Daten von Google Sheets zu laden
def load_data_from_sheet(gc, sheet_name):
    worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    values = worksheet.get_all_values()

    # Check if values list is not empty
    if values:
        data = pd.DataFrame(values[1:], columns=values[0])
    else:
        data = pd.DataFrame()

    return data



# Product details dictionary with codes, calories, and expiration days
product_details = {
        "Milk": {"Name": "Milk", "calories": "400", "Expiring_Days": 7},
        "Ham": {"Name": "Ham", "calories": "900", "Expiring_Days": 5},
        "Yogurt": {"Name": "Yogurt", "calories": "350", "Expiring_Days": 10},
        "Cheese": {"Name": "Cheese", "calories": "1200", "Expiring_Days": 15},
        "Cream": {"Name": "Cream", "calories": "1500", "Expiring_Days": 12},
        "Pepper": {"Name": "Pepper", "calories": "250", "Expiring_Days": 5},
        "Sausage": {"Name": "Sausage", "calories": "1800", "Expiring_Days": 8},
        "Carrots": {"Name": "Carrots", "calories": "300", "Expiring_Days": 14},
        "Cucumber": {"Name": "Cucumber", "calories": "100", "Expiring_Days": 5},
        "Chocolate": {"Name": "Chocolate", "calories": "3000", "Expiring_Days": 30},
        "Cake": {"Name": "Cake", "calories": "2500", "Expiring_Days": 7},
        "Butter": {"Name": "Butter", "calories": "3500", "Expiring_Days": 14},
        "Apple": {"Name": "Apple", "calories": "800", "Expiring_Days": 10},
        "Strawberries": {"Name": "Strawberries", "calories": "200", "Expiring_Days": 5},
        "Salad": {"Name": "Salad", "calories": "700", "Expiring_Days": 3},
    }


# Your add_owner function
def add_owner(gc, surname, last_name, date_of_birth, diet):
    worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(OWNER_SHEET_NAME)
    worksheet.append_row([surname, last_name, date_of_birth, diet])

# Initialize session state to set buttons to a certain default state
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {
        "Article": None,
        "Owner": None,
        "selected_button": None,
    }

# Initialize session state for both add_item_button and remove_item_button
if "text_input_items" not in st.session_state:
    st.session_state.text_input_items = {
        "Product_Name": None,
        "Owner": None,
        "Date": None,
        "selected_button_item": None,
        "selected_remove_item": None
    }

# Initialize session state for both add_owner_button and remove_owner_button
if "text_input_owners" not in st.session_state:
    st.session_state.text_input_owners = {
        "Surname": None,
        "Last_Name": None,
        "Date_of_Birth": None,
        "Diet": None,
        "selected_button_owner": None,
        "selected_remove_owner": None
    }

# Input the name of the fridge
wg_name = st.text_input("Your WG name")

# Display the title (name of the fridge) with a name given by a user input
st.markdown(f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>", unsafe_allow_html=True)

# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

# Initialize the add_item button
add_item_button = col1.button("Add product")

# Set the other buttons to False
if add_item_button:
    st.session_state.selected_options["selected_button"] = "add_item_button"
    st.session_state.text_input_items["selected_button_item"] = True
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the remove_item button
remove_item_button = col2.button("Remove Item")

# Set the other buttons to False
if remove_item_button:
    st.session_state.selected_options["selected_button"] = "remove_item_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = True
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the add_owner button
add_owner_button = col3.button("Add new Owner")

# Set the other buttons to False
if add_owner_button:
    st.session_state.selected_options["selected_button"] = "add_owner_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = True
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the remove_owner button
remove_owner_button = col4.button("Remove Owner")

# Set the other buttons to False
if remove_owner_button:
    st.session_state.selected_options["selected_button"] = "remove_owner_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = True

# What happens if you press the add_item_button
if add_item_button:
    st.session_state.text_input_items["selected_button_item"] = "add_item_button"

# Choose supported article
if st.session_state.text_input_items["selected_button_item"] == "add_item_button":
    st.session_state.text_input_items["Product_Name"] = st.selectbox(
        "Choose your Article",
        options=[
            "Milk", "Ham", "Yogurt", "Cheese", "Cream", "Pepper", "Sausage", "Carrots",
            "Cucumber", "Chocolate", "Cake", "Butter", "Apple", "Strawberries", "Salad",
        ],
        key="Options_article"
    )

    # Choose the owner from the owner register
    owners_data = load_data_from_sheet(gc, OWNER_SHEET_NAME)
    owners_surnames = owners_data["Surname"].tolist()
    selected_owner_surname_item = st.selectbox("Select Owner", owners_surnames, key="Options_owner")

    # Enter today's date
    st.session_state.text_input_items["Date"] = st.text_input(
        "Enter Date of Entry (Format: DD.MM.YYYY)",
        key="date_text_input",
    )

    # Confirm button
    confirm_add_item_button = st.button("Confirm item_add")

    if confirm_add_item_button:
        selected_product = st.session_state.text_input_items["Product_Name"]

        # Check if the selected article is in the product_details dictionary
        if selected_product in product_details:
            product_info = product_details[selected_product]
            product_name = product_info["Name"]
            calories = product_info["calories"]
            expiring_days = int(product_info["Expiring_Days"])
            owner = selected_owner_surname_item  # Use the selected owner from the dropdown
            entry_date_str = st.session_state.text_input_items["Date"]

            # Adjust the format string to match your date input format
            entry_date = datetime.strptime(entry_date_str, "%d.%m.%Y").date()

            item_id = random.randint(0, 999)  # Generate a random ID

            # Construct data to be stored
            data_to_store = [item_id, product_name, entry_date, expiring_days, owner, calories]

            # Write data to Google Sheets
            write_to_google_sheets_inventory(data_to_store)

            # Reset session state after confirming
            st.session_state.text_input_items = {
                "Product_Name": None,
                "Owner": None,
                "Date": None,
                "selected_button_item": None,
                "selected_remove_item": None
            }

            st.success("Item successfully added.")
        else:
            st.error("Invalid product selected. Please choose a valid product.")


if remove_item_button:
    st.session_state.text_input_items["selected_remove_item"] = "remove_item_button"

if st.session_state.text_input_items["selected_remove_item"] == "remove_item_button":
    # Load data from the inventory sheet
    item_data = load_data_from_sheet(gc, INVENTORY_SHEET_NAME)


    # Display a dropdown to select the owner
    selected_owner = st.selectbox("Select Owner", item_data['Owner'].unique())

    # Filter the item_data DataFrame based on the selected owner
    filtered_data = item_data[item_data['Owner'] == selected_owner]

    # Display a dropdown to select the item to remove with product name and expiration date
    selected_item_info = st.selectbox("Select Item to Remove", filtered_data.apply(lambda x: f"{x['Product name']} (Expiration Date: {x['Expiration Date']})", axis=1))

    print("Selected Item Info:", selected_item_info)  # Add this line to see the value of selected_item_info

    # Check if the selected item exists in the DataFrame
    if selected_item_info in filtered_data['Product name'].values:
        # Allow the user to confirm the removal
        if st.button(f"Remove 1 unit of {selected_item_info}"):
            st.success(f"Removing 1 unit of {selected_item_info}.")
            # Now you can update your DataFrame or perform other removal logic
    else:
        # You can choose to display a message here if needed
        pass

 


    # Extract the selected product name from the displayed information
    if selected_item_info is not None:
        selected_item_product_name = selected_item_info.split(' (Expiration Date: ')[0]
        print("Selected Item Product Name:", selected_item_product_name)  # Add this line to see the value of selected_item_product_name

    # Confirm button for removal
    confirm_remove_item_button = st.button("Confirm Item Removal")

    if confirm_remove_item_button:
        # Get the index of the selected item
        if selected_item_info is not None:
            item_index = item_data[item_data["Product name"] == selected_item_product_name].index

            # Remove the selected item's row from the Google Sheets
            remove_item_row(item_index)

            st.success("Item successfully removed.")

# What happens if you press the add_owner_button

if add_owner_button:
    st.session_state.text_input_owners["selected_button_owner"] = "add_owner_button"

# Text inputs for adding an owner
if st.session_state.text_input_owners["selected_button_owner"] == "add_owner_button":
    st.session_state.text_input_owners["Surname"] = st.text_input(
        "Enter Surname",
        key="surname_text_input",
    )
    st.session_state.text_input_owners["Last_Name"] = st.text_input(
        "Enter Last Name",
        key="last_name_text_input"
    )
    st.session_state.text_input_owners["Date_of_Birth"] = st.text_input(
        "Enter Date of Birth",
        key="date_of_birth_text_input"
    )
    st.session_state.text_input_owners["Diet"] = st.selectbox(
        "Choose Diet",
        options=("Vegan", "Vegetarian", "Rich in Proteins", "low calories", "low carbon", "None"),
        key="diet_text_input"
    )

    # Confirm button
    confirm_add_owner_button = st.button("Confirm Owner_add")
    if confirm_add_owner_button:
        # Extract data from session state
        data_to_store = [
            st.session_state.text_input_owners["Surname"],
            st.session_state.text_input_owners["Last_Name"],
            st.session_state.text_input_owners["Date_of_Birth"],
            st.session_state.text_input_owners["Diet"],
        ]

        # Write data to Google Sheets
        write_to_google_sheets_Owner(data_to_store)

        # Reset session state after confirming
        st.session_state.text_input_ownerss = {
            "Surname": None,
            "Last_Name": None,
            "Date_of_Birth": None,
            "Diet": None,
            "selected_button_owner": None,
            "selected_remove_owner": None
        }

        st.success("Owner successfully added.")

if remove_owner_button:
    st.session_state.text_input_owners["selected_remove_owner"] = "remove_owner_button"

# Dropdown to select owner for removal
if st.session_state.text_input_owners["selected_remove_owner"] == "remove_owner_button":
    owners_data = load_data_from_sheet(gc, OWNER_SHEET_NAME)
    owners_surnames = owners_data["Surname"].tolist()
    selected_owner_surname = st.selectbox("Select Owner to Remove", owners_surnames)

    # Confirm button for removal
    confirm_remove_button = st.button("Confirm Owner Removal")
    if confirm_remove_button:
        if st.session_state.text_input_owners["selected_remove_owner"] == "remove_owner_button":
            # Get the index of the selected owner
            owner_index = owners_data[owners_data["Surname"] == selected_owner_surname].index

            # Remove the selected owner's row from the Google Sheets
            remove_owner_row(owner_index)

            st.success("Owner successfully removed.")

# Initialize 2 columns to order 2 buttons in a row
col1, col2, col3, col4 = st.columns(4)
# Button to show/hide the entire inventory
show_inventory_button = col1.button("Show Inventory")

if show_inventory_button:
    # Load data from the inventory sheet
    inventory_data = load_data_from_sheet(gc, INVENTORY_SHEET_NAME)

    # Display the entire inventory
    st.write("## Inventory Data")
    st.table(inventory_data)

# Button to hide the inventory
hide_inventory_button = col2.button("Hide Inventory")

if hide_inventory_button:
    # Clear the displayed inventory
    st.text("")  # You can use other methods to clear or hide the inventory display



# BAR CHART

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import random

# Sample data for different selections from the second code
data = {
    'Article': ['Milk', 'Ham', 'Yogurt', 'Cheese', 'Cream', 'Pepper', 'Sausage', 'Carrots', 'Cucumber', 'Chocolate', 'Cake', 'Butter', 'Apple', 'Strawberries', 'Salad'],
    'Quantity': [10, 5, 7, 3, 2, 8, 6, 4, 9, 5, 7, 3, 6, 4, 5],
}

# Ensure there are 15 different articles and 3 owners
owners = ['A', 'B', 'C']
data['Owner'] = [random.choice(owners) for _ in range(len(data['Article']))]

# Create a DataFrame with a separate row for each unit
rows = []
for i in range(len(data['Article'])):
    units = data['Quantity'][i]
    for _ in range(units):
        row = {
            'Article': data['Article'][i],
            'Quantity': 1,  # Count each unit as 1
            'Owner': data['Owner'][i],
        }
        rows.append(row)

df = pd.DataFrame(rows)

# Expand the DataFrame to have one row for each unique combination of Article and Owner
expanded_df = df.explode('Owner')

# Create a Streamlit app
st.title('Fridge Overview')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', ['Owner', 'Article', 'Expiration'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = expanded_df.groupby('Article').size().reset_index(name='Count')
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


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# Sample data for different selections
data = {
    'Article': ['Milk', 'Ham', 'Yogurt', 'Cheese', 'Cream', 'Pepper', 'Sausage', 'Carrots', 'Cucumber', 'Chocolate', 'Cake', 'Butter', 'Apple', 'Strawberries', 'Salad'],
    'Quantity': [10, 5, 7, 3, 2, 8, 6, 4, 9, 5, 7, 3, 6, 4, 5],
    'Owner': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'Expiration Date': ['20231206', '20231207', '20231208', '20231209', '20231210', '20231211', '20231206', '20231206', '20231208', '20231215', '20231208', '20231217', '20231218', '20231219', '20231220'],
}

df = pd.DataFrame(data)

# Create a Streamlit app
st.title('Ownership')

# Select an owner from the dropdown
owners_list = df['Owner'].unique()
selected_owner = st.selectbox('Select an owner:', owners_list)
st.write(f'Selected owner: {selected_owner}')

# Filter and calculate total count of products belonging to the selected owner
owner_products = df[df['Owner'] == selected_owner]
total_count_dict = owner_products.groupby('Article')['Quantity'].sum().to_dict()

st.write(f'Total count of products owned by {selected_owner}:')

for article, total_count in total_count_dict.items():
    st.write(f'{article}: {total_count}')




# Convert 'Expiration Date' column to datetime type and round down to the nearest day
df['Expiration Date'] = pd.to_datetime(df['Expiration Date']).dt.floor('D')

# Create a Streamlit app
st.title('Expires soon')

# Calculate the date range for the next 5 days, including today
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

# Create an empty DataFrame with date columns
result_df = pd.DataFrame(index=['Products'], columns=date_range)

# Populate the DataFrame with product names expiring in the next 5 days
for date in date_range:
    expiring_articles = df[df['Expiration Date'] == date]
    result_df[date]['Products'] = ', '.join(expiring_articles['Article'].tolist())

# Display the DataFrame
st.table(result_df.T)

