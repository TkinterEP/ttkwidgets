# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import Tooltip
import tkinter as tk
from tkinter import ttk


window = tk.Tk()
button = tk.Button(window, text="Button", command=window.destroy)
button.pack()
balloon = Tooltip(button)
window.mainloop()
