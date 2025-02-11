import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsManager:
    def __init__(self, credentials_file, sheet_name):
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.client = self.authenticate()
        self.sheet = self.client.open(self.sheet_name).sheet1

    def authenticate(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return gspread.authorize(creds)

    def get_data(self):
        """Retrieve all values from the Google Sheet."""
        return self.sheet.get_all_values()

    def get_headers(self):
        """Retrieve only the headers (first row) from the Google Sheet."""
        data = self.get_data()
        return data[0] if data else []

    def append_data(self, new_data):
        """Append new data (excluding headers) to the Google Sheet."""
        self.sheet.append_rows(new_data)
