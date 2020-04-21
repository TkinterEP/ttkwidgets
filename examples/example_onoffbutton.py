# -*- coding: utf-8 -*-

# Copyright (c) 2020 Fredy Ramirez <https://formateli.com>
# For license see LICENSE

from ttkwidgets import OnOffButton
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


window = tk.Tk()


def grid_button(button, row, column):
    window.columnconfigure(column, weight=1)
    button.grid(row=row, column=column, padx=10, pady=10)


def print_value(button):
    print(button.get())


onoff_24_off = OnOffButton(window, command=print_value)
grid_button(onoff_24_off, 0, 0)

onoff_24_on = OnOffButton(window, command=print_value)
grid_button(onoff_24_on, 0, 1)
onoff_24_off.set(1)

onoff_24_disabled = OnOffButton(window, command=print_value)
grid_button(onoff_24_disabled, 0, 2)
onoff_24_disabled.config(state='disabled')

onoff_48_on = OnOffButton(window, size=48, command=print_value)
grid_button(onoff_48_on, 1, 0)

onoff_100_on = OnOffButton(window, size=100, command=print_value)
grid_button(onoff_100_on, 1, 1)
onoff_100_on.set(1)

window.mainloop()
