# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import LinkLabel
import tkinter as tk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        LinkLabel(self.main, text="ttkwidgets repository",
                  link="https://github.com/RedFantom/ttkwidgets",
                  normal_color='royal blue',
                  hover_color='blue',
                  clicked_color='purple').pack()


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
