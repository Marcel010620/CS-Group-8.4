import streamlit as st
from datetime import datetime, timedelta

reset_owner_button = st.button("Reset Owners")

if reset_owner_button: 
    owners_list = []

add_owner_button = st.button("Add Owner")

if add_owner_button:
    owners_list = []
    owner_name = st.text_input("Enter Owner Nr1.")

    if owner_name:
        owners_list.append(owner_name)



# Display the list of owners outside the if block to avoid resetting the list on each iteration
st.title(f"This is the smart refrigerator of: {' '.join(map(str, owners_list))}")