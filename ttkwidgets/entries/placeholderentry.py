"""
Author: Dogeek
License: GNU GPLv3
Source: This repository
"""

import tkinter as tk
import tkinter.ttk as ttk


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.style = ttk.Style(self)

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()
        self["style"] = "Custom.TEntry"

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.style.configure("Custom.TEntry", foreground=self.placeholder_color)

    def foc_in(self, *args):
        if self.style.lookup("Custom.TEntry", 'foreground') == self.placeholder_color:
            self.delete('0', 'end')
            self.style.configure("Custom.TEntry", foreground=self.style.lookup("TEntry", "foreground"))

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()