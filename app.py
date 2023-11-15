import streamlit as st
from datetime import datetime, timedelta
options_Article = ["Pepper", "Milk"]
selected_option_Article = st.selectbox("Choose your Article", options_Article)
st.write('You selected:', selected_option_Article)

options_Owner = ["A", "B", "C"]
selected_option_Owner = st.selectbox("Chosse the Owner", options_Owner)
st.write("You selected", selected_option_Owner)

today = datetime.now().date()

if selected_option_Article == "Pepper": 
    Product_Code = "01"
    calories = "0037"
    Expiring_Date = (today + timedelta(days=10)).strftime("%d%m%Y")
    if selected_option_Owner == "A": 
        Owner_Nr = "01"
    elif selected_option_Owner == "B": 
        Owner_Nr = "02"
    elif selected_option_Owner == "C":
        Owner_Nr = "03"
    Article_Code = str(Product_Code+Expiring_Date+calories+Owner_Nr)

if selected_option_Article == "Milk": 
    Product_Code = "02"
    calories = "0400"
    Expiring_Date = (today + timedelta(days=7)).strftime("%d%m%Y")
    if selected_option_Owner == "A": 
        Owner_Nr = "01"
    elif selected_option_Owner == "B": 
        Owner_Nr = "02"
    elif selected_option_Owner == "C":
        Owner_Nr = "03"
    Article_Code = str(Product_Code+Expiring_Date+calories+Owner_Nr)

st.write(Article_Code)