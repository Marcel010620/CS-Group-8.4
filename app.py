#Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta

#insert the name of the fridge (for example your WG Name)
wg_name = st.text_input("Your WG name")

#Display the title with the correct name given by a user input 
st.title(f"this is the smart refrigerator of: {wg_name}")

#Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

#Initialize buttons 
add_item_button = col1.button("Add product")
placeholder = col1.empty()
remove_item_button = col2.button("Remove product")
add_owner_button = col3.button("Add owners")
remove_owner_button = col4.button("remove owner")

#What happens if you press the add_item_button
if add_item_button:
    options_Article = ["Pepper", "Milk"]
    selected_option_Article = st.selectbox("Choose your Article", options_Article)
    st.write('You selected:', selected_option_Article)

    options_Owner = ["A", "B", "C"]
    selected_option_Owner = st.selectbox("Chosse the Owner", options_Owner)
    st.write("You selected", selected_option_Owner)

#What happens if you press the remove_item_buttonv
if remove_item_button:
    remove_options_article = ["Pepper", "Milk"] #this needs to be a list with all Procuts inside the fridge
    removed_options_article = st.selectbox("Choose the articles you want to remove", remove_options_article)
    st.write("You removed", removed_options_article)