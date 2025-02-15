from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pandas as pd


class UploadHandler:
    def __init__(self, parent):
        self.parent = parent

    def upload_data(self):
        """Handle file selection, validation, and data upload."""
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Open XLSX File", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            # Validate headers
            sheet_headers = self.parent.sheets_manager.get_headers()
            sheet_headers = [header for header in sheet_headers if header != "Termin"]
            df.columns = df.iloc[0]
            if list(df.columns) != sheet_headers:
                QMessageBox.warning(self.parent, "Error", "Uploaded file headers do not match the sheet.")
                return

            # Remove headers and convert to list
            df = df[1:].reset_index(drop=True)
            df = df.fillna("").infer_objects(copy=False)
            data_to_upload = df.values.tolist()

            # Upload to Google Sheets
            self.parent.sheets_manager.append_data(data_to_upload)

            # Reload Data
            self.parent.data_loader.load_data()

            QMessageBox.information(self.parent, "Success", "Data uploaded successfully!")

        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to upload data: {str(e)}")
