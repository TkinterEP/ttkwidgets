# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import ScrolledListbox
import tkinter as tk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        listbox = ScrolledListbox(self.main, height=5)

        for i in range(10):
            listbox.listbox.insert('end', 'item {}'.format(i))

        listbox.pack(fill='both', expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
