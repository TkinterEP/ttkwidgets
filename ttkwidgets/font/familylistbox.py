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
from ttkwidgets import ScrolledListbox


class FontFamilyListbox(ScrolledListbox):
    """
    :class:`~ttkwidgets.ScrolledListbox` listing all font families available on the system with a Scrollbar on the right with the option
    of a callback when double clicked and a property to get the font family name.
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        Create a FontFamilyListbox.

        :param master: master widget
        :type master: widget
        :param callback: callable object with one argument: the font family name
        :type callback: function
        :param kwargs: keyword arguments passed to :class:`~ttkwidgets.ScrolledListbox`, in turn passed to :class:`tk.Listbox`
        """
        ScrolledListbox.__init__(self, master, compound=tk.RIGHT, **kwargs)
        self._callback = callback
        font_names = sorted(set(font.families()))
        index = 0
        self.font_indexes = {}
        for name in font_names:
            self.listbox.insert(index, name)
            self.font_indexes[index] = name
            index += 1
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
        return self.font_indexes[self.listbox.curselection()[0]]
