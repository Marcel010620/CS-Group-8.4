# Content of the Code
# Section 1: Import all relevant libraries [from 15 to 26]
# Section 2: API connection to the database [from 27 to 44]
# Section 3: Functions [from 45 to 107]
# Section 4: Product List with all the attributes the different products have [from 108 to 127]
# Section 5: Initialization of the session state to the different input fields [from 128 to 154]
# Section 6: Text and Welcome Messages [from 155 to 205]
# Section 7: User input [from 206 to 500]
# Section 8: Visualization [from 501 to 546]
# Section 9: Interactive Owner and Ownership analysis [from 547 to 581]
# Section 10: User Output on Expiration Overview [from 582 to 631]
# Section 11: Inventory [from 632 to 676]


#### Section 1: Import all relevant libraries ####

from datetime import datetime, timedelta
import random
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import altair as alt



#### Section 2: API connection to the database ####

# Initialization of the library and API connection to the database
# (Path to JSON file, Spreadsheet ID from URL, authentication scope, and name of Google Sheet)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SERVICE_ACCOUNT_FILE = (
    "C:\\Users\\marce\\Documents\\Fridge\\projekt-cs-32b2fba1e1ff.json"
)
SPREADSHEET_ID = "1CLDAFhtriXEMnylxTfOqF27-GH5S9hXELq0WCl-8kb4"
OWNER_SHEET_NAME = "Owner_Register"
INVENTORY_SHEET_NAME = "Fridge_Inventory"


#### Section 3: Functions ####

# Function to create the credentials and authorize the Google Sheets client
def authenticate_gspread():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    gc = gspread.authorize(credentials)
    return gc

# Define the Autentication globally so it doesn't have to be mentioned every time
gc = authenticate_gspread()

# Function to get the worksheet from the Google Sheets
def get_worksheet(sheet_name):
    document = gc.open_by_key(SPREADSHEET_ID)
    worksheet = document.worksheet(sheet_name)
    return worksheet

# Function to write data to the Google Sheets Owner Register
def write_to_google_sheets_Owner(data):
    worksheet = get_worksheet(OWNER_SHEET_NAME)
    worksheet.append_row(data)

# Function to write data to the Google Sheets Inventory and format the inserted date to dd.mm.YYYY
def write_to_google_sheets_inventory(data):
    worksheet = get_worksheet(INVENTORY_SHEET_NAME)
    data[2] = data[2].strftime("%d.%m.%Y") if data[2] else None
    worksheet.append_row(data)

# Function to remove the chosen owner by deleting the row in the Google Sheet (Owner_Register)
def remove_owner_row(owner_index):
    worksheet = get_worksheet(OWNER_SHEET_NAME)
    owner_index_list = owner_index.tolist()
    worksheet.delete_rows(*[index + 2 for index in owner_index_list])
    # Adding 2 because Google Sheets is 1-indexed and pandas is 0-indexed

# Function to remove the chosen item by deleting the row in the Google Sheet (Fridge_Inventory)
def remove_item_row(item_index):
    worksheet = get_worksheet(INVENTORY_SHEET_NAME)
    item_index_list = item_index.tolist()
    worksheet.delete_rows(*[index + 2 for index in item_index_list])
    # Adding 2 because Google Sheets is 1-indexed and pandas is 0-indexed

# Function to load data from the Google Sheets and check if the values in the list are not empty
def load_data_from_sheet(sheet_name):
    worksheet = get_worksheet(sheet_name)
    values = worksheet.get_all_values()

    if values:
        data = pd.DataFrame(values[1:], columns=values[0])
    else:
        data = pd.DataFrame()

    return data

# Function to add a new owner with the attributes of surname, last name, date of birth, and diet
def add_owner(surname, last_name, date_of_birth, diet):
    worksheet = get_worksheet(OWNER_SHEET_NAME)
    worksheet.append_row([surname, last_name, date_of_birth, diet])



#### Section 4: Product List with all the attributes the different products have ####
    
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

#### Section 5: Initialization of the session state to the different input fields ####

# Initialize session state for the top 4 buttons add_item, remove_item, add_owner and remove_onwer
if "top_buttons" not in st.session_state:
    st.session_state.top_buttons = {"selected_button": None}

