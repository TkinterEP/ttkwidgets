# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.autocomplete import AutocompleteCombobox
import tkinter as tk

window = tk.Tk()
tk.Label(window, text="Combobox with autocompletion for the Tk instance's methods:").pack(side='left')
entry = AutocompleteCombobox(window, width=20, completevalues=dir(window))
entry.pack(side='right')
window.mainloop()
