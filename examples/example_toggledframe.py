# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE

from ttkwidgets.frames import ToggledFrame
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

window = tk.Tk()
frame = ToggledFrame(window, text="Value", width=10)
frame.pack()
button = ttk.Button(frame.interior, text="Button", command=window.destroy)
button.grid()
frame.toggle()
window.mainloop()
