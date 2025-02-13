from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDateEdit
from PyQt5.QtCore import Qt, QDateTime


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
                    # Create a QDateEdit for the 'Termin' column
                    date_edit = QDateEdit(calendarPopup=True)
                    if cell:  # If there is an existing date, use it
                        date_edit.setDateTime(QDateTime.fromString(cell, "yyyy-MM-dd"))
                    else:
                        date_edit.setDateTime(QDateTime.currentDateTime())  # Default to current date/time

                    # Connect signal to update Google Sheets
                    date_edit.dateChanged.connect(
                        lambda date, r=row_idx, c=col_idx: self.save_date_to_google_sheets(r, c, date))

                    self.setCellWidget(row_idx, col_idx, date_edit)
                else:
                    item = QTableWidgetItem(cell)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Read-only
                    self.setItem(row_idx, col_idx, item)

    def save_date_to_google_sheets(self, row, col, date):
        """Update the Google Sheet when a date is changed."""
        formatted_date = date.toString("yyyy-MM-dd")  # Format date for Google Sheets
        self.parent.sheets_manager.update_cell(row + 2, col + 1,
                                               formatted_date)  # +2 because Google Sheets starts at 1 and row 1 is headers
