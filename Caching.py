# Für Eric 

# Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import altair as alt
import random

# Initialize inventory list in session state
if "inventory_list" not in st.session_state:
    st.session_state.inventory_list = []

# Initialize classes & subclasses
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

# Function to generate a product code
def generate_product_code(article, owner):
    # ... (unchanged code)

# Function to decode the product code
def decode_product_code(product_code):
    # ... (unchanged code)

# Function to add a product to the inventory list
@st.cache(allow_output_mutation=True)
def add_product(product_code):
    st.session_state.inventory_list.append(product_code)

# Function to remove a product from the inventory list
@st.cache(allow_output_mutation=True)
def remove_product(product_code):
    if product_code in st.session_state.inventory_list:
        st.session_state.inventory_list.remove(product_code)

# ... (unchanged code)

# Confirm button
confirm_button = st.button("Confirm")
if confirm_button:
    product_code = generate_product_code(article, owner)
    add_product(product_code)
    st.write(f'You added the product with the following product code: {product_code}')

# ... (unchanged code)

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
    removed_product_code = generate_product_code(removed_options_article, owner)
    remove_product(removed_product_code)

# ... (unchanged code)

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

# ... (unchanged code)

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





#Overview

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample data
data = {
    'Article': ['Apple', 'Apple', 'Cherry', 'Tomato', 'Elderberry'],
    'Quantity': count_owner_product_codes,
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


    