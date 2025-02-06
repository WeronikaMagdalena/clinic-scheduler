import tkinter as tk
from tkinter import filedialog, messagebox
import google_sheets_manager


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        success = google_sheets_manager.upload_to_google_sheets(file_path)
        if success:
            messagebox.showinfo("Success", "Excel file uploaded successfully to Google Sheets!")
        else:
            messagebox.showerror("Error", "Upload failed!")


# GUI Setup
root = tk.Tk()
root.title("Upload Excel to Google Sheets")

upload_btn = tk.Button(root, text="Select Excel File & Upload", command=upload_file)
upload_btn.pack(pady=20)

root.mainloop()
