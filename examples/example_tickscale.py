# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import TickScale
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

        style = ttk.Style(self.main)
        style.theme_use('clam')
        style.configure('my.Vertical.TScale', sliderlength=50,
                background='white', foreground='red')
        style.configure('my.Horizontal.TScale', sliderlength=10,
                font='TkDefaultFont 20 italic')
        s1 = TickScale(self.main, orient='vertical', style='my.Vertical.TScale',
                tickinterval=0.2, from_=-1, to=1, showvalue=True, digits=2,
                length=400, labelpos='e')
        s2 = TickScale(self.main, orient='horizontal', style='my.Horizontal.TScale',
                from_=0, to=10, tickinterval=2, resolution=1,
                showvalue=True, length=400)
        s3 = TickScale(self.main, orient='horizontal', from_=0.25, to=1,
                tickinterval=0.1, resolution=0.1)

        s1.pack(fill='y')
        s2.pack(fill='x')
        s3.pack(fill='x')


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
