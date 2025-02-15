from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QDate, QDateTime

from calendar_widget import CustomDateEdit


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.horizontalHeader().setVisible(True)
        self.termin_column = None  # Store column index for 'Termin'

    def update_table(self, data, headers):
        """Update table display with filtered data."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.termin_column = headers.index("Termin") if "Termin" in headers else None
        self.setRowCount(len(data))

        for row_idx, row in enumerate(data):
            self.setVerticalHeaderItem(row_idx, QTableWidgetItem(str(row_idx + 1)))  # Index starts at 1
            for col_idx, cell in enumerate(row):
                if col_idx == self.termin_column:
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(0, 0, 0, 0)

                    date_edit = CustomDateEdit(cell)
                    layout.addWidget(date_edit)

                    if cell:  # Only add 'x' button if there's a date
                        clear_button = QPushButton("x")
                        clear_button.setFixedSize(20, 20)
                        clear_button.clicked.connect(
                            lambda _, r=row_idx, d=date_edit: self.clear_date(r, d)
                        )
                        layout.addWidget(clear_button)

                    widget.setLayout(layout)
                    self.setCellWidget(row_idx, col_idx, widget)

                    # Connect signal to update Google Sheets
                    date_edit.dateChanged.connect(
                        lambda date, r=row_idx, c=col_idx: self.save_date_to_google_sheets(r, c, date)
                    )
                else:
                    item = QTableWidgetItem(cell)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Read-only
                    self.setItem(row_idx, col_idx, item)

    def save_date_to_google_sheets(self, row, col, date):
        """Update the Google Sheet when a date is changed."""
        formatted_date = date.toString("yyyy-MM-dd") if date != QDate(1900, 1, 1) else ""
        self.parent.sheets_manager.update_cell(row + 2, col + 1, formatted_date)  # +2 for Google Sheets indexing

    def clear_date(self, row, date_edit):
        """Reset date to 'Not Set' and update Google Sheets."""
        date_edit.setDate(QDate(1900, 1, 1))  # Reset to minimum date
        date_edit.setSpecialValueText("Not Set")
        date_edit.setStyleSheet("color: gray;")
        date_edit.setReadOnly(True)
        self.save_date_to_google_sheets(row, self.termin_column, QDate(1900, 1, 1))
