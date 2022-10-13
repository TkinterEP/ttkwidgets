# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.frames import ScrolledFrame
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
frame = ScrolledFrame(window, compound=tk.RIGHT, canvasheight=200)
frame.pack(fill='both', expand=True)

for i in range(20):
    ttk.Label(frame.interior, text='Label %i' % i).pack()
window.mainloop()
