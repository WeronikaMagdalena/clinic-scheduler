import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ctypes import windll
import google_sheets_manager


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        success = google_sheets_manager.upload_to_google_sheets(file_path)
        if success:
            messagebox.showinfo("Success", "Excel file uploaded successfully to Google Sheets!")
            update_table()
        else:
            messagebox.showerror("Error", "Upload failed!")


def update_table():
    for row in tree.get_children():
        tree.delete(row)
    data = google_sheets_manager.fetch_google_sheets_data()
    if data:
        tree["columns"] = data[0]
        tree["show"] = "headings"

        for col in data[0]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for row in data[1:]:
            tree.insert("", "end", values=row)


def run():
    root.mainloop()


# GUI Setup
windll.shcore.SetProcessDpiAwareness(1)
root = tk.Tk()
root.title("Data Route")

upload_btn = tk.Button(root, text="Select Excel File & Upload", command=upload_file)
upload_btn.pack(pady=20)

frame = tk.Frame(root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True)

update_table()
root.mainloop()
