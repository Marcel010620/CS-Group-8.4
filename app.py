#Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict

# Initialize inventory list in session state in order to save data entries
if "inventory_list" not in st.session_state:
    st.session_state.inventory_list = []

# Read the Product file
df = pd.read_csv('products.csv')

#initialize classes & sublcasses 
class Product:
    def __init__(self, name, product_code, calories, expiry_days, quantity=1):
        self.name = name
        self.product_code = product_code
        self.calories = calories
        self.expiry_days = expiry_days
        self.quantity = quantity

class ApartmentFridge:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.owner in self.products:
            if len(self.products[product.owner]) < 1:
                self.products[product.owner].append(product)
                print(f"{product.name} added to the {product.owner}'s fridge.")
            else:
                print(f"The {product.owner}'s fridge is full!")
        else:
            self.products[product.owner] = [product]
            print(f"{product.name} added to a new {product.owner}'s fridge.")

    def display_fridge_contents(self):
        for owner, products in self.products.items():
            print(f"Owner: {owner}")
            for product in products:
                print(f" - {product.name} ({product.quantity} pieces)")


def generate_product_code(article, owner):
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

    if article in product_details:
        product_info = product_details[article]
        product_code = product_info["Product_Code"]  # Extract the product code
        calories = product_info["calories"]          # Extract the calories information
        # Calculate the expiration date based on the current date and the expiration days for the product
        expiring_date = (today + timedelta(days=product_info["Expiring_Days"])).strftime("%d%m%Y")
        owner_mapping = {"A": "01", "B": "02", "C": "03"}
        # Get the owner number corresponding to the provided owner ('A', 'B', or 'C') or set a default value
        owner_nr = owner_mapping.get(owner, "00")  # Default owner number if not 'A', 'B', or 'C'

        # Generate the article code by concatenating different information elements
        article_code = str(product_code + expiring_date + calories + owner_nr)
        return article_code  # Return the generated article code
    else:
        return "Product not found or not supported"  # Return a message if the article is not found in product_details
    
#Decode function to decode the product code
def decode_product_code(product_code):
    product_number = product_code[:2]
    expiration_date = product_code[2:10]
    calories = product_code[10:14]
    product_owner = product_code[14:]

    product_number = int(product_number)
    
    expiration_date = (datetime.strptime(expiration_date,"%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner}


# Initialize session state to set buttons to a certain default state
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {
        "Article": None,
        "Owner": None,
        "selected_button": None,
    }

# Insert the name of the fridge (for example, your WG Name)
wg_name = st.text_input("Your WG name")

# Display the title (name of the fridge) with a name given by a user input (style red)
st.markdown(
    f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>",
    unsafe_allow_html=True,
)

# Initialize Buttons

# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

# Initalize the add_item button
add_item_button = col1.button("Add product")

# Set the other buttons to False
if add_item_button:
    st.session_state.selected_options["selected_button"] = "add_item_button"

# Show select boxes and Confirm button if the "Add product" button is pressed
if st.session_state.selected_options["selected_button"] == "add_item_button":
    options_Article = [
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

    # Store the selected options in variables
    article = st.session_state.selected_options["Article"]
    owner = st.session_state.selected_options["Owner"]

    # Confirm button
    confirm_button = st.button("Confirm")
    if confirm_button:
        product_code = generate_product_code(article, owner)
        st.session_state.inventory_list.append(product_code)
        st.write(f'You added the product with the following product code: {product_code}')


# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["selected_button"] = "remove_item_button"

# Show select boxes if the "Remove product" button is pressed
if st.session_state.selected_options["selected_button"] == "remove_item_button":
    remove_options_article = [
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
    ]  # This needs to be a list with all Products inside the fridge
    removed_options_article = st.selectbox(
        "Choose the articles you want to remove", remove_options_article
    )
    st.write("You removed", removed_options_article)

# What happens if you press the add_owner_button
add_owner_button = col3.button("Add owners")
if add_owner_button:
    st.session_state.selected_options["selected_button"] = "add_owner_button"

# Show select boxes if the "Add owners" button is pressed
if st.session_state.selected_options["selected_button"] == "add_owner_button":
    new_owner = st.text_input("Enter new owner")
    if new_owner:
        st.session_state.selected_options["Owner"] = new_owner
        st.write("New owner added:", new_owner)

# What happens if you press the remove_owner_button
remove_owner_button = col4.button("Remove owner")
if remove_owner_button:
    st.session_state.selected_options["selected_button"] = "remove_owner_button"

# Show select boxes if the "Remove owner" button is pressed
if st.session_state.selected_options["selected_button"] == "remove_owner_button":
    owners_list = ["A", "B", "C"]  # Replace with your list of owners
    removed_owner = st.selectbox(
        "Choose the owner to remove", owners_list
    )
    if removed_owner:
        st.session_state.selected_options["Owner"] = None
        st.write("Removed owner:", removed_owner)

# Show Inventory button
show_inventory_button = st.button("Show Inventory")
if show_inventory_button:
    decoded_info_list = []

    for product_code in st.session_state.inventory_list:
        decoded_info = decode_product_code(product_code)
        decoded_info_list.append(decoded_info)

    # Create a DataFrame from the decoded information
    inventory_df = pd.DataFrame(decoded_info_list)

    # Display the inventory table
    st.write("Inventory:")
    st.table(inventory_df)


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


# Initialize session state to store the decoded information dictionary
if 'decoded_info_dict' not in st.session_state:
    st.session_state.decoded_info_dict = {}


def decode_product_code(product_code):
    product_number = product_code[:2]
    expiration_date = product_code[2:10]
    calories = product_code[10:14]
    product_owner = product_code[14:]

    product_number = int(product_number)
    
    expiration_date = (datetime.strptime(expiration_date, "%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner
    }

# Apply decode_product_code to each element in inventory_list and append to the session state dictionary
for product_code in inventory_list:
    decoded_info = decode_product_code(product_code)
    st.session_state.decoded_info_dict[product_code] = decoded_info

# Display the decoded information stored in the session state dictionary
for product_code, decoded_info in st.session_state.decoded_info_dict.items():
    st.write(f"Product Code: {product_code}")
    for key, value in decoded_info.items():
        st.write(f"{key}: {value}")
    st.write()

# Create a defaultdict to store the product count for each owner
owner_product_count = defaultdict(int)

# Create a defaultdict to store the product codes for each owner and product
owner_product_codes = defaultdict(lambda: defaultdict(list))

# Iterate through the decoded_info_dict in session state
for product_code, decoded_info in st.session_state.decoded_info_dict.items():
    owner = decoded_info["Product Owner"]
    product_number = decoded_info["Product Number"]
    expiration_date = decoded_info["Expiration Date"]
    owner_product_codes[owner][product_number].append(product_code)

# Print the results
for owner, product_codes in owner_product_codes.items():
    st.write(f"Owner {owner} possesses the following products:")
    for product_number, codes in product_codes.items():
        st.write(f"Product {product_number} and Expiration Date is: {expiration_date}")
    st.write()

#Test