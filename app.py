
from datetime import datetime, timedelta
import barcode
from barcode.writer import ImageWriter

today = datetime.now().date()
Article = input("Please select the Article")
Owner = input("Please select the owner of the product")

if Article == "Pepper": 
    Product_Code = "01"
    calories = "0037"
    Expiring_Date = (today + timedelta(days=10)).strftime("%d%m%Y")
    if Owner == "A": 
        Owner_Nr = "01"
    elif Owner == "B": 
        Owner_Nr = "02"
    elif Owner == "C":
        Owner_Nr = "03"
    Article_Code = str(Product_Code+Expiring_Date+calories+Owner_Nr)

if Article == "Milk": 
    Product_Code = "02"
    calories = "0400"
    Expiring_Date = (today + timedelta(days=7)).strftime("%d%m%Y")
    if Owner == "A": 
        Owner_Nr = "01"
    elif Owner == "B": 
        Owner_Nr = "02"
    elif Owner == "C":
        Owner_Nr = "03"
    Article_Code = str(Product_Code+Expiring_Date+calories+Owner_Nr)

print (Article_Code)

def generate_barcode(data):
    barcode_code128 = barcode.get("code128", data, writer=ImageWriter())
    filename = barcode_code128.save(f"{Article}_barcode")
    print(f"Barcode saved as {filename}")

#Number = Nr. Class + Due Date + Ownership + Nutritions 

generate_barcode(Article_Code)