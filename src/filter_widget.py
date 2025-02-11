from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class FilterWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()

        self.filter_label = QLabel("Filter by Betreuungsmonat:")
        self.layout.addWidget(self.filter_label)

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.currentIndexChanged.connect(self.apply_filter)
        self.layout.addWidget(self.filter_dropdown)

        self.setLayout(self.layout)

    def populate_dropdown(self):
        """Populate dropdown with unique 'Betreuungsmonat' values."""
        month_index = self.parent.sheets_manager.get_headers().index("Betreuungsmonat")
        months = sorted(set(row[month_index] for row in self.parent.original_data))

        self.filter_dropdown.clear()
        self.filter_dropdown.addItem("All", None)  # Default option
        self.filter_dropdown.addItems(months)

    def apply_filter(self):
        """Filter table based on selected 'Betreuungsmonat'."""
        selected_month = self.filter_dropdown.currentText()

        if selected_month == "All" or not selected_month:
            filtered_data = self.parent.original_data
        else:
            month_index = self.parent.sheets_manager.get_headers().index("Betreuungsmonat")
            filtered_data = [row for row in self.parent.original_data if row[month_index] == selected_month]

        self.parent.table.update_table(filtered_data)
