from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QTimeEdit, QPushButton, QLabel


class CustomDateTimePicker(QDialog):
    def __init__(self, cell_value=None):
        super().__init__()

        self.setWindowTitle("Select Date and Time")
        self.setGeometry(100, 100, 350, 350)

        layout = QVBoxLayout()

        # Calendar Widget for date selection
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # Time Edit Widget for time selection
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")

        # OK Button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.get_datetime)

        # Label to display selected datetime
        self.label = QLabel("Selected Date & Time: ", self)

        # Add widgets to layout
        layout.addWidget(self.calendar)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.label)

        self.setLayout(layout)

        # Initialize with existing value if provided
        if cell_value:
            datetime = QDateTime.fromString(cell_value, "yyyy-MM-dd HH:mm")
            self.calendar.setSelectedDate(datetime.date())
            self.time_edit.setTime(datetime.time())

    def get_datetime(self):
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_edit.time()
        datetime_str = f"{selected_date.toString('yyyy-MM-dd')} {selected_time.toString('HH:mm')}"
        self.label.setText(f"Selected Date & Time: {datetime_str}")
        self.accept()  # Close the dialog