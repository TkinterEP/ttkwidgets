# -*- coding: utf-8 -*-

# Copyright (c) rdbende 2021
# For license see LICENSE

from ttkwidgets import NumberEntry
import tkinter as tk

root = tk.Tk()
root.title('NumberEntry')

NumberEntry(root, expressions=True, roundto=4).pack(pady=30)

root.mainloop()
