"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende: default font size option
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
from ttkwidgets.autocomplete import AutocompleteCombobox


class FontSizeDropdown(AutocompleteCombobox):
    """
    A dropdown with default font sizes
    """

    def __init__(self, master=None, callback=None, font=None, **kwargs):
        """
        :param master: master widget
        :type master: widget
        :param callback: callback on click with single argument: `int` size
        :type callback: function
        :param font: set the default font family, family and size must be specified
        :type font: tuple
        :param kwargs: keyword arguments passed on to the :class:`~ttkwidgets.autocomplete.AutocompleteCombobox` initializer
        """
        int_values = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        values = [str(value) for value in int_values]
        AutocompleteCombobox.__init__(self, master, completevalues=values, **kwargs)
        self.bind("<<ComboboxSelected>>", self._on_click)
        self.bind("<Return>", self._on_click)
        self.__callback = callback
        if font:
            self.set(font[1])

    def _on_click(self, event):
        """
        Function bound to event of selection in the Combobox, calls callback if callable

        :param event: Tkinter event
        """
        if callable(self.__callback):
            self.__callback(self.selection)

    @property
    def selection(self):
        """
        Selection property.

        :return: None if no value is selected and size if selected.
        :rtype: None or int
        """
        if self.get() is "":
            return None
        else:
            return int(self.get())
