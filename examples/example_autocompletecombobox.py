# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.autocomplete import AutocompleteCombobox
import tkinter as tk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        tk.Label(self.main,
            text="Combobox with autocompletion for the Tk instance's methods:").pack(side='left')
        entry = AutocompleteCombobox(
            self.main, width=20, completevalues=dir(self.main))
        entry.pack(side='right')


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
