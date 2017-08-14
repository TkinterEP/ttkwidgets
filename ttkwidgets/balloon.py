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
        if background is "white":
            raise ValueError("White is the only background color not currently allowed.")
        ttk.Frame.__init__(self, master, **kwargs)
        self._toplevel = None
        self._canvas = None
        self.header_label = None
        self.text_label = None

        # The image was found here:
        # https://www.iconfinder.com/icons/26486/balloon_help_information_icon#size=16
        # Under CC Attribution License
        self._image = Image.open(os.path.join(get_assets_directory(), "balloon.png"))
        self._photo_image = ImageTk.PhotoImage(self._image)
        self.__background = background
        self.__headertext = headertext
        self.__text = text
        self.__width = width
        self.master = master
        self._id = None
        self._timeout = timeout
        self.master.bind("<Enter>", self._on_enter)
        self.master.bind("<Leave>", self._on_leave)

    def _grid_widgets(self):
        self._canvas.grid(sticky="nswe")
        self.header_label.grid(row=1, column=1, sticky="nswe", pady=5, padx=5)
        self.text_label.grid(row=3, column=1, sticky="nswe", pady=6, padx=5)

    def _on_enter(self, event):
        self._id = self.master.after(self._timeout * 1000, func=self.show)

    def _on_leave(self, event):
        if self._toplevel:
            self._toplevel.destroy()
        self.master.after_cancel(self._id)

    def show(self):
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
        self._toplevel.geometry("{0}x{1}+{2}+{3}".format(self._canvas.winfo_width(), self._canvas.winfo_height(),
                                                         x + 2, y + 2))


if __name__ == '__main__':
    window = tk.Tk()
    button = tk.Button(window, text="Button", command=window.destroy)
    button.pack()
    balloon = Balloon(button)
    window.mainloop()
