"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende: translation and default font properties option
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
import tkinter as tk
from tkinter import ttk
from locale import getdefaultlocale

# --- Translation
EN = {"Font properties:": "Font properties:"}

FR = {"Font properties:": "Propriétés"}

DE = {"Font properties:": "Eigenschaften"}

HU = {"Font properties:": "Betűstílus"}

try:
    if getdefaultlocale()[0][:2] == "fr":
        TR = FR
    elif getdefaultlocale()[0][:2] == "de":
        TR = DE
    elif getdefaultlocale()[0][:2] == "hu":
        TR = HU
    else:
        TR = EN
except ValueError:
    TR = EN


def tr(text):
    """Translate text."""
    return TR.get(text, text)


class FontPropertiesFrame(ttk.Frame):
    """
    Simple frame with buttons for Bold, Italic and Underline font types.
    """

    def __init__(self, master=None, callback=None, label=True, font=None, fontsize=11, **kwargs):
        """
        Create a FontPropertiesFrame.
        
        :param master: master widget
        :type master: widget
        :param callback: callback with argument
                         (`bool` bold, `bool` italic, `bool` underline, `bool` overstrike)
        :type callback: function
        :param label: show a header label
        :type label: str
        :param font: set the default font properties
        :type font: tuple
        :param fontsize: size of the font on the buttons
        :type fontsize: int
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self._style = ttk.Style()
        self.__label = label
        self.__callback = callback
        self._header_label = ttk.Label(self, text=tr("Font properties:"))
        
        self._style.configure("Bold.Toolbutton", font=("default", fontsize, "bold"), anchor=tk.CENTER)
        self._style.configure("Italic.Toolbutton", font=("default", fontsize, "italic"), anchor=tk.CENTER)
        self._style.configure("Underline.Toolbutton", font=("default", fontsize, "underline"), anchor=tk.CENTER)
        self._style.configure("Overstrike.Toolbutton", font=("default", fontsize, "overstrike"), anchor=tk.CENTER)

        self._bold = tk.BooleanVar(value=True if "bold" in font else False)
        self._italic = tk.BooleanVar(value=True if "italic" in font else False)
        self._underline = tk.BooleanVar(value=True if "underline" in font else False)
        self._overstrike = tk.BooleanVar(value=True if "overstrike" in font else False)
        
        self._bold_button = ttk.Checkbutton(self, style="Bold.Toolbutton", text="B", width=2,
                                            command=self._on_click, variable=self._bold, offvalue=False)
        self._italic_button = ttk.Checkbutton(self, style="Italic.Toolbutton", text="I", width=2,
                                              command=self._on_click, variable=self._italic, offvalue=False)
        self._underline_button = ttk.Checkbutton(self, style="Underline.Toolbutton", text="U", width=2,
                                                 command=self._on_click, variable=self._underline, offvalue=False)
        self._overstrike_button = ttk.Checkbutton(self, style="Overstrike.Toolbutton", text="O", width=2,
                                                  command=self._on_click, variable=self._overstrike, offvalue=False)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Place the widgets in the correct positions
        :return: None
        """
        if self.__label:
            self._header_label.grid(row=0, column=1, columnspan=3, sticky="nw", padx=5, pady=(5, 0))
        self._bold_button.grid(row=1, column=1, sticky="nswe", padx=5, pady=2)
        self._italic_button.grid(row=1, column=2, sticky="nswe", padx=(0, 5), pady=2)
        self._underline_button.grid(row=1, column=3, sticky="nswe", padx=(0, 5), pady=2)
        self._overstrike_button.grid(row=1, column=4, sticky="nswe", padx=(0, 5), pady=2)

    def _on_click(self):
        """Handles clicks and calls callback."""
    
        if callable(self.__callback):
            self.__callback((self.__generate_prop_tuple()))
    
    def __generate_prop_tuple(self):
        """
        Generate a prop tuple for tkinter widgets based on the user's entries.
        
        :return: prop tuple (*options)
        """
        prop = (self._bold.get(), self._italic.get(), self._underline.get(), self._overstrike.get())
        return prop

    @property
    def bold(self):
        """
        Bold property.
        
        :return: True if bold is selected
        :rtype: bool
        """
        return self._bold.get()

    @property
    def italic(self):
        """
        Italic property.
        
        :return: True if italic is selected
        :rtype: bool
        """
        return self._italic.get()

    @property
    def underline(self):
        """
        Underline property.
        
        :return: True if underline is selected
        :rtype: bool
        """
        return self._underline.get()

    @property
    def overstrike(self):
        """
        Overstrike property.
        
        :return: True if overstrike is selected
        :rtype: bool
        """
        return self._overstrike.get()
