from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from google_sheets_manager import GoogleSheetsManager
from table_widget import TableWidget
from filter_widget import FilterWidget
from upload_handler import UploadHandler


class App(QWidget):
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

        # Filter Widget
        self.filter_widget = FilterWidget(self)
        self.layout.addWidget(self.filter_widget)

        # Table Widget
        self.table = TableWidget(self)
        self.layout.addWidget(self.table)

        # Upload Button
        self.upload_handler = UploadHandler(self)
        self.uploadButton = QPushButton("Upload XLSX File")
        self.uploadButton.clicked.connect(self.upload_handler.upload_data)
        self.layout.addWidget(self.uploadButton)

        self.setLayout(self.layout)

    def load_data(self):
        """Load Google Sheets data into the table widget."""
        data = self.sheets_manager.get_data()

        if not data:
            return

        headers = data[0]  # First row as headers
        self.original_data = data[1:]  # Store full dataset for filtering

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.filter_widget.populate_dropdown()  # Fill dropdown with available months
        self.filter_widget.apply_filter()  # Initially show all data
