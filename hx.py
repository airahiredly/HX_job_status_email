import requests
import os
from googleapiclient.discovery import build

# === CONFIGURATION ===
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyADynlfr6qm28II06W6tp08rBOgfuSGyhs")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1bNpflbQ7t-beTy4lctchmOczKoovPcckasCOhb1V9qs")
NAME_RANGE_NAME = 'Recruiters!A2:A2000'
EMAIL_RANGE_NAME = 'Recruiters!B2:B2000'
WEBHOOK_URL = 'https://n8n-app-p68zu.ondigitalocean.app/webhook-test/b4b390c0-7ddb-462e-8923-6cf7f01c0a8f'

# === INITIALIZE SHEETS API ===
service = build('sheets', 'v4', developerKey=API_KEY)
sheet = service.spreadsheets()

# === FETCH SHEET DATA ===
name_result = sheet.values().get(spreadsheetId=SHEET_ID, range=NAME_RANGE_NAME).execute()
email_result = sheet.values().get(spreadsheetId=SHEET_ID, range=EMAIL_RANGE_NAME).execute()
NAME_rows = name_result.get('values', [])
EMAIL_rows = email_result.get('values', [])

# === SEND EACH ROW TO WEBHOOK ===
for name_row, email_row in zip(NAME_rows, EMAIL_rows):
    name = name_row[0] if name_row else ''
    email = email_row[0] if email_row else ''
    
    payload = {'Name': name, 'Email': email}
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Sent: {payload} | Status: {response.status_code}")
