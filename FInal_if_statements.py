from datetime import datetime, timedelta

def generate_product_code(article, owner):
    product_details = {
        "Milk": {"Product_Code": "02", "calories": "0400", "Expiring_Days": 7},
        "Ham": {"Product_Code": "05", "calories": "0900", "Expiring_Days": 5},
        "Yogurt": {"Product_Code": "08", "calories": "0350", "Expiring_Days": 10},
        "Cheese": {"Product_Code": "11", "calories": "1200", "Expiring_Days": 15},
        "Cream": {"Product_Code": "14", "calories": "1500", "Expiring_Days": 12},
        "Peppers": {"Product_Code": "17", "calories": "0250", "Expiring_Days": 5},
        "Sausage": {"Product_Code": "20", "calories": "1800", "Expiring_Days": 8},
        "Carrots": {"Product_Code": "23", "calories": "0300", "Expiring_Days": 14},
        "Cucumber": {"Product_Code": "26", "calories": "0100", "Expiring_Days": 5},
        "Chocolate": {"Product_Code": "29", "calories": "3000", "Expiring_Days": 30},
        "Cake": {"Product_Code": "32", "calories": "2500", "Expiring_Days": 7},
        "Butter": {"Product_Code": "35", "calories": "3500", "Expiring_Days": 14},
        "Apple": {"Product_Code": "38", "calories": "0800", "Expiring_Days": 10},
        "Strawberries": {"Product_Code": "41", "calories": "0200", "Expiring_Days": 5},
        "Salad": {"Product_Code": "44", "calories": "0700", "Expiring_Days": 3},
    }

   

    today = datetime.today()

   
    if article in product_details:
        name = product_details[article]
        product_code = name["Product_Code"]  # Extract the product code
        calories = name["calories"]          # Extract the calories information
        # Calculate the expiration date based on the current date and the expiration days for the product
        expiry_days = (today + timedelta(days=name["Expiring_Days"])).strftime("%d%m%Y")
        owner_mapping = {"A": "01", "B": "02", "C": "03"}
        # Get the owner number corresponding to the provided owner ('A', 'B', or 'C') or set a default value
        owner_nr = owner_mapping.get(owner, "00")  # Default owner number if not 'A', 'B', or 'C'

        # Generate the article code by concatenating different information elements
        article_code = str(product_code + expiry_days + calories + owner_nr)
        return article_code  # Return the generated article code
    else:
        return "Product not found or not supported"  # Return a message if the article is not found in product_details

# Example usage
Article = "Salad"  # Change the article name to test different products
Owner = "A"        # Change the owner to test different scenarios
Article_Code = generate_product_code(Article, Owner)
print(f"The generated article code for {Article} owned by {Owner} is: {Article_Code}")