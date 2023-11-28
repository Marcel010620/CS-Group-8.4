#Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

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

#Visualization 

# Initialize  session state to set buttons to a certain defualt state 
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {"Article": None, "Owner": None, "show_select_boxes": {"add_item_button": False, "remove_item_button": False, "add_owner_button": False, "remove_owner_button": False}}

# Insert the name of the fridge (for example, your WG Name)
wg_name = st.text_input("Your WG name")

# Display the title (name of the fridge) with a name given by a user input (style red)
st.markdown(f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>", unsafe_allow_html=True)

#Initalize Buttons 

# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

#Initalize the add_item button
add_item_button = col1.button("Add product")

#set the other buttons to False
if add_item_button:
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# Show select boxes of the add_item_button if the flag of the add_item_button is True
if st.session_state.selected_options["show_select_boxes"]["add_item_button"]:
    options_Article = ["Milk", "Ham", "Yogurt", "Cheese", "Cream", "Pepper", "Sausage", "Carrots", "Cucumber", "Chocolate", "Cake", "Butter", "Apple", "Strawberries", "Salad"]
    st.session_state.selected_options["Article"] = st.selectbox("Choose your Article", options_Article,
                                                                key="article_selectbox")
    st.write('You selected:', st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C", "D"]
    st.session_state.selected_options["Owner"] = st.selectbox("Choose the Owner", options_Owner,
                                                              key="owner_selectbox")
    st.write("You selected", st.session_state.selected_options["Owner"])

    # Store the selected options in variables
    article = st.session_state.selected_options["Article"]
    owner = st.session_state.selected_options["Owner"]

# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

if st.session_state.selected_options["show_select_boxes"]["remove_item_button"]:
    remove_options_article = ["Milk", "Ham", "Yogurt", "Cheese", "Cream", "Pepper", "Sausage", "Carrots", "Cucumber", "Chocolate", "Cake", "Butter", "Apple", "Strawberries", "Salad"]  # This needs to be a list with all Products inside the fridge
    removed_options_article = st.selectbox("Choose the articles you want to remove", remove_options_article)
    st.write("You removed", removed_options_article)

# What happens if you press the add_owner_button
add_owner_button = col3.button("Add owners")
if add_owner_button:
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

if st.session_state.selected_options["show_select_boxes"]["add_owner_button"]:
    new_owner = st.text_input("Enter new owner")
    if new_owner:
        st.session_state.selected_options["Owner"] = new_owner
        st.write("New owner added:", new_owner)

# What happens if you press the remove_owner_button
remove_owner_button = col4.button("Remove owner")
if remove_owner_button:
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False

# Show select boxes if the flag is True
if st.session_state.selected_options["show_select_boxes"]["remove_owner_button"]:
    owners_list = ["A", "B", "C"]  # Replace with your list of owners
    removed_owner = st.selectbox("Choose the owner to remove", owners_list)
    if removed_owner:
        st.session_state.selected_options["Owner"] = None
        st.write("Removed owner:", removed_owner)


inventory_list = [] 

confirm_button = st.button("Confirm")
if confirm_button:
    product_code = generate_product_code(article, owner)
    inventory_list.append(product_code)
    st.write(f'You added the product with following product code: {product_code}')

show_inventory_button = st.button("Show Inventory")
if show_inventory_button:
    # Create a DataFrame to display the inventory
    inventory_df = pd.DataFrame({"Product Code": inventory_list})
    st.write("Inventory:")
    st.dataframe(inventory_df)




get_product_code_button = st.button("generate product code")

if get_product_code_button: 
    st.write(generate_product_code(article, owner))



