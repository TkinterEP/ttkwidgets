# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import ScrolledListbox
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

window = tk.Tk()
listbox = ScrolledListbox(window, height=5)

for i in range(10):
    listbox.listbox.insert('end', 'item {}'.format(i))

listbox.pack(fill='both', expand=True)
window.mainloop()
