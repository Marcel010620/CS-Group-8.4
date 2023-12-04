import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Authentifizierungs-Scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Pfad zu deiner JSON-Anmeldedatei
SERVICE_ACCOUNT_FILE = '/Users/Anina/Desktop/CS/Project/Anina/CS-Project-main/projekt-cs-32b2fba1e1ff.json'

# Deine Spreadsheet-ID aus der URL deines Google Sheets
SPREADSHEET_ID = '1CLDAFhtriXEMnylxTfOqF27-GH5S9hXELq0WCl-8kb4'

# Funktion, um die Credentials zu erstellen und den Google Sheets Client zu autorisieren
def authenticate_gspread():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    return gc

# Funktion, um Daten von Google Sheets zu laden
def load_data_from_sheet(gc):
    worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    data = pd.DataFrame(worksheet.get_all_records())
    return data

# Funktion, um ein Produkt hinzuzufügen
def add_product(gc, product_name, expire_date):
    worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    worksheet.append_row([product_name, expire_date])

# Funktion, um das letzte Produkt zu entfernen
def remove_last_product(gc):
    worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    worksheet.delete_rows(worksheet.row_count)

# Hauptfunktion deiner Streamlit App
def main():
    # Authentifiziere den Google Sheets Client
    gc = authenticate_gspread()

    st.title('Produkte Manager')

    # Lade die Daten
    data = load_data_from_sheet(gc)
    st.write('Aktuelle Produkte:', data)

    # Eingabefelder für neue Produkte
    product_name = st.text_input('Produktname')
    expire_date = st.text_input('Verfallsdatum')

    # Button, um ein neues Produkt hinzuzufügen
    if st.button('Produkt hinzufügen'):
        add_product(gc, product_name, expire_date)
        st.success('Produkt hinzugefügt!')

    # Button, um das letzte Produkt zu entfernen
    if st.button('Letztes Produkt entfernen'):
        remove_last_product(gc)
        st.success('Letztes Produkt entfernt!')

    # Lade und zeige die aktualisierten Daten
    data = load_data_from_sheet(gc)
    st.write('Aktualisierte Produkte:', data)

if __name__ == "__main__":
    main()
