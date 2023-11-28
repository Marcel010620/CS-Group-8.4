import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict

# Initialize session state to store the decoded information dictionary
if 'decoded_info_dict' not in st.session_state:
    st.session_state.decoded_info_dict = {}

inventory_list = [
    "0220112023040002", "0120112023040003", "0320112023040003", "0420112023040001",
    "0520112023040001", "0620112023040002", "0720112023040002", "0820112023040001",
    "0920112023040002", "1020112023040001", "1120112023040002", "1220112023040003",
    "1320112023040001", "1420112023040003", "1520112023040001", "1620112023040002",
    "1720112023040001", "1820112023040002", "1920112023040003", "2020112023040001"
]

def decode_product_code(product_code):
    product_number = product_code[:2]
    expiration_date = product_code[2:10]
    calories = product_code[10:14]
    product_owner = product_code[14:]

    product_number = int(product_number)
    
    expiration_date = (datetime.strptime(expiration_date, "%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner
    }

# Apply decode_product_code to each element in inventory_list and append to the session state dictionary
for product_code in inventory_list:
    decoded_info = decode_product_code(product_code)
    st.session_state.decoded_info_dict[product_code] = decoded_info

# Display the decoded information stored in the session state dictionary
for product_code, decoded_info in st.session_state.decoded_info_dict.items():
    st.write(f"Product Code: {product_code}")
    for key, value in decoded_info.items():
        st.write(f"{key}: {value}")
    st.write()

# Create a defaultdict to store the product count for each owner
owner_product_count = defaultdict(int)

# Create a defaultdict to store the product codes for each owner and product
owner_product_codes = defaultdict(lambda: defaultdict(list))

# Iterate through the decoded_info_dict in session state
for product_code, decoded_info in st.session_state.decoded_info_dict.items():
    owner = decoded_info["Product Owner"]
    product_number = decoded_info["Product Number"]
    expiration_date = decoded_info["Expiration Date"]
    owner_product_codes[owner][product_number].append(product_code)

# Print the results
for owner, product_codes in owner_product_codes.items():
    st.write(f"Owner {owner} possesses the following products:")
    for product_number, codes in product_codes.items():
        st.write(f"Product {product_number} and Expiration Date is: {expiration_date}")
    st.write()