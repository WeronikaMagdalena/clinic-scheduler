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

        # Set headings
        for col in data[0]:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", stretch=True)

        # Insert rows
        for row in data[1:]:
            tree.insert("", "end", values=row)

        # Auto-resize columns based on content
        root.update_idletasks()  # Ensures accurate text measurement
        for col in data[0]:
            max_width = max(
                len(str(item)) for item in [col] + [row[data[0].index(col)] for row in data[1:]]
            )
            # Set max width of column to 300px, adjust as necessary
            tree.column(col, width=max(min(max_width * 8, 300), 100))  # Avoid very large widths


def run():
    root.mainloop()


# GUI Setup
windll.shcore.SetProcessDpiAwareness(1)
root = tk.Tk()
root.title("Data Route")
# root.geometry("800x500")
# root.minsize(700, 400)

# Main Frame
main_frame = tk.Frame(root, padx=10, pady=10, bg="#ECECEC")
main_frame.pack(fill="both", expand=True)

# Upload Button
upload_btn = ttk.Button(main_frame, text="Select Excel File & Upload", command=upload_file)
upload_btn.pack(pady=10)

# Treeview Frame
tree_frame = tk.Frame(main_frame, bg="white", relief="ridge", bd=2)
tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Scrollbars
tree_x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
tree_y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")

# Treeview Table
tree = ttk.Treeview(
    tree_frame,
    xscrollcommand=tree_x_scroll.set,
    yscrollcommand=tree_y_scroll.set,
    selectmode="browse",
)

tree_x_scroll.config(command=tree.xview)
tree_y_scroll.config(command=tree.yview)

tree_x_scroll.pack(side="bottom", fill="x")
tree_y_scroll.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# Run Application
update_table()
root.mainloop()
