from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QPushButton

from filtered_data_window import FilteredDataWindow

class TerminFilterWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select a Termin Date:")
        layout.addWidget(self.label)

        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        layout.addWidget(self.date_picker)

        self.filter_button = QPushButton("Filter by Termin", self)
        self.filter_button.clicked.connect(self.filter_data)
        self.date_picker.setDate(QDate.currentDate())
        layout.addWidget(self.filter_button)

        self.setLayout(layout)

    def filter_data(self):
        selected_date = self.date_picker.date()
        filtered_data = self.filter_by_termin(selected_date)

        # Create a new window or dialog to show filtered data
        self.filtered_window = FilteredDataWindow(filtered_data, self)
        self.filtered_window.exec_()

    def filter_by_termin(self, selected_date):
        """Filter rows where the 'Termin' column matches the selected date."""
        data = self.parent.original_data
        termin_column_index = self.parent.sheets_manager.get_headers().index("Termin")

        # Filter rows based on the selected date
        filtered_data = []
        for row in data:
            termin_datetime_str = row[termin_column_index]
            termin_date = QDateTime.fromString(termin_datetime_str, "yyyy-MM-dd HH:mm").date()
            if termin_date == selected_date:
                filtered_data.append(row)

        return filtered_data