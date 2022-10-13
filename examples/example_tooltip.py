# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import Tooltip
import tkinter as tk


window = tk.Tk()
button = tk.Button(window, text="Button", command=window.destroy)
button.pack()
balloon = Tooltip(button)
window.mainloop()
