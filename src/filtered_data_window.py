from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel


class FilteredDataWindow(QDialog):
    def __init__(self, filtered_data):
        super().__init__()
        self.filtered_data = filtered_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Filtered Data by Termin")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowMaximizeButtonHint)
        layout = QVBoxLayout()

        if self.filtered_data:
            self.table = QTableWidget()
            self.table.setRowCount(len(self.filtered_data))
            self.table.setColumnCount(len(self.filtered_data[0]))

            for row_idx, row in enumerate(self.filtered_data):
                for col_idx, cell in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

            layout.addWidget(self.table)
        else:
            layout.addWidget(QLabel("No data found for the selected Termin date."))

        self.setLayout(layout)
