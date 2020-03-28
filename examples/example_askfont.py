# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.font import askfont
import tkinter as tk
from tkinter import ttk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        self.label = ttk.Label(self.main, text='Sample text rendered in the chosen font.')
        self.label.pack(padx=10, pady=10)
        ttk.Button(self.main, text="Pick a font", command=self.font).pack()

    def font(self):
        res = askfont(self.main)
        if res[0] is not None:
            self.label.configure(font=res[0])
        self.main.grab_set()
        print(res)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
