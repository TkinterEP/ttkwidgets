"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Improved by rdbende
"""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from ttkwidgets.utilities import get_assets_directory

assets_dir = Path(get_assets_directory())


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
        :param text: text to in the header of the ToggledFrame
        :type text: str
        :param width: width of the closed ToggledFrame (in characters)
        :type width: int
        :param cursor: cursor that appears on the ToggledFrame's button
        :type cursor: str
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        cursor = kwargs.pop("cursor", "arrow")
        text = kwargs.pop("text", None)
        width = kwargs.pop("width", 20)

        self._open = tk.BooleanVar(value=False)

        ttk.Frame.__init__(self, master, **kwargs)

        self.interior = ttk.Frame(self)

        self._open_image = tk.PhotoImage(file=assets_dir / "open.png")
        self._closed_image = tk.PhotoImage(file=assets_dir / "closed.png")

        self._button = ttk.Checkbutton(
            self,
            style="Toolbutton",
            compound="right",
            cursor=cursor,
            image=self._closed_image,
            text=text,
            variable=self._open,
            command=self._toggle_when_clicked,
            width=width,
        )
        self._button.grid(row=0, column=0, sticky="ew")

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _toggle_when_clicked(self):
        # when clicking the checkbutton it inverts its variable, so we can't simply use self.toggle
        if self._open.get():
            self.interior.grid(row=1, column=0, sticky="nswe")
            self._button.config(image=self._open_image)
            self.event_generate("<<ToggledFrameOpened>>")
        else:
            self.interior.grid_forget()
            self._button.config(image=self._closed_image)
            self.event_generate("<<ToggledFrameClosed>>")

    def open(self):
        self.interior.grid(row=1, column=0, sticky="nswe")
        self._open.set(True)
        self._button.config(image=self._open_image)
        self.event_generate("<<ToggledFrameOpened>>")

    def close(self):
        self.interior.grid_forget()
        self._open.set(False)
        self._button.config(image=self._closed_image)
        self.event_generate("<<ToggledFrameClosed>>")

    def toggle(self):
        if self._open.get():
            self.close()
        else:
            self.open()

    @property
    def opened(self):
        return self._open.get()

    def configure(self, **kwargs):
        """Configure resources of the widget"""
        button_options = {
            key: kwargs.pop(key) for key in ("cursor", "text", "width") if key in kwargs
        }
        self._button.configure(**button_options)
        ttk.Frame.configure(self, **kwargs)

    config = configure

    def cget(self, key):
        """Return the resource value for a KEY given as string"""
        if key in {"cursor", "text", "width"}:
            return self._button.cget(key)
        else:
            return ttk.Frame.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget"""
        return sorted(ttk.Frame.keys(self) + ["text"])
