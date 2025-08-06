import requests
import os
from googleapiclient.discovery import build

# === CONFIGURATION ===
API_KEY = os.getenv("GOOGLE_API_KEY")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
NAME_RANGE_NAME = 'Recruiters!A2:A2000'
EMAIL_RANGE_NAME = 'Recruiters!B2:B2000'
CC_RANGE_NAME = 'Recruiters!C2:C2000'
WEBHOOK_URL =  os.getenv("WEBHOOK_URL")

# === INITIALIZE SHEETS API ===
service = build('sheets', 'v4', developerKey=API_KEY)
sheet = service.spreadsheets()

# === FETCH SHEET DATA ===
name_result = sheet.values().get(spreadsheetId=SHEET_ID, range=NAME_RANGE_NAME).execute()
email_result = sheet.values().get(spreadsheetId=SHEET_ID, range=EMAIL_RANGE_NAME).execute()
cc_result = sheet.values().get(spreadsheetId=SHEET_ID, range=CC_RANGE_NAME).execute()
NAME_rows = name_result.get('values', [])
EMAIL_rows = email_result.get('values', [])
CC_rows = cc_result.get('values', [])

# === SEND EACH ROW TO WEBHOOK ===
for name_row, email_row in zip(NAME_rows, EMAIL_rows, CC_rows):
    name = name_row[0] if name_row else ''
    email = email_row[0] if email_row else ''
    cc = cc_row[0] if cc_row else ''
    
    payload = {'Name': name, 'Email': email, 'CC': cc}
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Sent: {payload} | Status: {response.status_code}")
