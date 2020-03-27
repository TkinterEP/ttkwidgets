# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import AutoHideScrollbar
import tkinter as tk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        listbox = tk.Listbox(self.main, height=5)
        scrollbar = AutoHideScrollbar(self.main, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        for i in range(10):
            listbox.insert('end', 'item %i' % i)

        tk.Label(self.main,
            text="Increase the window's height\nto make the scrollbar vanish.").pack(side='top',
            padx=4, pady=4)
        scrollbar.pack(side='right', fill='y')
        listbox.pack(side='left', fill='both', expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
