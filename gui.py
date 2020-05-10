# RUN THIS GUI FOR PROCESSING FILES
# Automatically checks and corrects for power cuts using "RecoverAfterPowerCut"
# Select the file to load by commenting one of the lines in preproc_gui.py... e.g.  READ_FILENAME = "corrected.csv"


import tkinter as tk
from tkinter import filedialog
from preproc_gui import *
import json

class Data:
    def __init__(self):
        self.load_filename = ""
        self.save_filename = ""
        self.HT_start = 0
        self.NT_start = 0
        self.APP_start = 0
        self.HT_end = 1
        self.NT_end = 1
        self.APP_end = 1
        self.start_datetime = ""
        self.end_datetime = ""
        self.actual_heating = 0
        self.actual_app =0
        self.logged_heating = 0
        self.logged_app = 0

START_DIR = "/"
SAVE_DIR = "/"
data = Data()

def update_global_data(*args):
    global data
    try:
        data.HT_start = float(HT_start_value.get())
        data.HT_end = float(HT_end_value.get())
        data.NT_start = float(NT_start_value.get())
        data.NT_end = float(NT_end_value.get())
        data.APP_start = float(APP_start_value.get())
        data.APP_end = float(APP_end_value.get())
        data.start_datetime = start_datetime_value.get()
        data.end_datetime = end_datetime_value.get()
        echo_values()
        run_pre_proc()
    except:
        print("Invalid field data")
        print("Attempting run from loaded JSON info")
        run_pre_proc()
        

def echo_values():
    for field in data.__dict__:
        print(field, data.__dict__[field])

def run_pre_proc():
    root.destroy()
    print("root destroyed")

def create_label(parent, text, row, column, rowspan=1, columnspan=1):
    label = tk.Label(master=parent,text=text)
    label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
    return label

def create_entry(parent, row, column, rowspan=1, columnspan=1):
    entry = tk.Entry(master=parent)
    entry.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="EW")
    return entry

def create_button(parent, text, row, column, command):
    button = tk.Button(master=parent, text=text, command=command)
    button.grid(row=row, column=column, sticky="EW")
    return button

def file_load_callback():
    global data
    data.load_filename = filedialog.askopenfilename(initialdir=START_DIR, title="Select file",
                                                    filetypes=(
                                                        ("Arduino files", "*.txt"), ("all files", "*.*")))
    print(data.load_filename)
    with open(data.load_filename) as f:
        info = json.load(f)
    print(info)
    data.HT_end = float(info["end"]["HT"])
    data.HT_start = float(info["start"]["HT"])
    data.NT_end = float(info["end"]["NT"])
    data.NT_start = float(info["start"]["NT"])
    data.APP_end = float(info["end"]["APP"])
    data.APP_start = float(info["start"]["APP"])
    data.start_datetime = info["start"]["date"]
    data.end_datetime = info["end"]["date"]


def file_save_callback():
    global data
    data.save_filename = filedialog.asksaveasfilename(initialdir=SAVE_DIR, title="Select file",
                                                      filetypes=(
                                                          ("Arduino files", "*.txt"), ("all files", "*.*")))

def actual_units_used():
    ht = data.HT_end-data.HT_start
    nt = data.NT_end-data.NT_start
    app = data.APP_end-data.APP_start

    heating = round(ht+nt, 2)
    appliance = round(app, 2)
    data.actual_heating = heating
    data.actual_app = appliance
    print("heating units: {}kWh".format(heating))
    print("appliance units used: {}kWh".format(appliance))

root = tk.Tk()

load_file_button = create_button(root, "Load filename", 0, 0, file_load_callback)
save_file_button = create_button(root, "Save file", 1, 0, file_save_callback)
submit_button = create_button(root, "Submit", 6, 0, update_global_data)
submit_button.grid_configure(columnspan=4)
start_datetime_label = create_label(root, "Start YYYY, MM, DD, HH, MM, SS", 2, 0)
end_datetime_label = create_label(root, "End YYYY, MM, DD, HH, MM, SS", 2, 2)
HT_start_label = create_label(root, "Start HT", 3, 0)
HT_end_label = create_label(root, "End HT", 3, 2)
NT_start_label = create_label(root, "Start HT", 4, 0)
HT_end_label = create_label(root, "End NT", 4, 2)
APP_start_label = create_label(root, "Start App", 5, 0)
APP_end_label = create_label(root, "End App", 5, 2)

# load_filename = create_entry(root, "a", 0, 1, 1, 3)
# save_filename = create_entry(root, "b", 1, 1, 1, 3)
# HT_start_value = create_entry(root, "c", 2, 1)
# NT_start_value = create_entry(root, "d", 3, 1)
# APP_start_value = create_entry(root, "e", 4, 1)
# HT_end_value = create_entry(root, "f", 2, 3)
# NT_end_value = create_entry(root, "g", 3, 3)
# APP_end_value = create_entry(root, "h", 4, 3)

# load_filename = create_entry(root, data.load_filename, 0, 1, 1, 3)
# save_filename = create_entry(root, data.save_filename, 1, 1, 1, 3)
# HT_start_value = create_entry(root, data.HT_start, 2, 1)
# NT_start_value = create_entry(root, data.NT_start, 3, 1)
# APP_start_value = create_entry(root, data.APP_start, 4, 1)
# HT_end_value = create_entry(root, data.HT_end, 2, 3)
# NT_end_value = create_entry(root, data.NT_end, 3, 3)
# APP_end_value = create_entry(root, data.APP_end, 4, 3)

load_filename = create_entry(root, 0, 1, 1, 3)
save_filename = create_entry(root, 1, 1, 1, 3)
start_datetime_value = create_entry(root, 2, 1)
end_datetime_value = create_entry(root, 2, 3)
HT_start_value = create_entry(root, 3, 1)
NT_start_value = create_entry(root, 4, 1)
APP_start_value = create_entry(root, 5, 1)
HT_end_value = create_entry(root, 3, 3)
NT_end_value = create_entry(root, 4, 3)
APP_end_value = create_entry(root, 5, 3)

tk.mainloop()
actual_units_used()
return_info = analyse(data)
data.logged_heating = return_info[0]
data.logged_app = return_info[1]
filename = return_info[2][:-4] + "_calibration.json"

for field in data.__dict__:
    print(field, data.__dict__[field])

with open(filename, "w") as fileout:
    json.dump(data.__dict__, fileout, indent=4)