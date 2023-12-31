# Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict
import altair as alt
import random

# Initialize inventory list in session state to save data entries
if "inventory_list" not in st.session_state:
    st.session_state.inventory_list = []

# Define the Product class
class Product:
    def __init__(self, name, product_code, calories, expiry_days, quantity=1):
        self.name = name
        self.product_code = product_code
        self.calories = calories
        self.expiry_days = expiry_days
        self.quantity = quantity

# Function to generate a product code based on the article and owner
def generate_product_code(article, owner):
    # Product details dictionary with codes, calories, and expiration days
    product_details = {
        "Milk": {"Product_Code": "01", "calories": "0400", "Expiring_Days": 7},
        "Ham": {"Product_Code": "02", "calories": "0900", "Expiring_Days": 5},
        "Yogurt": {"Product_Code": "03", "calories": "0350", "Expiring_Days": 10},
        "Cheese": {"Product_Code": "04", "calories": "1200", "Expiring_Days": 15},
        "Cream": {"Product_Code": "05", "calories": "1500", "Expiring_Days": 12},
        "Pepper": {"Product_Code": "06", "calories": "0250", "Expiring_Days": 5},
        "Sausage": {"Product_Code": "07", "calories": "1800", "Expiring_Days": 8},
        "Carrots": {"Product_Code": "08", "calories": "0300", "Expiring_Days": 14},
        "Cucumber": {"Product_Code": "09", "calories": "0100", "Expiring_Days": 5},
        "Chocolate": {"Product_Code": "10", "calories": "3000", "Expiring_Days": 30},
        "Cake": {"Product_Code": "11", "calories": "2500", "Expiring_Days": 7},
        "Butter": {"Product_Code": "12", "calories": "3500", "Expiring_Days": 14},
        "Apple": {"Product_Code": "13", "calories": "0800", "Expiring_Days": 10},
        "Strawberries": {"Product_Code": "14", "calories": "0200", "Expiring_Days": 5},
        "Salad": {"Product_Code": "15", "calories": "0700", "Expiring_Days": 3},
    }

    today = datetime.today()

     # Check if the selected article is in the product_details dictionary
    if article in product_details:
        product_info = product_details[article]
        product_code = product_info["Product_Code"]
        calories = product_info["calories"]
        expiring_date = (today + timedelta(days=product_info["Expiring_Days"])).strftime("%d%m%Y")
        owner_mapping = {"A": "01", "B": "02", "C": "03"}
        owner_nr = owner_mapping.get(owner, "00")

        # Generate the article code by concatenating different information elements
        article_code = str(product_code + expiring_date + calories + owner_nr)
        return article_code
    else:
        return "Product not found or not supported"

# Function to remove a selected article from inventory_list
def remove_item(selected_article):
    if selected_article in st.session_state.inventory_list:
        st.session_state.inventory_list.remove(selected_article)
        st.write(f'The product with the product code {selected_article} has been removed from the inventory.')

