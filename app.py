import streamlit as st
from datetime import datetime, timedelta

add_owner_button = st.button("Add owners here")
remove_owner_button = st.button("Which Owner would you like to remove")
add_item_button = st.button("Add an item to re fridge")
remove_item_button = st.button("remove an item from the fridge")

st.write(add_item_button,remove_item_button,add_owner_button,remove_owner_button)


wg_name = st.text_input("Your WG name")

st.title(f"his is the smart refrigerator of: {wg_name}")

add_owner_button = st.button("Add Owner")

if add_owner_button: 
    owners_list = []
    owners_list.append(st.text_input("Owner Nr.1"))
    add_another_owner_button = st.button ("Add another Owner")
    if add_another_owner_button: 
        owners_list.append(st.text_input("Owner Nr.2"))

reset_owner_button = st.button("Reset Owners")

if reset_owner_button: 
    owners_list = []
