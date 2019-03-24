import tkinter as tk
from tkinter import filedialog
import datetime

class ImportFile:
    def __init__(self, parent_widget):
        self.filename = ""
        self.start_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
        self.start_time = datetime.datetime(2019, 1, 1, 0, 0, 0)
        self.start_ht = 0.0
        self.start_nt = 0.0
        self.start_ap = 0.0
        self.end_ht = 1.0
        self.end_nt = 1.0
        self.end_ap = 1.0
        self.import_widget = tk.Toplevel(parent_widget)
        self.select_file_button = tk.Button(self.import_widget, text='Select File', command=self.get_filename).pack()
        self.quit_button = tk.Button(self.import_widget, text='close',
                                     command=self.close_window).pack()

    def close_window(self):
        print(self.filename)
        self.import_widget.destroy()

    def get_filename(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("data files", "*.txt"), ("all files", "*.*")))

def create_ui(root):
    import_buton = tk.Button(root, text='Import', command=lambda: import_subwindow(root)).pack()

def import_subwindow(root):
    import_data = ImportFile(root)



