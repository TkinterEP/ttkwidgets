"""
Author: Dogeek
License: GNU GPLv3
Source: This repository
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from pathlib import Path

from ttkwidgets.utilities import get_bitmap


class SelectFolderEntry(ttk.Frame):
    """ An Entry with a Button attached, dedicated to selecting a folder """
    
    def __init__(self, master=None, title="Select a directory", bitmap=None, path=None, **kwargs):
        """
        :param master: The master widget
        :param title: Title of the tkinter.filedialog.askdirectory dialog
        :type title: str
        :param bitmap: a tkinter.BitmapImage instance for the bitmap shown on the button.
        :type bitmap: tkiner.BitmapImage
        :param path: the path to the folder. If None, the Entry will be empty.
        :type path: str
        :param **kwargs: keyword arguments passed on to the underlying Entry widget
        """
        super().__init__(master)
        self.ety = ttk.Entry(self, **kwargs)
        self.button_img = bitmap or get_bitmap("folder")
        button = ttk.Button(self, bitmap=self.button_img, command=self.on_btn_click)

        self.ety.bind("<Double-Button-1>", self.on_btn_click)
        self.path = path
        self.title = title
        if path is not None:
            self.ety.delete(0, tk.END)
            self.ety.insert(tk.END, self.path)

        self.ety.grid(row=0, column=0)
        button.grid(row=0, column=1)

    def on_btn_click(self, *args):
        self.path = filedialog.askdirectory(title=self.title)
        self.ety.delete(0, tk.END)
        self.ety.insert(tk.END, self.path)
    
    def get(self, as_string=False):
        """
        Gets the path from the Entry.
        :param as_string: (False) gets the path as a string
        :type as_string: bool
        
        :returns: path selected by the user
        :rtype: str or pathlib.Path object
        """
        if as_string:
            return self.path
        else:
            return Path(self.path)
