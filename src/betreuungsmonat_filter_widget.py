from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox


class BetreuungsmonatFilterWidget(QWidget):
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

        # Store a mapping of filtered data indices to original data indices
        self.filtered_data_mapping = []

    def parse_month_year(self, value):
        """Convert 'mm/yyyy' string into (year, month) tuple for proper sorting."""
        try:
            month, year = map(int, value.split('/'))
            return (year, month)
        except ValueError:
            return (0, 0)

    def populate_dropdown(self):
        """Populate dropdown with unique 'Betreuungsmonat' values."""
        month_index = self.parent.sheets_manager.get_headers().index("Betreuungsmonat")
        months = sorted(set(row[month_index] for row in self.parent.original_data), key=self.parse_month_year)

        self.filter_dropdown.clear()
        self.filter_dropdown.addItem("All", None)
        self.filter_dropdown.addItems(months)

    def apply_filter(self):
        """Filter table based on selected 'Betreuungsmonat'."""
        selected_month = self.filter_dropdown.currentText()

        if selected_month == "All" or not selected_month:
            filtered_data = self.parent.original_data
        else:
            month_index = self.parent.sheets_manager.get_headers().index("Betreuungsmonat")
            filtered_data = [row for row in self.parent.original_data if row[month_index] == selected_month]

         # Store mapping of filtered rows to original rows
            self.filtered_data_mapping = [
                (i, self.parent.original_data.index(row)) for i, row in enumerate(filtered_data)
            ]

        self.parent.table.update_table(filtered_data, self.parent.sheets_manager.get_headers())
