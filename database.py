import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Authentifizierungs-Scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# JSON credentials information
credentials_info = {
    "type": "service_account",
    "project_id": "projekt-cs",
    "private_key_id": "32b2fba1e1ff5c8b13a83c50d5f3d7bfa6f27477",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIUF11TpEBbnKz\nq92eLPkQ9hj5dYZCofe3cqfowxK1WvKkWtOoPessaSlgp1Ms9DNL3qNfTL6QJef1\nVKvB/vX/5gI3IrR4WywNiTO/z7ODShsw6qNBJ0C+/Mhe3W6I6zkVFPjep4i8rQR5\nXQFDrku7L6drugfq6Ph1ovj4HklBZfitBrh82Kw49yxFGb2Vv6sWXQkQT4hgCwcq\nPcWhbS8o85jim3rgVx8lndUzgviad9SX/y2qAlUXD6nwyO+6E+DS2HlNGbx/CPbc\n+Bzoiqb7mVeFpBmEIYgpeIO7xn7XZTsvSuQM86jTlWQD2JGsA829OG4/fOAY+AiK\nmhJ515MJAgMBAAECggEACh6kQBBEa1r39LuAplRtj0WtiJG/QwfBdt02HiBXxj12\nX2b+xSO+qSdVaa5+WVmra0Bvxrle8bOWirp4tGPj6+YD8+LfFOr/OF5XdM/iiOYS\nJlgeQAUChHuLCF7drhFbGIVvFrmGQwjnHlX8Yb3REd90EPFMo9mZ7sB5XTiTeRgd\npgX7QVs2ueFJQkJEiTZjcGDL1NLuXOMevwBZRBuKnejJMXwfQQJI2LMVEBQd2zeS\nnvhnwkAMKMyNXodiuwrSrkEaWXvUgK0mSaAt9JLHudkQhArUjs3qG2h+Z7NezS52\n3gvjXUjh/evnbC3uKugX/sF8U0GVZ6OcsMXmXcW30QKBgQDzNqgUrCoDa3e63NPP\n/6gn7QLHjbqd643LlTbVBFY/6z+SkcxRW2UGm4qIW7Q4meyAxrFwGFqfWq12Z7SX\n8Q6WxclDDcXtzdeCHs5hGdHQP+Sj/6yF9/zIoBA9wpY5ISU189J2JiD01pF3F9J9\n/miSfX6oeHE2HYXTjk9Lr3Aw0QKBgQDS2FW+60X9TC/vyPEOIVpL2MaOgzCMaHyG\ny96MSwc9iER4us+qZzjzzbA7U7hLFhzUNyIiEv1IPfAU99To9f0CIvU+TSdoKgFM\nKq0EsSNiHRkfapt9MPcHhFXCflBeuKLaJ28oXfmQgOTujIY/iB/JVnqV3j+3sIBh\nKftWenKMuQKBgDjwb9M/JyrbyxENR+1nLggC3ea4EJuOHQkvasHeHQ8j1SNMTOgz\nHGi6m2knBv9FUfAoFDxpBzZNdVTGHKqBveegcGjpXZA5451L9wcWk19Mxgt6/Pn0\nP9L8XjEHUEIZt2t1JK2SaZ7IaQ/XnOjwWa0KAlAQunhv2vfXVksizIIxAoGBAJxp\nAcr8q9II97Kw5SnvUhXb/QfxiE1Qobg5eqGmcvuRoAHTy4QEyPoLx0VriNai08YW\nFEskvSIfWH+ljhs3iHZSSo3qHGaoaof/TJSjd7UsEtv8cNaBQXAhGqGKpMJvw9eD\n03ElraImDC5urpRovfPVJGETGz+APuxVgW8YrOt5AoGASdY2uNCU7tG1alOq8W4K\nsbrcspBnRVr/1Tev73xqDRLS8ew++2tlvKbrBYbdmBFPub40Dt04bWzIV9Qj9vHw\n2Eke5VbjhL0pQhez3MxT9P0FMiqU/35nNBzM+Vu0Gj+dxqg2r+Qx7E+7P+REkRZV\nWbH9xEDs1XfTAtbyZKWXypo=\n-----END PRIVATE KEY-----\n",
    "client_email": "cs-projekt@projekt-cs.iam.gserviceaccount.com",
    "client_id": "117933353454520023198",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cs-projekt%40projekt-cs.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Deine Spreadsheet-ID aus der URL deines Google Sheets
SPREADSHEET_ID = '1CLDAFhtriXEMnylxTfOqF27-GH5S9hXELq0WCl-8kb4'


def authenticate_gspread():
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
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