# Initialize session state for both add_item_button and remove_item_button
if "text_input_items" not in st.session_state:
    st.session_state.text_input_items = {
        "Product_Name": None,
        "Owner": None,
        "Date": None,
        "selected_button_item": None,
        "selected_remove_item": None,
    }

# Initialize session state for both add_owner_button and remove_owner_button
if "text_input_owners" not in st.session_state:
    st.session_state.text_input_owners = {
        "Surname": None,
        "Last_Name": None,
        "Date_of_Birth": None,
        "Diet": None,
        "selected_button_owner": None,
        "selected_remove_owner": None,
    }

#### Section 6: Text and Welcome Messages ####
    
# Initalize Columns
# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

new_fridge_name = col4.text_input("Change Fridge Name")
fridge_name = "CoolPythonator" if not new_fridge_name else new_fridge_name

# Display the updated fridge_name in the markdown row
st.markdown(f"# Welcome to {fridge_name}!")

# Input the name of the fridge
users_data = load_data_from_sheet(OWNER_SHEET_NAME)
users_surnames = users_data["Surname"].tolist()
selected_owner_surname = st.selectbox(
    f"Who is using the {fridge_name} today?", users_surnames
)

# Display the title (name of the fridge) with a name given by a user input
st.markdown(
    f"## How are you doing <span style='color:brown;'>{selected_owner_surname}</span>?",
    unsafe_allow_html=True,
)

# Get the current weekday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday) for daily Slogan
current_date = datetime.now()
weekday = current_date.weekday()

# Define slogans for each weekday
weekday_slogans = {
    0: "Monday Motivation: Embrace the challenges!🚀",
    1: "Terrific Tuesday: Shine bright!🔆",
    2: "Wonderful Wednesday: halfway there!✅",
    3: "Thoughtful Thursday: kindness matters!🫶",
    4: "Fantastic Friday: let the weekend begin!🍾",
    5: "Super Saturday: enjoy and relax!☕",
    6: "Sunday Funday: make memories!☀️",
}

# Get the slogan for the current weekday
current_slogan = weekday_slogans.get(weekday, "Have a great day!")

# Display the slogan
st.write(
    f"<span style='color:brown;'><b>Today's Slogan to get motivated: {current_slogan}</b></span>",
    unsafe_allow_html=True,
)
# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

#### Section 7: User input ####

# Initialize the add_item button
add_item_button = col1.button("Add product")

# Set the other buttons to False if the add_item_button is pressed so that
# they will disappear
if add_item_button:
    st.session_state.top_buttons["selected_button"] = "add_item_button"
    st.session_state.text_input_items["selected_button_item"] = True
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the remove_item button
remove_item_button = col2.button("Remove Item")

# Set the other buttons to False if the remove_item_button is pressed so
# that they will disappear
if remove_item_button:
    st.session_state.top_buttons["selected_button"] = "remove_item_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = True
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the add_owner button
add_owner_button = col3.button("Add new Owner")

# Set the other buttons to False if the add_owner_button is pressed so
# that they will disappear
if add_owner_button:
    st.session_state.top_buttons["selected_button"] = "add_owner_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = True
    st.session_state.text_input_owners["selected_remove_owner"] = False

# Initialize the remove_owner button
remove_owner_button = col4.button("Remove Owner")

# Set the other buttons to False if the remove_owner_button is pressed so
# that they will disappear
if remove_owner_button:
    st.session_state.top_buttons["selected_button"] = "remove_owner_button"
    st.session_state.text_input_items["selected_button_item"] = False
    st.session_state.text_input_items["selected_remove_item"] = False
    st.session_state.text_input_owners["selected_button_owner"] = False
    st.session_state.text_input_owners["selected_remove_owner"] = True

# What happens if you press the add_item_button

# Set the session state to True
if add_item_button:
    st.session_state.text_input_items["selected_button_item"] = "add_item_button"

