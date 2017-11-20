"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter.ttk as ttk
    import tkinter as tk
from PIL import Image, ImageTk
import os
from ttkwidgets.utilities import get_assets_directory


class Balloon(ttk.Frame):
    """
    Simple help hover balloon
    """

    def __init__(self, master=None, headertext="Help", text="Some great help is displayed here.", width=200, timeout=1,
                 background="#fef9cd", **kwargs):
        """
        :param master: widget to bind to
        :param headertext: text to show in window header
        :param text: text to show as help text
        :param width: width of the window
        :param timeout: timeout in seconds (can be float) to wait until Balloon is shown
        :param background: background color of the help Balloon
        :param kwargs: keyword arguments for Frame creation
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
        self.master = master
        self._id = None
        self._timeout = timeout
        self.master.bind("<Enter>", self._on_enter)
        self.master.bind("<Leave>", self._on_leave)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _grid_widgets(self):
        """
        Place the widgets in the Toplevel
        """
        self._canvas.grid(sticky="nswe")
        self.header_label.grid(row=1, column=1, sticky="nswe", pady=5, padx=5)
        self.text_label.grid(row=3, column=1, sticky="nswe", pady=6, padx=5)

    def _on_enter(self, event):
        """
        Creates a delayed callback for the <Enter> event
        """
        self._id = self.master.after(int(self._timeout * 1000), func=self.show)

    def _on_leave(self, event):
        """
        Callback for the <Leave> event to destroy the Toplevel
        """
        if self._toplevel:
            self._toplevel.destroy()
            self._toplevel = None
        if self._id:
            self.master.after_cancel(self._id)
            self._id = None

    def show(self):
        """
        Callback for the delayed <Enter> event (see _on_enter) to create the Toplevel widget and its child widgets to
        show in the spot of the cursor.
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
        x, y = self.master.winfo_pointerxy()
        self._canvas.update()
        # Update the Geometry of the Toplevel to update its position and size
        self._toplevel.geometry("{0}x{1}+{2}+{3}".format(self._canvas.winfo_width(), self._canvas.winfo_height(),
                                                         x + 2, y + 2))

    def cget(self, key):
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
        else:
            return ttk.Frame.cget(self, key)

    def config(self, **kwargs):
        self.__headertext = kwargs.pop("headertext", self.__headertext)
        self.__text = kwargs.pop("text", self.__text)
        self.__width = kwargs.pop("width", self.__width)
        self._timeout = kwargs.pop("timeout", self._timeout)
        self.__background = kwargs.pop("background", self.__background)
        if self._toplevel:
            self._on_leave(None)
            self.show()
        ttk.Frame.config(self, **kwargs)

    def configure(self, **kwargs):
        self.config(**kwargs)

    def keys(self):
        keys = ttk.Frame.keys(self)
        keys.extend(["headertext", "text", "width", "timeout", "background"])
        return keys
