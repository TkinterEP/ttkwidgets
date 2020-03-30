# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2019
# For license see LICENSE

import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntryListbox


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        tk.Label(self.main,
            text="Entry + Listbox with autocompletion for the Tk instance's methods:").pack()
        entry = AutocompleteEntryListbox(
            self.main, width=20, completevalues=dir(self.main))
        entry.pack()


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
