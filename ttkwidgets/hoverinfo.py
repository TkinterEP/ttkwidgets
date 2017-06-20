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


class Balloon(tk.Toplevel):
    """
    Simple help hover balloon
    """

    def __init__(self, master=None, headertext="Help", text="Some great help is displayed here.", width=200, timeout=1,
                 background="#fef9cd", **kwargs):
        if background is "white":
            raise ValueError("White is the only background color not currently allowed.")
        tk.Toplevel.__init__(self, master, background="white", **kwargs)
        self._canvas = tk.Canvas(self, background=background)
        self.wm_attributes("-transparentcolor", "white")
        # The image was found here:
        # https://www.iconfinder.com/icons/26486/balloon_help_information_icon#size=16
        # Under CC Attribution License
        self._image = Image.open(os.path.join(get_assets_directory(), "balloon.png"))
        self._photo_image = ImageTk.PhotoImage(self._image)
        self.__background = background
        self.header_label = ttk.Label(self._canvas, text=headertext, background=background, image=self._photo_image,
                                      compound=tk.LEFT)
        self.text_label = ttk.Label(self._canvas, text=text, wraplength=width, background=background)
        self.overrideredirect(True)
        self.master = master
        self._id = None
        self._timeout = timeout
        self.master.bind("<Enter>", self._on_enter)
        self.master.bind("<Leave>", self._on_leave)
        self.withdraw()

    def _grid_widgets(self):
        self._canvas.grid(sticky="nswe")
        self.header_label.grid(row=1, column=1, sticky="nswe", pady=5, padx=5)
        self.text_label.grid(row=3, column=1, sticky="nswe", pady=6, padx=5)

    def _ungrid_widgets(self):
        self._canvas.grid_forget()
        self.header_label.grid_forget()
        self.text_label.grid_forget()

    def _on_enter(self, event):
        print("Entered")
        self._id = self.after(self._timeout * 1000, func=self.show)
        print(self._id)

    def _on_leave(self, event):
        self.attributes("-topmost", False)
        print("Left")
        self.after_cancel(self._id)
        self._ungrid_widgets()

    def show(self):
        self.attributes("-topmost", True)
        self._grid_widgets()
        print("Showing")
        self.deiconify()
        x, y = self.winfo_pointerxy()
        self.geometry("{0}x{1}+{2}+{3}".format(self.winfo_reqwidth(), self.winfo_reqheight(), x + 2, y + 2))


if __name__ == '__main__':
    window = tk.Tk()
    button = tk.Button(window, text="Button", command=window.destroy)
    button.pack()
    balloon = Balloon(button)
    window.mainloop()
