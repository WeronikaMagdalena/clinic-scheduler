from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog,
    QMessageBox, QComboBox, QLabel
)
import pandas as pd
from google_sheets_manager import GoogleSheetsManager


class GoogleSheetsApp(QWidget):
    def __init__(self, credentials_file, sheet_name):
        super().__init__()
        self.sheets_manager = GoogleSheetsManager(credentials_file, sheet_name)
        self.original_data = []  # Store unfiltered data
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('Google Sheets Viewer')
        self.setGeometry(100, 100, 800, 500)

        self.layout = QVBoxLayout()

        # Filter Dropdown
        self.filter_label = QLabel("Filter by Betreuungsmonat:")
        self.layout.addWidget(self.filter_label)

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.currentIndexChanged.connect(self.apply_filter)
        self.layout.addWidget(self.filter_dropdown)

        # Table to Display Data
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.tableWidget)

        # Upload Button
        self.uploadButton = QPushButton("Upload XLSX File")
        self.uploadButton.clicked.connect(self.upload_data)
        self.layout.addWidget(self.uploadButton)

        self.setLayout(self.layout)

    def load_data(self):
        """Load Google Sheets data into the table widget."""
        data = self.sheets_manager.get_data()

        if not data:
            return

        headers = data[0]  # First row as headers
        self.original_data = data[1:]  # Store full dataset for filtering

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        self.populate_dropdown()  # Fill dropdown with available months
        self.apply_filter()  # Initially show all data

    def populate_dropdown(self):
        """Populate dropdown with unique 'Betreuungsmonat' values."""
        month_index = self.sheets_manager.get_headers().index("Betreuungsmonat")
        months = sorted(set(row[month_index] for row in self.original_data))

        self.filter_dropdown.clear()
        self.filter_dropdown.addItem("All", None)  # Default option
        self.filter_dropdown.addItems(months)

    def apply_filter(self):
        """Filter table based on selected 'Betreuungsmonat'."""
        selected_month = self.filter_dropdown.currentText()

        if selected_month == "All" or not selected_month:
            filtered_data = self.original_data
        else:
            month_index = self.sheets_manager.get_headers().index("Betreuungsmonat")
            filtered_data = [row for row in self.original_data if row[month_index] == selected_month]

        self.update_table(filtered_data)

    def update_table(self, data):
        """Update table display with filtered data."""
        self.tableWidget.setRowCount(len(data))

        for row_idx, row in enumerate(data):
            self.tableWidget.setVerticalHeaderItem(row_idx, QTableWidgetItem(str(row_idx + 1)))  # Index starts at 1
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
