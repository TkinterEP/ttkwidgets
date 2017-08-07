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


class FontFamilyDropdown(AutocompleteCombobox):
    """
    A dropdown menu to select a font family with callback support and selection property
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :param callback: callable object with single argument: font family name
        :param kwargs: keyword arguments passed on to AutocompleteCombobox initializer
        """
        font_families = sorted([item for item in font.families()])
        self._fonts = font_families
        self._font = tk.StringVar(master)
        self.__callback = callback
        AutocompleteCombobox.__init__(self, master, textvariable=self._font, completevalues=font_families, **kwargs)
        self.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, *args):
        """
        Function bound to event of selection in the Combobox, calls callback if callable
        :param args: Tkinter event
        :return: None
        """
        if callable(self.__callback):
            self.__callback(self.selection)

    @property
    def selection(self):
        """
        Selection property returns None if no font is selected and font family name if one is selected
        :return:
        """
        if self._font.get() is "" or self._font.get() not in self._fonts:
            return None
        else:
            return self._font.get()
