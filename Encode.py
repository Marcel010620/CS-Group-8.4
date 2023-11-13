!pip install python-barcode
!pip install streamlit


from datetime import datetime, timedelta
import barcode
from barcode.writer import ImageWriter

today = datetime.now().date()
Article = "Pepper"#input("Please select the Article")
Owner = "A"#input("Please select the owner of the product")

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
    filename = (f"{Article}_barcode")
    barcode_code128.save(filename)
    st.image (filename, caption=f"Generated Barcode", use_column_width=True)
    print(f"Barcode saved as {filename}")

#Number = Nr. Class + Due Date + Ownership + Nutritions 

generate_barcode(Article_Code)