# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.font import FontSelectFrame
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

def update_preview(font_tuple):
    print(font_tuple)
    font = font_selection.font[0]
    if font is not None:
        label.configure(font=font)

window = tk.Tk()
label = ttk.Label(window, text='Sample text rendered in the chosen font.')
label.pack(padx=10, pady=10)
font_selection = FontSelectFrame(window, callback=update_preview)
font_selection.pack()
window.mainloop()
