# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import CheckboxTreeview
import tkinter as tk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        tree = CheckboxTreeview(self.main)
        tree.pack()

        tree.insert("", "end", "1", text="1")
        tree.insert("1", "end", "11", text="11")
        tree.insert("1", "end", "12",  text="12")
        tree.insert("11", "end", "111", text="111")
        tree.insert("", "end", "2", text="2")


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
