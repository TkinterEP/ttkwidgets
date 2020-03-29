# -*- coding: utf-8 -*-

# Copyright (c) Dogeek 2020
# For license see LICENSE

import ttkwidgets.validated_entries as v_entries
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('Validated Entries Example')
frame = ttk.Frame(window)
frame.pack()

include = []
exclude = []

def filter_func(name):
    if name == 'ValidatedEntry':
        return False
    if name in include:
        return True
    if name in exclude:
        return False
    if name.endswith('Entry'):
        return True
    return False


for i, entry_data in enumerate([(n, vars(v_entries)[n]) for n in dir(v_entries) if filter_func(n)]):
    name, klass = entry_data
    label = ttk.Label(frame, text=name)
    entry = klass(frame)
    label.grid(row=i, column=0)
    entry.grid(row=i, column=1)
window.mainloop()
