"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
try:
    import Tkinter as tk
    import ttk
    import tkFont as font
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font
from ttkwidgets.autocomplete import AutocompleteCombobox


class FontSizeDropdown(AutocompleteCombobox):
    """
    A dropdown with default font sizes
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :param callback: callback on click with signle argument: int size
        :param kwargs: keyword arguments passed on to AutocompleteCombobox initializer
        """
        int_values = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        values = [str(value) for value in int_values]
        AutocompleteCombobox.__init__(self, master, completevalues=values, **kwargs)
        self.bind("<<ComboboxSelected>>", self._on_click)
        self.__callback = callback
        self.insert(0, "12")

    def _on_click(self, event):
        """
        Function bound to event of selection in the Combobox, calls callback if callable
        :param event: Tkinter event
        :return: None
        """
        if callable(self.__callback):
            self.__callback(self.selection)

    @property
    def selection(self):
        """
        Property that returns None if no value is selected and int size if selected
        :return: None
        """
        if self.get() is "":
            return None
        else:
            return int(self.get())
