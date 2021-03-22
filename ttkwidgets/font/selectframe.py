"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende: default font option
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from .familydropdown import FontFamilyDropdown
from .propertiesframe import FontPropertiesFrame
from .sizedropdown import FontSizeDropdown


class FontSelectFrame(ttk.Frame):
    """
    A frame to use in your own application to let the user choose a font.

    For :class:`~font.Font` object, use :obj:`font` property.
    """

    def __init__(self, master=None, callback=None, default=("Arial", 9), **kwargs):
        """
        :param master: master widget
        :type master: widget
        :param callback: callback passed argument
                         (`str` family, `int` size, `bool` bold, `bool` italic, `bool` underline)
        :type callback: function
        :param default: set the default font, family and size must be specified: (family, size, options)
        :type default: tuple 
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self.__callback = callback
        self._family = default[0]
        self._size = default[1]
        
        self._bold = True if "bold" in default else False
        self._italic = True if "italic" in default else False
        self._underline = True if "underline" in default else False
        self._overstrike = True if "overstrike" in default else False
        
        self._family_dropdown = FontFamilyDropdown(self, font=default, callback=self._on_family)
        self._size_dropdown = FontSizeDropdown(self, font=default, callback=self._on_size, width=6)
        self._properties_frame = FontPropertiesFrame(self, callback=self._on_properties, font=self.__generate_font_tuple()[2:], label=False)
        self._grid_widgets()
        # Unfortunately we can't just call _on_change,
        # because if the callback function uses the returned value (like in the example)
        # it raises error, because the widget basically does not exist until the end of __init__
        # self._on_change()

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
            font = self.__generate_font_tuple()
            self.__callback(font)

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
        Selected font.
        
        :return: font tuple (family_name, size, \*options), :class:`~font.Font` object
        """
        if self._family is None:
            return None, None
        else:
            font_tuple = self.__generate_font_tuple()
            font_obj = tkfont.Font(family=self._family, size=self._size,
                                   weight=tkfont.BOLD if self._bold else tkfont.NORMAL,
                                   slant=tkfont.ITALIC if self._italic else tkfont.ROMAN,
                                   underline=1 if self._underline else 0,
                                   overstrike=1 if self._overstrike else 0)
            return font_tuple, font_obj
