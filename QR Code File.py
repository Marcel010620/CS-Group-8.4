import qrcode
from PIL import Image
import json
import base64
import io
import streamlit as st

def dict_to_qr_code(dict_data):
    # Convert dictionary to a string
    data_str = json.dumps(dict_data)

    # Create QR Code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to QR Code
    qr.add_data(data_str)
    qr.make(fit=True)

    # Create QR Code image
    img = qr.make_image(fill_color="black", back_color="white")

    return img

def decode_product_code(Article_Code):
    # This function is a placeholder and should be replaced with your actual decoding function
    product_number = "12345"
    expiration_date = "2023-01-01"
    calories = 100
    product_owner = "John Doe"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner}

st.write(decode_product_code(Article_Code))



# Display QR Code image
st.image


