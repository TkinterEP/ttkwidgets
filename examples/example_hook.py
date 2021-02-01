# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2021
# For license see LICENSE
from tkinter import ttk
import tkinter as tk
from ttkwidgets.hook import hook_ttk_widgets

if __name__ == '__main__':
    hook_ttk_widgets(lambda s, o, v: print(s, o, v), {"tooltip": "Default Value"})
    hook_ttk_widgets(lambda s, o, v: print(s, o, v), {"hello_world": "second_hook"})

    original_init = ttk.Button.__init__

    def __init__(self, *args, **kwargs):
        print("User custom hook")
        original_init(self, *args, **kwargs)

    ttk.Button.__init__ = __init__

    window = tk.Tk()
    button = ttk.Button(window, text="Destroy", command=window.destroy, tooltip="Destroys Window")
    button.pack()
    print([name for name in dir(button) if name.startswith("WidgetHook")])
    window.after(1000, lambda: button.configure(tooltip="Does not destroy window", command=lambda: None))
    window.mainloop()