# Create a dropdown field (selectbox) where the user can choose from one
# of the supported products listed in section 4 of this code
if st.session_state.text_input_items["selected_button_item"] == "add_item_button":
    st.session_state.text_input_items["Product_Name"] = st.selectbox(
        "Choose your Article",
        options=[
            "Milk",
            "Ham",
            "Yogurt",
            "Cheese",
            "Cream",
            "Pepper",
            "Sausage",
            "Carrots",
            "Cucumber",
            "Chocolate",
            "Cake",
            "Butter",
            "Apple",
            "Strawberries",
            "Salad",
        ],
        key="Options_article",
    )

    # Load the surnames of the current owners in the database so that the user can choose which of them is the owner of the product
    owners_data = load_data_from_sheet(OWNER_SHEET_NAME)
    owners_surnames = owners_data["Surname"].tolist()
    selected_owner_surname_item = st.selectbox(
        "Select Owner", owners_surnames, key="Options_owner"
    )

    # Insert a textfield where the user inserts the date of entry
    st.session_state.text_input_items["Date"] = st.text_input(
        "Enter Date of Entry (Format: DD.MM.YYYY)",
        key="date_text_input",
    )

    # Initialize a confirm button to actually store the inserted date in the
    # database
    confirm_add_item_button = st.button("Confirm")

    if confirm_add_item_button:
        selected_product = st.session_state.text_input_items["Product_Name"]

        # Check if the selected article is in the product_details dictionary
        # and get all the data from the user input and the product list
        if selected_product in product_details:
            product_info = product_details[selected_product]
            product_name = product_info["Name"]
            calories = product_info["calories"]
            expiring_days = int(product_info["Expiring_Days"])
            owner = (
                selected_owner_surname_item  # Use the selected owner from the dropdown
            )
            entry_date_str = st.session_state.text_input_items["Date"]

            # Adjust the format string to match your date input format
            entry_date = datetime.strptime(entry_date_str, "%d.%m.%Y").date()

            item_id = random.randint(0, 999)  # Generate a random ID

            # Construct data to be stored
            data_to_store = [
                item_id,
                product_name,
                entry_date,
                expiring_days,
                owner,
                calories,
            ]

            # Write data to Google Sheets
            write_to_google_sheets_inventory(data_to_store)

            # Reset session state after confirming
            st.session_state.text_input_items = {
                "Product_Name": None,
                "Owner": None,
                "Date": None,
                "selected_button_item": None,
                "selected_remove_item": None,
            }

            st.success("Item successfully added.")


# What happens if you press the remove_item_button

# Set the session state to True
if remove_item_button:
    st.session_state.text_input_items["selected_remove_item"] = "remove_item_button"

if st.session_state.text_input_items["selected_remove_item"] == "remove_item_button":
    # Load data from the inventory sheet
    item_data = load_data_from_sheet(INVENTORY_SHEET_NAME)

    # Display a dropdown to select the owner
    selected_owner = st.selectbox("Select Owner", item_data["Owner"].unique())

    # Filter the item_data DataFrame based on the selected owner
    filtered_data = item_data[item_data["Owner"] == selected_owner]

    # Display a dropdown to select the item to remove with product name and
    # expiration date
    selected_item_info = st.selectbox(
        "Select Item to Remove",
        filtered_data.apply(
            lambda x: f"{x['Product name']} (Expiration Date: {x['Expiration Date']})",
            axis=1,
        ),
    )

    print(
        "Selected Item Info:", selected_item_info
    )  # To see the value of selected_item_info

    # Check if the selected item exists in the DataFrame
    if selected_item_info in filtered_data["Product name"].values:
        # Allow the user to confirm the removal
        if st.button(f"Remove 1 unit of {selected_item_info}"):
            st.success(f"Removing 1 unit of {selected_item_info}.")
            # Now you can update your DataFrame or perform other removal logic
    else:
        pass

    # Extract the selected product name from the displayed information
    if selected_item_info is not None:
        selected_item_product_name = selected_item_info.split(
            " (Expiration Date: ")[0]
        print("Selected Item Product Name:", selected_item_product_name)

    # Confirm button for removal
    confirm_remove_item_button = st.button("Confirm")

    if confirm_remove_item_button:
        # Get the index of the selected item
        if selected_item_info is not None:
            item_index = item_data[
                item_data["Product name"] == selected_item_product_name
            ].index

            # Remove the selected item's row from the Google Sheets
            remove_item_row(item_index)

            st.success("Item successfully removed.")


