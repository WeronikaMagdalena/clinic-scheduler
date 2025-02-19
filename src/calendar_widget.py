from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QCalendarWidget, QTimeEdit,
    QPushButton, QLabel, QDateTimeEdit
)

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
        print(f"Selected Date & Time: {datetime_str}")
        self.accept()  # Close the dialog


class CustomDateEdit(QDateTimeEdit):
    def __init__(self, cell_value=None):
        super().__init__()
        self.setDisplayFormat("yyyy-MM-dd HH:mm")  # Set date and time format
        self.setMinimumDateTime(QDateTime(1900, 1, 1, 0, 0))  # Set a reasonable minimum date and time

        if cell_value:
            self.setDateTime(QDateTime.fromString(cell_value, "yyyy-MM-dd HH:mm"))
            self.setStyleSheet("")  # Normal text color
            self.setReadOnly(False)  # Allow editing when date and time is set
        else:
            self.setSpecialValueText("Not Set")
            self.setDateTime(self.minimumDateTime())  # Default to minimum date and time
            self.setStyleSheet("color: gray;")  # Indicate unset state
            self.setReadOnly(True)  # Make it non-editable when "Not Set"

        # Disable text editing by default
        self.setFocusPolicy(Qt.StrongFocus)  # Only focus via tab or click
        self.lineEdit().setReadOnly(True)  # Prevent manual typing

        # Connect to the custom dialog for date-time selection
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self and event.type() == 3:  # MousePressEvent
            if self.dateTime() == self.minimumDateTime():  # If no value is set
                self.setDateTime(QDateTime.currentDateTime())  # Set to current date and time
                self.setStyleSheet("")  # Reset text color to default
                self.setReadOnly(False)  # Allow editing now
            # Show the dialog for date-time selection
            picker = CustomDateTimePicker(self.dateTime().toString("yyyy-MM-dd HH:mm:ss"))
            picker.exec_()

            # Update the current widget value with selected date and time
            selected_datetime = picker.label.text().replace("Selected Date & Time: ", "")
            self.setDateTime(QDateTime.fromString(selected_datetime, "yyyy-MM-dd HH:mm:ss"))
            return True  # Event handled

        return super().eventFilter(source, event)  # Let the parent handle other events
