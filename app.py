#Import relevant libraries
import streamlit as st
from datetime import datetime, timedelta

# Insert the name of the fridge (for example, your WG Name)
wg_name = st.text_input("Your WG name")

# Display the title with the correct name given by a user input
st.markdown(f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>", unsafe_allow_html=True)

# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

# Initialize buttons
add_item_button = col1.button("Add product")
remove_item_button = col2.button("Remove product")
add_owner_button = col3.button("Add owners")
remove_owner_button = col4.button("Remove owner")

# Initialize session state to store selected options
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {"Article": None, "Owner": None}

# What happens if you press the add_item_button
if add_item_button:
    options_Article = ["Pepper", "Milk"]
    st.session_state.selected_options["Article"] = st.selectbox("Choose your Article", options_Article,
                                                                key="article_selectbox")
    st.write('You selected:', st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C"]
    st.session_state.selected_options["Owner"] = st.selectbox("Choose the Owner", options_Owner,
                                                              key="owner_selectbox")
    st.write("You selected", st.session_state.selected_options["Owner"])

# What happens if you press the remove_item_button
if remove_item_button:
    remove_options_article = ["Pepper", "Milk"]  # This needs to be a list with all Products inside the fridge
    removed_options_article = st.selectbox("Choose the articles you want to remove", remove_options_article)
    st.write("You removed", removed_options_article)