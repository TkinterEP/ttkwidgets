# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import DebugWindow
import tkinter as tk
from tkinter import ttk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        ttk.Button(self.main, text="Print ok", command=lambda: print('ok')).pack()
        DebugWindow(self.main)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
