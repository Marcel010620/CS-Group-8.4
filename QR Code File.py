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

def decode_product_code(article_code):
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

decoded_data = decode_product_code(Article_Code)
qr_code_img = dict_to_qr_code(decoded_data)

# Convert QR Code image to a Streamlit-compatible format
buffered = io.BytesIO()
qr_code_img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Display QR Code image
st.image(img_str)