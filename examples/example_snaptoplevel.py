# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE
import tkinter as tk
from ttkwidgets import SnapToplevel


window = tk.Tk()
top = SnapToplevel(window, location=tk.RIGHT, allow_change=True, locked=False)
window.mainloop()