# What happens if you press the add_owner_button

# Set the session state to True
if add_owner_button:
    st.session_state.text_input_owners["selected_button_owner"] = "add_owner_button"

# Text inputs for adding an owner
if st.session_state.text_input_owners["selected_button_owner"] == "add_owner_button":
    st.session_state.text_input_owners["Surname"] = st.text_input(
        "Enter Surname",
        key="surname_text_input",
    )
    st.session_state.text_input_owners["Last_Name"] = st.text_input(
        "Enter Last Name", key="last_name_text_input"
    )
    st.session_state.text_input_owners["Date_of_Birth"] = st.text_input(
        "Enter Date of Birth", key="date_of_birth_text_input"
    )
    st.session_state.text_input_owners["Diet"] = st.selectbox(
        "Choose Diet",
        options=(
            "Vegan",
            "Vegetarian",
            "Rich in Proteins",
            "low calories",
            "low carbs",
            "None",
        ),
        key="diet_text_input",
    )

    # Confirm button
    confirm_add_owner_button = st.button("Confirm")
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
            "selected_remove_owner": None,
        }

        st.success("Owner successfully added.")


# What happens if you press the remove_owner_button

# Set the session state to True
if remove_owner_button:
    st.session_state.text_input_owners["selected_remove_owner"] = "remove_owner_button"

# Dropdown to select owner for removal
if st.session_state.text_input_owners["selected_remove_owner"] == "remove_owner_button":
    owners_data = load_data_from_sheet(OWNER_SHEET_NAME)
    owners_surnames = owners_data["Surname"].tolist()
    selected_owner_surname = st.selectbox(
        "Select Owner to Remove", owners_surnames)

    # Confirm button for removal
    confirm_remove_button = st.button("Confirm")
    if confirm_remove_button:
        if (
            st.session_state.text_input_owners["selected_remove_owner"]
            == "remove_owner_button"
        ):
            # Get the index of the selected owner
            owner_index = owners_data[
                owners_data["Surname"] == selected_owner_surname
            ].index

            # Remove the selected owner's row from the Google Sheets
            remove_owner_row(owner_index)

            st.success("Owner successfully removed.")

st.markdown("---")


#### Section 8: Visualization ####

# Creating a Bar chart for Owner and Product Overview #

#Setting a Head Title
st.markdown("## Owner and Product Overview")

# Load data from Google Sheets
owners_data = load_data_from_sheet(OWNER_SHEET_NAME)
inventory_data = load_data_from_sheet(INVENTORY_SHEET_NAME)

# Create a dropdown to select an option
selected_option = st.selectbox("Select an option:", ["Owner", "Product name"])

# Check if 'Owner' or 'Product name' column exists in inventory_data
if selected_option == "Owner" and "Owner" in inventory_data.columns:
    # Create a bar chart for Owner data
    chart_df = inventory_data.groupby("Owner").size().reset_index(name="Count")
    x_title, y_title = "Owner", "Count"
elif selected_option == "Product name" and "Product name" in inventory_data.columns:
    # Create a bar chart for Product name data
    chart_df = inventory_data.groupby(
        "Product name").size().reset_index(name="Count")
    x_title, y_title = "Product name", "Count"
else:
    st.warning(f"The '{selected_option}' column is not present in the data.")

# Setting the chart properties of the Altair Chart
chart = (
    alt.Chart(chart_df)
    .mark_bar()
    .encode(
        x=alt.X(f"{x_title}:O", title=x_title),
        y=alt.Y(f"{y_title}:Q", title=y_title),
        color=alt.value("brown"),
    )
    .properties(
        width=400,
    )
)

#Generate and display the chart
st.subheader(f"Bar Chart for {selected_option} Data:")
st.altair_chart(chart, use_container_width=True)


#### Section 9: Interactive Owner and Ownership analysis ####

# Display the products sorted by the different owners. Therefore an Owner exactly knows her Inventory within the Fridge

