from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from google_sheets_manager import GoogleSheetsManager
from data_loader import DataLoader
from termin_filter_widget import TerminFilterWidget
from table_widget import TableWidget
from betreuungsmonat_filter_widget import BetreuungsmonatFilterWidget
from upload_handler import UploadHandler


class App(QWidget):
    def __init__(self, credentials_file, sheet_name):
        super().__init__()
        self.sheets_manager = GoogleSheetsManager(credentials_file, sheet_name)
        self.original_data = []  # Store unfiltered data

        self.init_ui()
        self.data_loader.load_data()

    def init_ui(self):
        self.setWindowTitle('Data Link')
        self.setGeometry(100, 100, 800, 500)
        self.layout = QVBoxLayout()

        # Betreuungsmonat Filter Widget
        self.filter_widget = BetreuungsmonatFilterWidget(self)
        self.layout.addWidget(self.filter_widget)

        # Termin Filter Widget
        self.termin_filter_widget = TerminFilterWidget(self)
        self.layout.addWidget(self.termin_filter_widget)

        # Table Widget
        self.table = TableWidget(self)
        self.layout.addWidget(self.table)

        # Upload Button
        self.upload_handler = UploadHandler(self)
        self.uploadButton = QPushButton("Upload XLSX File")
        self.uploadButton.clicked.connect(self.upload_handler.upload_data)
        self.layout.addWidget(self.uploadButton)

        self.setLayout(self.layout)

        self.data_loader = DataLoader(self)
