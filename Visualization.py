from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import altair as alt
import random

# Import relevant libraries from the second code
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Initialize inventory list in session state
if "inventory_list" not in st.session_state:
    st.session_state.inventory_list = []

# Initialize classes & subclasses 
class Product:
    def __init__(self, name, product_code, calories, expiry_days, quantity=1, owner=None):
        self.name = name
        self.product_code = product_code
        self.calories = calories
        self.expiry_days = expiry_days
        self.quantity = quantity
        self.owner = owner

class ApartmentFridge:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.owner in self.products:
            if len(self.products[product.owner]) < 1:
                self.products[product.owner].append(product)
                print(f"{product.name} added to the {product.owner}'s fridge.")
            else:
                print(f"The {product.owner}'s fridge is full!")
        else:
            self.products[product.owner] = [product]
            print(f"{product.name} added to a new {product.owner}'s fridge.")

    def display_fridge_contents(self):
        for owner, products in self.products.items():
            print(f"Owner: {owner}")
            for product in products:
                print(f" - {product.name} ({product.quantity} pieces)")

def generate_product_code(article, owner):
    product_details = {
        "Milk": {"Product_Code": "01", "calories": "0400", "Expiring_Days": 7},
        "Ham": {"Product_Code": "02", "calories": "0900", "Expiring_Days": 5},
        "Yogurt": {"Product_Code": "03", "calories": "0350", "Expiring_Days": 10},
        "Cheese": {"Product_Code": "04", "calories": "1200", "Expiring_Days": 15},
        "Cream": {"Product_Code": "05", "calories": "1500", "Expiring_Days": 12},
        "Pepper": {"Product_Code": "06", "calories": "0250", "Expiring_Days": 5},
        "Sausage": {"Product_Code": "07", "calories": "1800", "Expiring_Days": 8},
        "Carrots": {"Product_Code": "08", "calories": "0300", "Expiring_Days": 14},
        "Cucumber": {"Product_Code": "09", "calories": "0100", "Expiring_Days": 5},
        "Chocolate": {"Product_Code": "10", "calories": "3000", "Expiring_Days": 30},
        "Cake": {"Product_Code": "11", "calories": "2500", "Expiring_Days": 7},
        "Butter": {"Product_Code": "12", "calories": "3500", "Expiring_Days": 14},
        "Apple": {"Product_Code": "13", "calories": "0800", "Expiring_Days": 10},
        "Strawberries": {"Product_Code": "14", "calories": "0200", "Expiring_Days": 5},
        "Salad": {"Product_Code": "15", "calories": "0700", "Expiring_Days": 3},
    }

    today = datetime.today()

    if article in product_details:
        product_info = product_details[article]
        product_code = product_info["Product_Code"]  # Extract the product code
        calories = product_info["calories"]          # Extract the calories information
        # Calculate the expiration date based on the current date and the expiration days for the product
        expiring_date = (today + timedelta(days=product_info["Expiring_Days"])).strftime("%d%m%Y")
        owner_mapping = {"A": "01", "B": "02", "C": "03"}
        # Get the owner number corresponding to the provided owner ('A', 'B', or 'C') or set a default value
        owner_nr = owner_mapping.get(owner, "00")  # Default owner number if not 'A', 'B', or 'C'

        # Generate the article code by concatenating different information elements
        article_code = str(product_code + expiring_date + calories + owner_nr)
        return article_code  # Return the generated article code
    else:
        return "Product not found or not supported"  # Return a message if the article is not found in product_details

# Decode function to decode the product code
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
        "Product Owner": product_owner}

# Visualization 

# Sample data for different selections from the second code
data = {
    'Article': ['Milk', 'Ham', 'Yogurt', 'Cheese', 'Cream', 'Pepper', 'Sausage', 'Carrots', 'Cucumber', 'Chocolate', 'Cake', 'Butter', 'Apple', 'Strawberries', 'Salad'],
    'Quantity': [10, 5, 7, 3, 2, 8, 6, 4, 9, 5, 7, 3, 6, 4, 5],
}

# Ensure there are 15 different articles and 3 owners
owners = ['A', 'B', 'C']
data['Owner'] = [random.choice(owners) for _ in range(len(data['Article']))]

