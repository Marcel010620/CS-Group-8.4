import streamlit as st
from datetime import datetime, timedelta

add_owner_button = st.button ("Add Owner")
if add_owner_button: 
    Owner = st.text_input("Enter Owner Nr1.", "")




st.title(f"This is the smart refrigerator of:blue{Owner}")
