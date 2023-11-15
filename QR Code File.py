import qrcode
from PIL import Image
import json
import base64
import io

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

if st.button('Reload your Article Code'):
    # This will force the Streamlit app to rerun
    st.experimental_rerun()

st.write(Article_Code)

from datetime import datetime, timedelta
def decode_product_code(article_Code):
    product_number = article_Code[:2]
    expiration_date = article_Code[2:10]
    calories = article_Code[10:14]
    product_owner = article_Code[14:]

    product_number = int(product_number)
    
    expiration_date = (datetime.strptime(expiration_date,"%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner}

st.write(decode_product_code(Article_Code))


import qrcode
from PIL import Image

def dict_to_qr_code(data):
    # Convert dictionary to string
    data_str = json.dumps(data)

    # Create QR Code from string
    qr = qrcode.QRCode()
    qr.add_data(data_str)
    qr.make()

    # Convert QR Code to an image
    img = qr.make_image(fill_color="black", back_color="white")

    return img

import base64
import io

# ...

buffered = io.BytesIO()
qr_code_img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()


# Display QR Code image
st.image(img_str)