# Decode function to decode the product code
def decode_product_code(product_code, product_details):
    product_number = product_code[:2]
    expiration_date = product_code[2:10]
    calories = product_code[10:14]
    product_owner = product_code[14:]

    # Use the product name from the product_details dictionary based on the product code
    product_name = None
    for name, details in product_details.items():
        if details["Product_Code"] == product_number:
            product_name = name
            break

    expiration_date = (datetime.strptime(expiration_date, "%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Name": product_name,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner
    }

# Initialize session state to set buttons to a certain default state
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {
        "Article": None,
        "Owner": None,
        "selected_button": None,
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

# Show select boxes and Confirm button if the "Add product" button is pressed
if st.session_state.selected_options["selected_button"] == "add_item_button":
    options_Article = [
        "Milk", "Ham", "Yogurt", "Cheese", "Cream", "Pepper", "Sausage", "Carrots",
        "Cucumber", "Chocolate", "Cake", "Butter", "Apple", "Strawberries", "Salad",
    ]
    st.session_state.selected_options["Article"] = st.selectbox(
        "Choose your Article",
        options_Article,
        key="article_selectbox",
    )
    st.write("You selected:", st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C", "D"]
    st.session_state.selected_options["Owner"] = st.selectbox(
        "Choose the Owner", options_Owner, key="owner_selectbox"
    )
    st.write("You selected", st.session_state.selected_options["Owner"])

    # Confirm button
    confirm_button = st.button("Confirm")
    if confirm_button:
        product_code = generate_product_code(
            st.session_state.selected_options["Article"],
            st.session_state.selected_options["Owner"]
        )
        st.session_state.inventory_list.append(product_code)
        st.write(f'You added the product with the following product code: {product_code}')
        # Reset the selected button state after adding the article
        st.session_state.selected_options["selected_button"] = None

# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["selected_button"] = "remove_item_button"

# Show select boxes if the "Remove product" button is pressed
if st.session_state.selected_options["selected_button"] == "remove_item_button":
    # Display only the articles present in the inventory_list
    remove_options_article = st.session_state.inventory_list
    st.session_state.selected_options["Remove Article"] = st.selectbox(
        "Choose the articles you want to remove", remove_options_article
    )
    st.write("You selected", st.session_state.selected_options["Remove Article"])

    # Confirm button for removing the selected article
    confirm_remove_button = st.button("Confirm Remove")
    if confirm_remove_button:
        # Remove the selected article from the inventory_list
        st.session_state.inventory_list.remove(st.session_state.selected_options["Remove Article"])
        st.write(f'You removed the product with the following product code: {st.session_state.selected_options["Remove Article"]}')
        # Reset the selected button state after removing the article
        st.session_state.selected_options["selected_button"] = None

# Add owner button
add_owner_button = col3.button("Add owners")
if add_owner_button:
    st.session_state.selected_options["selected_button"] = "add_owner_button"

# Show select boxes if the "Add owners" button is pressed
if st.session_state.selected_options["selected_button"] == "add_owner_button":
    new_owner = st.text_input("Enter new owner")
    if new_owner:
        st.session_state.selected_options["Owner"] = new_owner
        st.write("New owner added:", new_owner)

# Remove owner button
remove_owner_button = col4.button("Remove owner")
if remove_owner_button:
    st.session_state.selected_options["selected_button"] = "remove_owner_button"

# Show select boxes if the "Remove owner" button is pressed
if st.session_state.selected_options["selected_button"] == "remove_owner_button":
    owners_list = [...]
    removed_owner = st.selectbox("Choose the owner to remove", owners_list)
    if removed_owner:
        st.session_state.selected_options["Owner"] = None
        st.write("Removed owner:", removed_owner)

# Show Inventory button
show_inventory_button = st.button("Show Inventory")
if show_inventory_button:
    owner_product_codes = defaultdict(lambda: defaultdict(list))
    product_details = {
        "Milk": {"Product_Code": "01", "calories": "0400", "Expiring_Days": 7},
        "Ham": {"Product_Code": "02", "calories": "0900", "Expiring_Days": 5},
        "Yogurt": {"Product_Code": "03", "calories": "0350", "Expiring_Days": 10},
        "Cheese": {"Product_Code": "04", "calories": "1200", "Expiring_Days": 15},
        "Cream": {"Product_Code": "05", "calories": "1500", "Expiring_Days": 12},
        "Pepper": {"Product_Code": "06", "calories": "0250", "Expiring_Days": 5},
        "Sausage": {"Product_Code": "07", "calories": "1800", "Expiring_Days": 8},
        "Carrots": {"Product_Code": "08", "calories": "0300", "Expiring_Days": 14},
        "Cucumber": {"Product_Code": "09", "calories": "0100", "Expiring_Days": 5},
        "Chocolate": {"Product_Code": "10", "calories": "3000", "Expiring_Days": 30},
        "Cake": {"Product_Code": "11", "calories": "2500", "Expiring_Days": 7},
        "Butter": {"Product_Code": "12", "calories": "3500", "Expiring_Days": 14},
        "Apple": {"Product_Code": "13", "calories": "0800", "Expiring_Days": 10},
        "Strawberries": {"Product_Code": "14", "calories": "0200", "Expiring_Days": 5},
        "Salad": {"Product_Code": "15", "calories": "0700", "Expiring_Days": 3},
    }

    for product_code in st.session_state.inventory_list:
        decoded_info = decode_product_code(product_code, product_details)
        owner = decoded_info["Product Owner"]
        product_name = decoded_info["Product Name"]
        expiration_date = decoded_info["Expiration Date"]
        owner_product_codes[owner][product_name].append((product_code, expiration_date))

    for owner, product_names in owner_product_codes.items():
        st.write(f"Owner {owner} possesses the following products:")
        for product_name, codes_and_dates in product_names.items():
            for product_code, expiration_date in codes_and_dates:
                st.write(f"{product_name}, Expiration Date - {expiration_date}")
        st.write()


from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import altair as alt
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
selected_option = st.selectbox('Select an option:', ['Owner', 'Article'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = expanded_df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

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





