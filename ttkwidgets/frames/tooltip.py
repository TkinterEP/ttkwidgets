"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from ttkwidgets.utilities import get_assets_directory


class Tooltip(ttk.Frame):
    """Simple help hover balloon."""

    def __init__(self, master=None, headertext="Help", text="Some great help is displayed here.", width=200, timeout=1,
                 background="#fef9cd", offset=(2, 2), showheader=True, static=False, **kwargs):
        """
        Create a Tooltip
        
        :param master: widget to bind the Tooltip to
        :type master: widget
        :param headertext: text to show in window header
        :type headertext: str
        :param text: text to show as help text
        :type text: str
        :param width: width of the window
        :type width: int
        :param timeout: timeout in seconds to wait until the Tooltip is shown
        :type timeout: float
        :param background: background color of the Tooltip
        :type background: str
        :param offset: The offset from the mouse position the Ballon shows up
        :type offset: Tuple[int, int]
        :param showheader: Whether to display the header with image
        :type showheader: bool
        :param static: Whether to display the tooltip with static
            position. When the position is set to static, the balloon
            will always appear an offset from the bottom right corner of
            the widget.
        :type static: bool
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self._toplevel = None
        self._canvas = None
        self.header_label = None
        self.text_label = None

        # The image was found here:
        # https://www.iconfinder.com/icons/26486/balloon_help_information_icon#size=16
        # Under CC Attribution License
        self._image = Image.open(os.path.join(get_assets_directory(), "balloon.png"))
        self._photo_image = ImageTk.PhotoImage(self._image, master=self)
        self.__background = background
        self.__headertext = headertext
        self.__text = text
        self.__width = width
        self.__offset = offset
        self.__showheader = showheader
        self.__static = static

        self.master = master
        self._id = None
        self._timeout = timeout

        self._bind_to_master()

    def _bind_to_master(self):
        """Bind the Balloon widget to the master widget's events"""
        self.master.bind("<Enter>", self._on_enter, "add")
        self.master.bind("<Leave>", self._on_leave, "add")
        self.master.bind("<ButtonPress>", self._on_leave, "add")

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _grid_widgets(self):
        """Place the widgets in the Toplevel."""
        self._canvas.grid(sticky="nswe")
        if self.__showheader is True:
            self.header_label.grid(row=1, column=1, sticky="nswe", pady=5, padx=5)
        self.text_label.grid(row=3, column=1, sticky="nswe", pady=6, padx=5)

    def _on_enter(self, event):
        """Creates a delayed callback for the :obj:`<Enter>` event."""
        self._id = self.master.after(int(self._timeout * 1000), func=self.show)

    def _on_leave(self, event):
        """Callback for the :obj:`<Leave>` event to destroy the Toplevel."""
        if self._toplevel:
            self._toplevel.destroy()
            self._toplevel = None
        if self._id:
            self.master.after_cancel(self._id)
            self._id = None

    def show(self):
        """
        Create the Toplevel and its children to show near the cursor

        This is the callback for the delayed :obj:`<Enter>` event
        (see :meth:`~Tooltip._on_enter`).
        """
        self._toplevel = tk.Toplevel(self.master)
        self._canvas = tk.Canvas(self._toplevel, background=self.__background)
        self.header_label = ttk.Label(self._canvas, text=self.__headertext, background=self.__background,
                                      image=self._photo_image, compound=tk.LEFT)
        self.text_label = ttk.Label(self._canvas, text=self.__text, wraplength=self.__width,
                                    background=self.__background)
        self._toplevel.attributes("-topmost", True)
        self._toplevel.overrideredirect(True)
        self._grid_widgets()
        if self.__static is True:
            x, y = self.master.winfo_rootx(), self.master.winfo_rooty()
            w, h = self.master.winfo_width(), self.master.winfo_height()
            x, y = x + w, y + h
        else:
            x, y = self.master.winfo_pointerxy()
        self._canvas.update()
        # Update the Geometry of the Toplevel to update its position and size
        self._toplevel.geometry("{0}x{1}+{2}+{3}".format(
            self._canvas.winfo_width(), self._canvas.winfo_height(),
            x + self.__offset[0], y + self.__offset[1]))

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method
        :meth:`~Tooltip.keys`.
        """
        if key == "headertext":
            return self.__headertext
        elif key == "text":
            return self.__text
        elif key == "width":
            return self.__width
        elif key == "timeout":
            return self._timeout
        elif key == "background":
            return self.__background
        elif key == "offset":
            return self.__offset
        elif key == "showheader":
            return self.__showheader
        elif key == "static":
            return self.__static
        else:
            return ttk.Frame.cget(self, key)

    def config(self, **kwargs):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method
        :meth:`~Tooltip.keys`. See :meth:`~Tooltip.__init__` for a
        description of the widget specific option.
        """
        self.__headertext = kwargs.pop("headertext", self.__headertext)
        self.__text = kwargs.pop("text", self.__text)
        self.__width = kwargs.pop("width", self.__width)
        self._timeout = kwargs.pop("timeout", self._timeout)
        self.__background = kwargs.pop("background", self.__background)
        self.__offset = kwargs.pop("offset", self.__offset)
        self.__showheader = kwargs.pop("showheader", self.__showheader)
        self.__static = kwargs.pop("static", self.__static)
        if self._toplevel:
            self._on_leave(None)
            self.show()
        ttk.Frame.config(self, **kwargs)

    configure = config

    def keys(self):
        keys = ttk.Frame.keys(self)
        keys.extend(["headertext", "text", "width", "timeout", "background", "offset", "showheader", "static"])
        return keys
