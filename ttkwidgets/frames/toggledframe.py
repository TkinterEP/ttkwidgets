"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
import os
from PIL import Image, ImageTk
from ttkwidgets.utilities import get_assets_directory


class ToggledFrame(ttk.Frame):
    """
    A frame that can be toggled to open and close.

    :ivar interior: :class:`ttk.Frame` in which to put the widgets to be toggled with any geometry manager.
    """

    def __init__(self, master=None, text="", width=20, compound=tk.LEFT, **kwargs):
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
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self._open = False
        self.__checkbutton_var = tk.BooleanVar()
        self._open_image = ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), "open.png")))
        self._closed_image = ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), "closed.png")))
        self._checkbutton = ttk.Checkbutton(self, style="Toolbutton", command=self.toggle,
                                            variable=self.__checkbutton_var, text=text, compound=compound,
                                            image=self._closed_image, width=width)
        self.interior = ttk.Frame(self, relief=tk.SUNKEN)
        self._grid_widgets()

    def _grid_widgets(self):
        self._checkbutton.grid(row=0, column=0, sticky="we")

    def toggle(self):
        """Toggle :obj:`ToggledFrame.interior` opened or closed."""
        if self._open:
            self._open = False
            self.__checkbutton_var.set(False)
            self.interior.grid_forget()
            self._checkbutton.config(image=self._closed_image)
        else:
            self._open = True
            self.__checkbutton_var.set(True)
            self.interior.grid(row=1, column=0, sticky="nswe")
            self._checkbutton.config(image=self._open_image)
