import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets API Setup
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "../service_account.json"
SPREADSHEET_ID = "1rjI5FQcNPfaWpbOD7bmndpMwJooOshzCQQomBMYlQKg"  #to ENV VAR or other solution


def upload_to_google_sheets(file_path):
    try:
        """Authentication"""
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1

        """Read and process file"""
        df = pd.read_excel(file_path, engine='openpyxl')
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.columns = df.iloc[0]
        df = df[1:]
        df.reset_index(drop=True, inplace=True)
        df = df.fillna("")

        """Headers validation"""
        existing_headers = sheet.row_values(1)
        if existing_headers != df.columns.tolist():
            print("⚠️ Error: Headers do not match. Data upload aborted.")
            print(f"Google Sheets Headers: {existing_headers}")
            print(f"File Headers: {df.columns.tolist()}")
            return False

        """Data upload"""
        # sheet.clear()
        sheet.append_rows(df.values.tolist())
        # sheet.append_rows([df.columns.tolist()] + df.values.tolist())

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
