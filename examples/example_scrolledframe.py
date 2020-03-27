# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.frames import ScrolledFrame
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

        frame = ScrolledFrame(self.main, compound=tk.RIGHT, canvasheight=200)
        frame.pack(fill='both', expand=True)

        for i in range(20):
            ttk.Label(frame.interior, text='Label %i' % i).pack()


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
