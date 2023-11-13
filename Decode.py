from datetime import datetime, timedelta
def decode_product_code(Product_Code):
    product_number = Product_Code[:2]
    expiration_date = Product_Code[2:10]
    calories = Product_Code[10:14]
    product_owner = Product_Code[14:]

    product_number = int(product_number)
    expiration_date = (datetime.strptime(expiration_date,"%d%m%Y")).strftime("%d.%m.%Y")
    calories = calories.lstrip("0")
    product_owner = "A" if product_owner == "01" else "B" if product_owner == "02" else "C" if product_owner == "03" else "No Owner"

    return {
        "Product Number": product_number,
        "Expiration Date": expiration_date,
        "Calories": calories,
        "Product Owner": product_owner
    }

print (decode_product_code("0220112023040002"))