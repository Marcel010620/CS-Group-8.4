# Implementation of ChatGPT-3.5-turbo API
# Goal: Get a recipe in natural language by giving prompt of list of ingredients
# Question whether we need ChatGPT-4 (potentially implement payment method for token payments, i.e. payments are collected
# by token-metric, each API request has given amount of units (tokens) which are used to calculate payment to openai)
# Question whether we need ChatGPT-4 (potentially implement payment method for token payments, i.e. payments are collected
# by token-metric, each API request has given amount of units (tokens) which are used to calculate payment to openai)

# Code:

import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_name('Marcel010620/CS-Group-8.4/projekt-cs-32b2fba1e1ff.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Database_A").sheet1  # File name of the gsheet 'Database_A

# Extract food items from the second column
food_items = sheet.col_values(2)  # Adjust if there are changes being made to the colums in the google-spreadsheet
food_list = ', '.join(food_items)

# OpenAI-API key for ChatGPT setup
openai.api_key = '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'  # Insert Openai-API key here

# Create prompt for ChatGPT
prompt = f"Create a recipe using the following ingredients: {food_list}"

# Generate recipe
response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt,
  max_tokens=150
)

# Print out the recipe
print(response.choices[0].text)



            
