import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ctypes import windll
import google_sheets_manager
import month_filter


class DataRouteApp:
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.root = tk.Tk()
        self.root.title("Data Route")

        # Main Frame
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#ECECEC")
        main_frame.pack(fill="both", expand=True)

        # Upload Button
        upload_btn = ttk.Button(main_frame, text="Select Excel File & Upload", command=self.upload_file)
        upload_btn.pack(pady=10)

        # Filter Frame
        filter_frame = tk.Frame(main_frame, bg="#ECECEC")
        filter_frame.pack(pady=5)

        filter_label = ttk.Label(filter_frame, text="Filter by Betreuungsmonat (mm/yyyy):")
        filter_label.pack(side="left", padx=5)

        self.filter_entry = ttk.Entry(filter_frame)
        self.filter_entry.pack(side="left", padx=5)

        filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        filter_btn.pack(side="left", padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(main_frame, bg="white", relief="ridge", bd=2)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbars
        tree_x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")

        # Treeview Table
        self.tree = ttk.Treeview(
            tree_frame,
            xscrollcommand=tree_x_scroll.set,
            yscrollcommand=tree_y_scroll.set,
            selectmode="browse",
        )

        tree_x_scroll.config(command=self.tree.xview)
        tree_y_scroll.config(command=self.tree.yview)

        tree_x_scroll.pack(side="bottom", fill="x")
        tree_y_scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.update_table()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            success = google_sheets_manager.upload_to_google_sheets(file_path)
            if success:
                messagebox.showinfo("Success", "Excel file uploaded successfully to Google Sheets!")
                self.update_table()
            else:
                messagebox.showerror("Error", "Upload failed!")

    def update_table(self, filter_value=None):
        data = google_sheets_manager.fetch_google_sheets_data()
        if data:
            month_filter.populate_tree(self.tree, data, filter_value)

    def apply_filter(self):
        filter_value = self.filter_entry.get().strip()
        self.update_table(filter_value)

    def run(self):
        self.root.mainloop()

