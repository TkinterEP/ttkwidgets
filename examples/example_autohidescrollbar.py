# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import AutoHideScrollbar
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

window = tk.Tk()
listbox = tk.Listbox(window, height=5)
scrollbar = AutoHideScrollbar(window, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)

for i in range(10):
    listbox.insert('end', 'item %i' % i)

tk.Label(window, text="Increase the window's height\nto make the scrollbar vanish.").pack(side='top', padx=4, pady=4)
scrollbar.pack(side='right', fill='y')
listbox.pack(side='left', fill='both', expand=True)

window.mainloop()
