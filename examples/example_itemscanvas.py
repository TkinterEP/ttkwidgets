# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ItemsCanvas
import tkinter as tk
from tkinter import ttk


root = tk.Tk()

canvas = ItemsCanvas(root)
canvas.pack()

canvas.add_item("Example", font=("default", 13, "italic"), backgroundcolor="green", textcolor="darkblue",
                highlightcolor="blue")

root.mainloop()
