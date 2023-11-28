#Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta

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

#Visualization 

# Initialize  session state to set buttons to a certain defualt state 
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {"Article": None, "Owner": None, "show_select_boxes": {"add_item_button": False, "remove_item_button": False, "add_owner_button": False, "remove_owner_button": False}}

# Insert the name of the fridge (for example, your WG Name)
wg_name = st.text_input("Your WG name")

# Display the title (name of the fridge) with a name given by a user input (style red)
st.markdown(f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>", unsafe_allow_html=True)

#Initalize Buttons 
#Initalize the add_item button
add_item_button = col1.button("Add product")
#set the other buttons to False
if add_item_button:
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# Show select boxes if the flag of the add_item_button is True
if st.session_state.selected_options["show_select_boxes"]["add_item_button"]:
    options_Article = ["Pepper", "Milk"]
    st.session_state.selected_options["Article"] = st.selectbox("Choose your Article", options_Article,
                                                                key="article_selectbox")
    st.write('You selected:', st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C"]
    st.session_state.selected_options["Owner"] = st.selectbox("Choose the Owner", options_Owner,
                                                              key="owner_selectbox")
    st.write("You selected", st.session_state.selected_options["Owner"])

# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# What happens if you press the add_owner_button
add_owner_button = col3.button("Add owners")
if add_owner_button:
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False
#User input 

    #Buttons
    #Selectboxes 
    #Encode
        #--> Lisst append
    #Decode
        #--> Show item
    #Visulization of product/items