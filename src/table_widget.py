from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QDate, QDateTime

from calendar_widget import CustomDateEdit
from event_uploader import EventUploader


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.horizontalHeader().setVisible(True)
        self.termin_column = None  # Store column index for 'Termin'
        self.plandauer_column = None  # Store column index for 'Plandauer'
        self.event_uploader = EventUploader(self)

    def update_table(self, data, headers):
        """Update table display with filtered data."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.termin_column = headers.index("Termin") if "Termin" in headers else None
        self.plandauer_column = headers.index("Plandauer") if "Plandauer" in headers else None
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

                    clear_button = QPushButton("×")
                    clear_button.setFixedSize(22, 22)
                    clear_button.setStyleSheet(
                        "border: none; color: red; font-weight: bold; font-size: 14px;"
                    )
                    clear_button.setFocusPolicy(Qt.StrongFocus)  # Allow the button to gain focus

                    clear_button.setStyleSheet("""
                        QPushButton:focus {
                            background-color: lightcoral; /* Change color when focused */
                            color: white;
                        }
                    """)

                    clear_button.clicked.connect(
                        lambda _, r=row_idx, d=date_edit: self.clear_date(r, d)
                    )

                    layout.addWidget(clear_button)

                    upload_button = QPushButton("Upload")
                    upload_button.setFixedSize(60, 22)
                    upload_button.clicked.connect(
                        lambda _, r=row_idx: self.upload_event(r)
                    )
                    layout.addWidget(upload_button)

                    widget.setLayout(layout)
                    self.setCellWidget(row_idx, col_idx, widget)

                    # Connect signal to update Google Sheets
                    date_edit.dateTimeChanged.connect(
                        lambda datetime, r=row_idx, c=col_idx: self.save_date_to_google_sheets(r, c, datetime)
                    )
                else:
                    item = QTableWidgetItem(cell)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Read-only
                    self.setItem(row_idx, col_idx, item)

    def save_date_to_google_sheets(self, row, col, datetime):
        """Update Google Sheets when a date-time is changed."""
        try:
            original_row = self.parent.filter_widget.filtered_data_mapping[row][1]
        except IndexError:
            original_row = row

        formatted_datetime = datetime.toString("yyyy-MM-dd HH:mm") if datetime != QDateTime(1900, 1, 1, 0, 0) else ""
        # Update original data
        self.parent.original_data[original_row][col] = formatted_datetime

        # Update Google Sheets
        self.parent.sheets_manager.update_cell(original_row + 2, col + 1, formatted_datetime)

    def clear_date(self, row, date_edit):
        """Reset date-time to 'Not Set' and update Google Sheets."""
        date_edit.setDateTime(QDateTime(1900, 1, 1, 0, 0))  # Reset both date and time
        date_edit.setSpecialValueText("Not Set")
        date_edit.setStyleSheet("color: gray;")

        try:
            original_row = self.parent.filter_widget.filtered_data_mapping[row][1] if hasattr(
                self.parent.filter_widget, 'filtered_data_mapping') else row
        except IndexError:
            original_row = row

        self.parent.original_data[original_row][self.termin_column] = ""  # Clear the datetime in original data

        self.save_date_to_google_sheets(row, self.termin_column, QDateTime(1900, 1, 1, 0, 0))

    def upload_event(self, row_idx):
        """Upload event to Google Calendar."""
        row_data = []
        for col in range(self.columnCount()):
            if col == self.termin_column:
                date_edit = self.cellWidget(row_idx, col).layout().itemAt(0).widget()
                row_data.append(date_edit.dateTime().toString("yyyy-MM-dd HH:mm"))
            else:
                item = self.item(row_idx, col)
                row_data.append(item.text() if item else "")
        self.event_uploader.upload_event(row_data)
