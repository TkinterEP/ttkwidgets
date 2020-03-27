# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE

from ttkwidgets.frames import ToggledFrame
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

        frame = ToggledFrame(self.main, text="Value", width=10)
        frame.pack()
        button = ttk.Button(frame.interior, text="Button", command=self.main.destroy)
        button.grid()
        frame.toggle()


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
