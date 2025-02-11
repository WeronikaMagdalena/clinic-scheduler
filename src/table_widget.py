from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.horizontalHeader().setVisible(True)

    def update_table(self, data):
        """Update table display with filtered data."""
        self.setRowCount(len(data))

        for row_idx, row in enumerate(data):
            self.setVerticalHeaderItem(row_idx, QTableWidgetItem(str(row_idx + 1)))  # Index starts at 1
            for col_idx, cell in enumerate(row):
                self.setItem(row_idx, col_idx, QTableWidgetItem(cell))
