# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import DebugWindow
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
ttk.Button(root, text="Print ok", command=lambda: print('ok')).pack()
DebugWindow(root)
root.mainloop()
