# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import Calendar
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

def validate():
    sel = calendar.selection
    if sel is not None:
        label.configure(text='Selected date: %s' % sel.strftime('%x'))

window = tk.Tk()
calendar = Calendar(window, year=2015, month=3, selectforeground='white',
                    selectbackground='red')
calendar.pack()

tk.Button(window, text='Select', command=validate).pack()
label = tk.Label(window, text='Selected date:')
label.pack()
window.mainloop()
