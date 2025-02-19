from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QDateTimeEdit

from date_picker import CustomDateTimePicker


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
            picker = CustomDateTimePicker(self.dateTime().toString("yyyy-MM-dd HH:mm"))
            picker.exec_()

            # Update the current widget value with selected date and time
            selected_datetime = picker.label.text().replace("Selected Date & Time: ", "")
            self.setDateTime(QDateTime.fromString(selected_datetime, "yyyy-MM-dd HH:mm"))
            return True  # Event handled

        return super().eventFilter(source, event)  # Let the parent handle other events
