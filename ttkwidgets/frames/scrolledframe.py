"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# The following sites were used for reference in the creation of this file:
# http://code.activestate.com/recipes/578894-mousewheel-binding-to-scrolling-area-tkinter-multi/
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class ScrolledFrame(ttk.Frame):
    """
    A frame that sports a vertically oriented scrollbar for scrolling

    Widgets can be placed in instance.interior attribute Frame with any geometry manager
    """

    def __init__(self, master=None, compound=tk.RIGHT, canvasheight=400, canvaswidth=400, canvasborder=0, **kwargs):
        """
        :param master: master widget
        :param compound: side the scrollbar should be on
        :param canvasheight: hight of the internal canvas
        :param canvaswidth: width of the internal canvas
        :param canvasborder: border width of the internal canvas
        :param kwargs: passed on to Frame.__init__
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._canvas = tk.Canvas(self, borderwidth=canvasborder, highlightthickness=0,
                                 yscrollcommand=self._scrollbar.set, width=canvaswidth, height=canvasheight)
        self.__compound = compound
        self._scrollbar.config(command=self._canvas.yview)
        self._canvas.yview_moveto(0)
        self.interior = ttk.Frame(self._canvas)
        self._interior_id = self._canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
        self.interior.bind("<Configure>", self.__configure_interior)
        self._canvas.bind("<Configure>", self.__configure_canvas)
        self.__grid_widgets()

    def __grid_widgets(self):
        """
        Places all the child widgets in the appropriate positions
        :return: None
        """
        scrollbar_column = 0 if self.__compound is tk.LEFT else 2
        self._canvas.grid(row=0, column=1, sticky="nswe")
        self.interior.grid(row=0, column=1, sticky="nswe")
        self._scrollbar.grid(row=0, column=scrollbar_column, sticky="ns")

    def __configure_interior(self, *args):
        """
        Private function to configure the interior Frame
        :param args: Tkinter event
        :return: None
        """
        # Resize the canvas scrollregion to fit the entire frame
        (size_x, size_y) = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self._canvas.config(scrollregion="0 0 {0} {1}".format(size_x, size_y))
        if self.interior.winfo_reqwidth() is not self._canvas.winfo_width():
            # If the interior Frame is wider than the canvas, automatically resize the canvas to fit the frame
            self._canvas.config(width=self.interior.winfo_reqwidth())

    def __configure_canvas(self, *args):
        """
        Private function to configure the internal Canvas
        Changes the width of the canvas to fit the interior Frame
        :param args: Tkinter event
        :return: None
        """
        if self.interior.winfo_reqwidth() is not self._canvas.winfo_width():
            self._canvas.configure(width=self.interior.winfo_reqwidth())

    def __mouse_wheel(self, event):
        """
        Private function to scroll the canvas view
        :param event: Tkinter event
        :return: None
        """
        self._canvas.yview_scroll(-1 * (event.delta // 100), "units")

    def resize_canvas(self, height=400, width=400):
        """
        Function for the user to resize the internal Canvas widget if desired
        :param height: new height in pixels
        :param width: new width in pixels
        :return:
        """
        self._canvas.configure(width=width, height=height)
