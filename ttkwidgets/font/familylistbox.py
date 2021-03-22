"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende to use AutocompleteEntryListbox to improve font search,
and for allow default font family option
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
import tkinter as tk
from tkinter import font as tkfont
from ttkwidgets.autocomplete.autocomplete_entrylistbox import AutocompleteEntryListbox


class FontFamilyListbox(AutocompleteEntryListbox):
    """
    :class:`~ttkwidgets.AutocompleteEntryListbox` listing all font families available
    on the system
    """

    def __init__(self, master=None, callback=None, font=None, **kwargs):
        """
        Create a FontFamilyListbox.

        :param master: master widget
        :type master: widget
        :param callback: callable object with one argument: the font family name
        :type callback: function
        :param font: set the default font family, family and size must be specified
        :type font: tuple
        :param kwargs: keyword arguments passed to :class:`~ttkwidgets.ScrolledListbox`, in turn passed to :class:`tk.Listbox`
        """
        self._callback = callback
        self._font_families = sorted(set(tkfont.families()))
        AutocompleteEntryListbox.__init__(self, master, completevalues=self._font_families, **kwargs)
        self.font_indexes = {}
        if font:
            self.listbox.selection_set(self._font_families.index(font[0]))
            self.listbox.yview_scroll(self._font_families.index(font[0]), "units")
        self.listbox.bind("<<ListboxSelect>>", self._on_click)

    def _on_click(self, *args):
        """
        Function bound to double click on Listbox that calls the callback if a valid callback object is passed

        :param args: Tkinter event
        """
        if callable(self._callback):
            self._callback(self.selection)

    @property
    def selection(self):
        """
        Selection property.

        :return: None if no font is selected and font family name if one is selected.
        :rtype: None or str
        """
        selection = self.listbox.curselection()
        if len(selection) is 0:
            return None
        return self._font_families[selection[0]]
