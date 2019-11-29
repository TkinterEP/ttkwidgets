"""
Author: Dogeek
License: GNU GPLv3
Source: This repository
"""

import tkinter as tk
import tkinter.ttk as ttk


class PlaceholderEntry(ttk.Entry):
    """ An Entry that takes an argument for a placeholder that'll be put in, and disappear once the widget takes focus"""
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        """
        :param master: Parent widget
        :param placeholder: Placeholder text to put in the widget
        :type placeholder: str
        :param color: color of the placeholder text
        :type color: str
        :param **kwargs: keyword arguments passed on to ttk::Entry
        :type kwargs: dict
        """
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.style = ttk.Style(self)

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self._put_placeholder()
        self["style"] = "Custom.TEntry"

    def _put_placeholder(self):
        """ Puts the placeholder text in the entry, and sets the foreground color of the style to the proper color"""
        self.insert(0, self.placeholder)
        self.style.configure("Custom.TEntry", foreground=self.placeholder_color)

    def _on_focus_in(self, *args):
        if self.style.lookup("Custom.TEntry", 'foreground') == self.placeholder_color:
            self.delete('0', 'end')
            self.style.configure("Custom.TEntry", foreground=self.style.lookup("TEntry", "foreground"))

    def _on_focus_out(self, *args):
        if not self.get():
            self._put_placeholder()