# Load data from Google Sheets
df_inventory = load_data_from_sheet(INVENTORY_SHEET_NAME)
df_owner = load_data_from_sheet(OWNER_SHEET_NAME)

#Creating a horizontal separator line
st.markdown("---")

# Create a Streamlit app
st.markdown("## Product Ownership")

# Select an owner from the dropdown
owners_list = df_owner["Surname"].unique()
selected_owner = st.selectbox("Select an owner:", owners_list)
st.write(f"Selected owner: {selected_owner}")

# Filter and count the occurrences of each article belonging to the selected owner in the inventory sheet
owner_inventory = df_inventory[df_inventory["Owner"] == selected_owner]
article_counts = owner_inventory["Product name"].value_counts().to_dict()

#Display the Articles of the chosen Owner
st.write(f"Article counts owned by {selected_owner} in Inventory:")

#Count the units of articles
for article, count in article_counts.items():
    st.write(f"{article}: {count}")

# Additional information about the selected owner from the owner sheet
owner_info = df_owner[df_owner["Surname"] == selected_owner]
st.subheader(f"Additional information about {selected_owner}:")
st.write(owner_info)

#### Section 10: User Output on Expiration Overview ####

#Creating a horizontal separator line
st.markdown("---")

# Create a Title
st.markdown("## Expires soon")

# In here the goal is to display the products with close Expiration date so those products get used soon

# Load data from Google Sheets
df_inventory = load_data_from_sheet(INVENTORY_SHEET_NAME)

# Convert 'Expiration Date' column to datetime type and round down to the nearest day
df_inventory["Expiration Date"] = pd.to_datetime(
    df_inventory["Expiration Date"], format="%d.%m.%Y"
).dt.floor("D")


# Calculate the date range for the next 5 days, including today
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
date_range = [(today + timedelta(days=i)).strftime("%d.%m.%Y")
              for i in range(5)]

# Create an empty DataFrame with a single row
result_df = pd.DataFrame(index=["Products"], columns=date_range)

# Populate the DataFrame with product names and quantities expiring in the next 5 days
for date in date_range:
    # Filter the DataFrame for items expiring on the current date
    expiring_articles = df_inventory[df_inventory["Expiration Date"] == date]

    # Check if there are any expiring articles on the current date
    if not expiring_articles.empty:
        grouped_data = (
            expiring_articles.groupby("Product name")
            .size()
            .reset_index(name="Quantity")
        )

        # Initialize an empty string to store the product names and quantities
        products_str = ""
        # Iterate through the grouped data and construct the string
        for _, row in grouped_data.iterrows():
            products_str += f"{row['Product name']} (Qty: {row['Quantity']})\n"

        # Store the constructed string in the result DataFrame under the current date
        result_df[date]["Products"] = products_str


#### Section 11: Inventory ####

# Display the DataFrame as a left-aligned table. Missing values get replaced by empty strings.
st.table(result_df.fillna("").style.set_properties(**{"text-align": "left"}))

#Creating a horizontal separator line
st.markdown("---")

# Create a Title
st.markdown("## Display whole Inventory")

# Initialize 2 columns to order 2 buttons in a row
col1, col2, col3, col4 = st.columns(4)

# Button to show/hide the entire inventory
show_inventory_button = col1.button("Show Inventory")

# What happens if you press the show_inventory_button
if show_inventory_button:
    # Columns to show
    columns_to_show = ["Owner", "Product name", "Expiration Date"]

    # Load data from the inventory sheet
    inventory_data = load_data_from_sheet(INVENTORY_SHEET_NAME)

    # Group by 'Owner' and 'Product', then sort by 'Expiration Date'
    grouped_data = (
        inventory_data.groupby(["Owner", "Product name"])
        .apply(lambda x: x.sort_values("Expiration Date"))
        .reset_index(drop=True)
    )

    # Select only the specified columns
    selected_columns_data = grouped_data[columns_to_show]

    # Display the selected columns in a table
    st.table(selected_columns_data)


# Button to hide the inventory
hide_inventory_button = col2.button("Hide Inventory")

if hide_inventory_button:
    # Clear the displayed inventory
    st.text("")  # You can use other methods to clear or hide the inventory display
