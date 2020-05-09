# -*- coding: utf-8 -*-

# Copyright (c) 2020 Fredy Ramirez <https://formateli.com>
# For license see LICENSE

from ttkwidgets import OnOffButton
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


window = tk.Tk()


def grid_button(button, row, column):
    window.columnconfigure(column, weight=1)
    button.grid(row=row, column=column, padx=10, pady=10)


def print_value():
    print('Button toggled')


onoff_off = OnOffButton(window, command=print_value)
grid_button(onoff_off, 0, 0)

onoff_off_dis = OnOffButton(window)
grid_button(onoff_off_dis, 0, 1)
onoff_off_dis['state'] = 'disabled'

onoff_on = OnOffButton(window, command=print_value, cursor='hand2')
grid_button(onoff_on, 0, 2)
onoff_on.set('on')

onoff_on_dis = OnOffButton(window)
grid_button(onoff_on_dis, 0, 3)
onoff_on_dis.set('on')
onoff_on_dis['state'] = 'disabled'

chk = ttk.Checkbutton(window)
grid_button(chk, 1, 0)

window.mainloop()
