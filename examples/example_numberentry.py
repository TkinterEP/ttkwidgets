# -*- coding: utf-8 -*-

# Copyright (c) rdbende 2021
# For license see LICENSE

from ttkwidgets import NumberEntry
import tkinter as tk

root = tk.Tk()
root.title('NumberEntry')

NumberEntry(root, expressions=True, roundto=4, allowed_chars={'p': 3.14159, 'x': 5}).pack(pady=30)

root.mainloop()
