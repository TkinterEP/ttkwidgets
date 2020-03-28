# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE

from ttkwidgets import ItemsCanvas
import tkinter as tk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        canvas = ItemsCanvas(self.main)
        canvas.pack()

        canvas.add_item("Example",
                font=("default", 13, "italic"),
                backgroundcolor="green",
                textcolor="darkblue",
                highlightcolor="blue")


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
