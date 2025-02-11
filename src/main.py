import sys
import gspread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setWindowTitle('Google Sheets Viewer')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def loadData(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("../service_account.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("Data Link").sheet1
        data = sheet.get_all_values()

        if data:
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))

            for row_idx, row in enumerate(data):
                for col_idx, cell in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(cell))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GoogleSheetsApp()
    window.show()
    sys.exit(app.exec_())
