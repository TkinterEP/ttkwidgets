# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import ScaleEntry
import tkinter as tk


window = tk.Tk()
scaleentry = ScaleEntry(window, scalewidth=200, entrywidth=3, from_=0, to=20)
scaleentry.config_entry(justify='center')
scaleentry.pack()
window.mainloop()
