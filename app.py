import streamlit as st
from datetime import datetime, timedelta

add_owner_button = st.button ("Add Owner")
if add_owner_button: 
    Owner_name = st.text_input("Enter Owner Nr1.")

    if Owner_name: 
        owners_list = []
        owners_list.append(Owner_name)


st.title(f"This is the smart refrigerator of:blue{owners_list}")
