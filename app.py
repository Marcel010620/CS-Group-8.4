import streamlit as st
from datetime import datetime, timedelta
st.title(f"his is the smart refrigerator of: {st.text_input("Your WG Name")}")

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
