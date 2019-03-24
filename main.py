import import_dump
import pandas as pd
import datetime
import tkinter as tk
import ui


df = pd.read_csv('DUMP.TXT')
end_datetime = pd.to_datetime('now')
start_datetime = pd.Timestamp(datetime.datetime(1970, 1, 1, 0, 0, 0))
df, heat, appl = import_dump.preprocess(df,start_datetime,end_datetime,0,0,0,0,0,0)

root = tk.Tk()
ui.create_ui(root)
root.mainloop()