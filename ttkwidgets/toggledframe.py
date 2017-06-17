# Copyright (c) RedFantom 2017
# For license see LICENSE
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
    A frame that can be toggled to open and close
    """
    def __init__(self, master=None, labeltext="", compound=tk.LEFT, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.__open = tk.BooleanVar()
        self._open_image = ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), "open.png")))
        self._closed_image = ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), "closed.png")))
        self._checkbutton = ttk.Checkbutton(self, style="Toolbutton", command=self.toggle, variable=self.__open,
                                            text=labeltext, compound=compound, image=self._closed_image)
        self.interior = ttk.Frame(self, relief=tk.SUNKEN)
        self._grid_widgets()

    def _grid_widgets(self):
        self._checkbutton.grid(row=0, column=0, sticky="we")

    def toggle(self):
        if self.__open.get():
            self.__open.set(False)
            self.interior.grid(row=1, column=0, sticky="nswe")
            self._checkbutton.config(image=self._open_image)
        else:
            self.__open.set(True)
            self.interior.grid_forget()
            self._checkbutton.config(image=self._closed_image)

