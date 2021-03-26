"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Improved by rdbende
"""

import tkinter as tk
from tkinter import ttk
import os
from ttkwidgets.utilities import get_assets_directory


class ToggledFrame(ttk.Frame):
    """
    A frame that can be toggled to open and close.

    :ivar interior: :class:`ttk.Frame` in which to put the widgets to be toggled with any geometry manager.
    """
    
    def __init__(self, master=None, **kwargs):
        """
        Create a ToggledFrame.

        :param master: master widget
        :type master: widget
        :param text: text to display next to the toggle arrow
        :type text: str
        :param width: width of the closed ToggledFrame (in characters)
        :type width: int
        :param compound: "center", "none", "top", "bottom", "right" or "left":
            position of the toggle arrow compared to the text
        :type compound: str
        :param opened: whether the frame should be opened by default
        :type opened: bool
        :param cursor: cursor that appears on the toggler-checkbutton
        :type cursor: str
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        self._compound = kwargs.pop("compound", tk.LEFT)
        self._cursor = kwargs.pop("cursor", "arrow")
        self._open = kwargs.pop("opened", False)
        self._text = kwargs.pop("text", None)
        self._width = kwargs.pop("width", 20)
        self._toggled = tk.BooleanVar(value=self._open)
        ttk.Frame.__init__(self, master, **kwargs)
        
        self._open_image = tk.PhotoImage(file=os.path.join(get_assets_directory(), "open.png"))
        self._closed_image = tk.PhotoImage(file=os.path.join(get_assets_directory(), "closed.png"))
        self._button = ttk.Checkbutton(self, style="Toolbutton", image=self._closed_image,
                                       cursor=self._cursor, variable=self._toggled,
                                       text=self._text, command=self.toggle,
                                       compound=self._compound, width=self._width)
        self._button.grid(row=0, column=0, sticky="ew")
        self.interior = ttk.Frame(self)
        if self._open:
            self.toggle()
    
    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def toggle(self, *args):
        """Toggle :obj:`ToggledFrame.interior` opened or closed."""
        if self._open:
            self._open = False
            self._toggled.set(False)
            self.interior.grid_forget()
            self._button.config(image=self._closed_image)
            self.event_generate("<<ToggledFrameClosed>>")
        else:
            self._open = True
            self._toggled.set(True)
            self.interior.grid(row=1, column=0, sticky="nswe")
            self._button.config(image=self._open_image)
            self.event_generate("<<ToggledFrameOpened>>")
        self.event_generate("<<ToggledFrameToggled>>")
            
    def configure(self, **kwargs):
        """Configure resources of the widget"""
        self._compound = kwargs.pop("compound", self._compound)
        self._cursor = kwargs.pop("cursor", self._cursor)
        self._open = kwargs.pop("opened", self._open)
        self._text = kwargs.pop("text", self._text)
        self._width = kwargs.pop("width", self._width)
        self._button.configure(text=self._text, cursor=self._cursor, compound=self._compound, width=self._width)
        ttk.Frame.configure(self, **kwargs)
        self._open = not self._open
        self.toggle()
        
    config = configure
            
    def cget(self, key):
        """Return the resource value for a KEY given as string"""
        if key == "compound":
            return self._compound
        elif key == "cursor":
            return self._cursor
        elif key == "opened":
            return self._opened
        elif key == "text":
            return self._text
        elif key == "width":
            return self._width
        else:
            return ttk.Frame.cget(key)
    
    def keys(self):
        """Return a list of all resource names of this widget"""
        keys = ttk.Frame.keys()
        keys.extend(["compound", "cursor", "opened", "text", "width"])
        keys.sort()
        return keys
