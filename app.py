import streamlit as st
from datetime import datetime, timedelta

st.button ("Reset Owner")
if st.button("Reset Owner"):
    Owner = []
    Owner.append(str(st.text_input("Owner Nr.1")))



st.title(f"This is the smart refrigerator of:blue{Owner}")
