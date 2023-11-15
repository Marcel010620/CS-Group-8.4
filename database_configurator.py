import sqlite3
from datetime import date
import pandas as pd

# Connect to SQLite database (create one if it doesn't exist)
conn = sqlite3.connect('refrigerator.sql')

# Create a table (if it doesn't exist)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS refrigerator_contents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    expiring_date DATE,
    owner TEXT,
    calories INTEGER,
    protein INTEGER,
    fat INTEGER,
    carbohydrates INTEGER
    )
    ''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def add_item(product_name, expiring_date, owner, calories, protein, fat, carbohydrates):
    # Connect to SQLite database
    conn = sqlite3.connect('refrigerator.db')
    cursor = conn.cursor()

    # Insert the item into the table
    cursor.execute('''
        INSERT INTO refrigerator_contents (product_name, expiring_date, owner, calories, protein, fat, carbohydrates)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product_name, expiring_date, owner, calories, protein, fat, carbohydrates))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def display_contents():
    # Connect to SQLite database
    conn = sqlite3.connect('refrigerator.db')

    # Query the database to get all items in the refrigerator
    query = "SELECT * FROM refrigerator_contents"
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

print(display_contents())