# Create a DataFrame with a separate row for each unit and a unique expiration date
rows = []
for i in range(len(data['Article'])):
    units = data['Quantity'][i]
    expiration_dates = [datetime.now() + timedelta(days=random.randint(1, 7)) for _ in range(units)]
    for expiration_date in expiration_dates:
        row = {
            'Article': data['Article'][i],
            'Quantity': 1,  # Count each unit as 1
            'Owner': data['Owner'][i],
            'Expiration Date': expiration_date,
        }
        rows.append(row)

df = pd.DataFrame(rows)

# Expand the DataFrame to have one row for each unique combination of Article and Expiration Date
expanded_df = df.explode('Expiration Date')

# Create a Streamlit app
st.title('Fridge Overview')

# Create a dropdown to select an option
selected_option = st.selectbox('Select an option:', ['Owner', 'Article', 'Expiration Date'])

# Create a DataFrame for Altair
if selected_option == 'Owner':
    chart_df = df.groupby('Owner').size().reset_index(name='Count')
    x_title, y_title = 'Owner', 'Count'

elif selected_option == 'Article':
    chart_df = expanded_df.groupby('Article').size().reset_index(name='Count')
    x_title, y_title = 'Article', 'Count'

elif selected_option == 'Expiration Date':
    # Create a new DataFrame for the selected Expiration Date
    next_7_days = [datetime.now() + timedelta(days=i) for i in range(7)]
    next_7_days_str = [date.date() for date in next_7_days]
    chart_df = expanded_df[expanded_df['Expiration Date'].dt.date.isin(next_7_days_str)].groupby(['Expiration Date']).size().reset_index(name='Count')
    x_title, y_title = 'Expiration Date', 'Count'

# Create a bar chart with Altair
chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X(f'{x_title}:O', title=x_title),
    y=alt.Y(f'{y_title}:Q', title=y_title),
    color=alt.value('blue'),
    tooltip=[x_title, y_title, alt.Tooltip('Expiration Date:T', format='%Y-%m-%d')]
)

# Apply changes only when 'Expiration Date' is chosen
if selected_option == 'Expiration Date':
    chart = chart.transform_aggregate(
        Count='sum(Count)',
        groupby=['Expiration Date']
    ).transform_calculate(
        Count='datum.Count'
    ).encode(
        x=alt.X(f'{x_title}:T', title=x_title, axis=alt.Axis(labels=True, format='%d/%m'), scale=alt.Scale(domain='unique')),
    )

# Set chart properties
chart = chart.properties(
    width=400,
    title=f'Bar Chart - {selected_option}'
)

# Display the bar chart using Streamlit
st.altair_chart(chart, use_container_width=True)



import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample data
data = {
    'Article': ['Apple', 'Apple', 'Cherry', 'Tomato', 'Elderberry'],
    'Quantity': [10, 5, 7, 3, 2],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit'],
    'Owner': ['A', 'A', 'C', 'A', 'B'],
    'Expiration Date': [datetime(2023, 12, 1), datetime(2023, 12, 3), datetime(2023, 12, 5), datetime(2023, 11, 25), datetime(2023, 12, 7)],
}

df = pd.DataFrame(data)

# Create a Streamlit app
st.title('Ownership')

# Create a dropdown to select either "Owner" or "Expires soon"
selection_option = st.selectbox('Select an option:', ['Owner', 'Expires soon'])

# Display the selected option
st.write(f'Selected option: {selection_option}')

# Based on the selected option, create and display the corresponding list
if selection_option == 'Owner':
    owners_list = df['Owner'].unique()
    selected_owner = st.selectbox('Select an owner:', owners_list)
    st.write(f'Selected owner: {selected_owner}')
    
    # Filter and calculate total count of products belonging to the selected owner
    owner_products = df[df['Owner'] == selected_owner]
    total_count_dict = owner_products.groupby('Article')['Quantity'].sum().to_dict()
    
    st.write(f'Total count of products owned by {selected_owner}:')
    
    for article, total_count in total_count_dict.items():
        st.write(f'{article}: {total_count}')

elif selection_option == 'Expires soon':
    expiration_threshold = datetime.now() + timedelta(days=2)
    expiring_articles = df[df['Expiration Date'] <= expiration_threshold]['Article'].tolist()
    st.write("Articles that expire soon:")
    st.write(expiring_articles)