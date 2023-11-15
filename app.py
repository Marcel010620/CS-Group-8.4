import streamlit as st
options = ["Pepper", "Milk"]
selected_option = st.selectbox("Choose your Article", options)
st.write('You selected:', selected_option)