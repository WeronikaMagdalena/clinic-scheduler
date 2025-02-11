import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox
)
from google_sheets_manager import GoogleSheetsManager


class GoogleSheetsApp(QWidget):
    def __init__(self, credentials_file, sheet_name):
        super().__init__()
        self.sheets_manager = GoogleSheetsManager(credentials_file, sheet_name)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('Google Sheets Viewer')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Table to Display Data
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.tableWidget)

        # Button to Upload File
        self.uploadButton = QPushButton("Upload XLSX File")
        self.uploadButton.clicked.connect(self.upload_data)
        self.layout.addWidget(self.uploadButton)

        self.setLayout(self.layout)

    def load_data(self):
        """Load Google Sheets data into the table widget."""
        data = self.sheets_manager.get_data()
        if data:
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))

            for row_idx, row in enumerate(data):
                for col_idx, cell in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(cell))

    def upload_data(self):
        """Handle file selection, validation, and data upload."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XLSX File", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            # Validate headers
            sheet_headers = self.sheets_manager.get_headers()
            df.columns = df.iloc[0]
            if list(df.columns) != sheet_headers:
                QMessageBox.warning(self, "Error", "Uploaded file headers do not match the sheet.")
                return

            # Remove headers and convert to list
            df = df[1:].reset_index(drop=True)
            df = df.fillna("")
            data_to_upload = df.values.tolist()

            # Upload to Google Sheets
            self.sheets_manager.append_data(data_to_upload)

            # Reload Data
            self.load_data()

            QMessageBox.information(self, "Success", "Data uploaded successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to upload data: {str(e)}")
