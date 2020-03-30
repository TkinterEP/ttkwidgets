# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import ScaleEntry
import tkinter as tk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        scaleentry = ScaleEntry(self.main, scalewidth=200, entrywidth=3, from_=0, to=20)
        scaleentry.config_entry(justify='center')
        scaleentry.pack()


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
