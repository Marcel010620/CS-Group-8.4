# Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

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

# Function to generate product code
def generate_product_code(article, owner):
    product_details = {
        # ... (your product details)
    }

    today = datetime.today()

    if article in product_details:
        product_info = product_details[article]
        product_code = product_info["Product_Code"]
        calories = product_info["calories"]
        expiring_date = (today + timedelta(days=product_info["Expiring_Days"])).strftime("%d%m%Y")
        owner_mapping = {"A": "01", "B": "02", "C": "03"}
        owner_nr = owner_mapping.get(owner, "00")

        article_code = str(product_code + expiring_date + calories + owner_nr)
        return article_code
    else:
        return "Product not found or not supported"

# Function to decode the product code
def decode_product_code(product_code):
    # ... (your decode function)

# Function to add a product to the inventory list
    @st.cache(allow_output_mutation=True)
    def add_product(product_code):
        st.session_state.inventory_list.append(product_code)

# Function to remove a product from the inventory list
    @st.cache(allow_output_mutation=True)
    def remove_product(product_code):
        if product_code in st.session_state.inventory_list:
            st.session_state.inventory_list.remove(product_code)

# Initialize session state to set buttons to a certain default state
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {
        "Article": None,
        "Owner": None,
        "selected_button": None,
    }

# Insert the name of the fridge
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
        # ... (your options)
    ]
    st.session_state.selected_options["Article"] = st.selectbox(
        "Choose your Article",
        options_Article,
        key="article_selectbox",
    )
    st.write("You selected:", st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C"]
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
    add_product(product_code)
    st.write(f'You added the product with the following product code: {product_code}')

# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["selected_button"] = "remove_item_button"

# Show select boxes if the "Remove product" button is pressed
if st.session_state.selected_options["selected_button"] == "remove_item_button":
    remove_options_article = [
        # ... (your remove options)
    ]
    removed_options_article = st.selectbox(
        "Choose the articles you want to remove", remove_options_article
    )
    st.write("You removed", removed_options_article)
    removed_product_code = generate_product_code(removed_options_article, owner)
    remove_product(removed_product_code)

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

# ...

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

    # Check if the inventory is not empty
    if not inventory_df.empty:
        # Create a DataFrame for Altair
        chart_df = inventory_df.groupby('Article').size().reset_index(name='Count')

        # Create a bar chart with Altair
        chart = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X('Article:O', title='Article'),
            y=alt.Y('Count:Q', title='Count'),
            color=alt.value('blue')
        )

        # Set chart properties
        chart = chart.properties(
            width=400,
            title=f'Bar Chart - Quantity by Article'
        )

        # Display the bar chart using Streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Inventory is empty. Add products to see the bar chart.")
