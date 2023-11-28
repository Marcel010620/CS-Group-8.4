from datetime import datetime, timedelta

inventory_list = [
    "0220112023040002", "0120112023040001", "0320112023040003", "0420112023040004",
    "0520112023040005", "0620112023040006", "0720112023040007", "0820112023040008",
    "0920112023040009", "1020112023040010", "1120112023040011", "1220112023040012",
    "1320112023040013", "1420112023040014", "1520112023040015", "1620112023040016",
    "1720112023040017", "1820112023040018", "1920112023040019", "2020112023040020"
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

# Create an empty dictionary to store the decoded information
decoded_info_dict = {}

# Apply decode_product_code to each element in inventory_list and append to the dictionary
for product_code in inventory_list:
    decoded_info = decode_product_code(product_code)
    decoded_info_dict[product_code] = decoded_info

# Print the decoded information stored in the dictionary
for product_code, decoded_info in decoded_info_dict.items():
    print(f"Product Code: {product_code}")
    for key, value in decoded_info.items():
        print(f"{key}: {value}")
    print()