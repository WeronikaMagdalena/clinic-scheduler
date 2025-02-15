from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QDateEdit


class CustomDateEdit(QDateEdit):
    def __init__(self, cell_value):
        super().__init__(calendarPopup=True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setMinimumDate(QDate(1900, 1, 1))  # Set a reasonable minimum date

        if cell_value:
            self.setDate(QDateTime.fromString(cell_value, "yyyy-MM-dd").date())
            self.setStyleSheet("")  # Normal text color
            self.setReadOnly(False)  # Allow editing when date is set
        else:
            self.setSpecialValueText("Not Set")
            self.setDate(self.minimumDate())  # Default to minimum date
            self.setStyleSheet("color: gray;")  # Indicate unset state
            self.setReadOnly(True)  # Make it non-editable when "Not Set"

    def mousePressEvent(self, event):
        """If no date is set, change it to today when clicked."""
        if self.date() == self.minimumDate():
            self.setDate(QDate.currentDate())  # Set to today's date
            self.setStyleSheet("")  # Reset text color to default
            self.setReadOnly(False)  # Allow editing now
        super().mousePressEvent(event)  # Continue normal event handling

    def keyPressEvent(self, event):
        """Prevent manual editing when 'Not Set' is active."""
        if self.date() == self.minimumDate():
            return  # Ignore key presses when "Not Set"
        super().keyPressEvent(event)
