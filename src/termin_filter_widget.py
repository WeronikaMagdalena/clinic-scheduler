# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget
# from PyQt5.QtCore import QDate
#
#
# class TerminFilterWidget(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         self.layout = QVBoxLayout()
#
#         self.filter_label = QLabel("Filter by Termin:")
#         self.layout.addWidget(self.filter_label)
#
#         self.calendar = QCalendarWidget()
#         self.calendar.setGridVisible(True)  # Optional: makes the calendar more readable
#         self.calendar.selectionChanged.connect(self.apply_filter)
#         self.layout.addWidget(self.calendar)
#
#         self.setLayout(self.layout)
#
#     def apply_filter(self):
#         """Filter table based on selected 'Termin'."""
#         selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")  # Adjust format as needed
#
#         month_index = self.parent.sheets_manager.get_headers().index("Termin")
#         filtered_data = [
#             row for row in self.parent.original_data if row[month_index] == selected_date
#         ]
#
#         self.parent.table.update_table(filtered_data, self.parent.sheets_manager.get_headers())
