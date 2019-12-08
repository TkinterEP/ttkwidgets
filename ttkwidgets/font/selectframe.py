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
from .familydropdown import FontFamilyDropdown
from .propertiesframe import FontPropertiesFrame
from .sizedropdown import FontSizeDropdown


class FontSelectFrame(ttk.Frame):
    """
    A frame to use in your own application to let the user choose a font.

    For :class:`~font.Font` object, use :obj:`font` property.
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :type master: widget
        :param callback: callback passed argument
                         (`str` family, `int` size, `bool` bold, `bool` italic, `bool` underline)
        :type callback: function
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self.__callback = callback
        self._family = None
        self._size = 11
        self._bold = False
        self._italic = False
        self._underline = False
        self._overstrike = False
        self._family_dropdown = FontFamilyDropdown(self, callback=self._on_family)
        self._size_dropdown = FontSizeDropdown(self, callback=self._on_size, width=4)
        self._properties_frame = FontPropertiesFrame(self, callback=self._on_properties, label=False)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts all the widgets in the correct place.
        """
        self._family_dropdown.grid(row=0, column=0, sticky="nswe")
        self._size_dropdown.grid(row=0, column=1, sticky="nswe")
        self._properties_frame.grid(row=0, column=2, sticky="nswe")

    def _on_family(self, name):
        """
        Callback if family is changed.

        :param name: font family name
        """
        self._family = name
        self._on_change()

    def _on_size(self, size):
        """
        Callback if size is changed.

        :param size: font size int
        """
        self._size = size
        self._on_change()

    def _on_properties(self, properties):
        """
        Callback if properties are changed

        :param properties: tuple (bold, italic, underline, overstrike)
        """
        self._bold, self._italic, self._underline, self._overstrike = properties
        self._on_change()

    def _on_change(self):
        """Call callback if any property is changed."""
        if callable(self.__callback):
            self.__callback((self._family, self._size, self._bold, self._italic, self._underline, self._overstrike))

    def __generate_font_tuple(self):
        """
        Generate a font tuple for tkinter widgets based on the user's entries.

        :return: font tuple (family_name, size, *options)
        """
        if not self._family:
            return None
        font = [self._family, self._size]
        if self._bold:
            font.append("bold")
        if self._italic:
            font.append("italic")
        if self._underline:
            font.append("underline")
        if self._overstrike:
            font.append("overstrike")
        return tuple(font)

    @property
    def font(self):
        """
        Font property.

        :return: a :class:`~font.Font` object if family is set, else None
        :rtype: :class:`~font.Font` or None
        """
        if not self._family:
            return None, None
        font_obj = font.Font(family=self._family, size=self._size,
                             weight=font.BOLD if self._bold else font.NORMAL,
                             slant=font.ITALIC if self._italic else font.ROMAN,
                             underline=1 if self._underline else 0,
                             overstrike=1 if self._overstrike else 0)
        font_tuple = self.__generate_font_tuple()
        return font_tuple, font_obj
