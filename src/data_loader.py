class DataLoader:
    def __init__(self, parent):
        self.parent = parent

    def load_data(self):
        """Load Google Sheets data into the table widget."""
        data = self.parent.sheets_manager.get_data()

        if not data:
            return

        headers = data[0]  # First row as headers
        self.parent.original_data = data[1:]  # Store full dataset for filtering

        self.parent.table.setColumnCount(len(headers))
        self.parent.table.setHorizontalHeaderLabels(headers)

        self.parent.filter_widget.populate_dropdown()  # Fill dropdown with available months
        self.parent.filter_widget.apply_filter()  # Initially show all data
