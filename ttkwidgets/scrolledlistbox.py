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


class ScrolledListbox(ttk.Frame):
    """
    Simple Listbox with an added scrollbar
    """
    def __init__(self, master=None, compound=tk.RIGHT, **kwargs):
        """
        :param master: master widget
        :param compound: side for the Scrollbar to be on (tk.LEFT or tk.RIGHT)
        :param listheight: height of the Listbox in items
        :param listwidth: width of the Listbox in characters
        :param kwargs: keyword arguments passed on to Listbox initializer
        """
        ttk.Frame.__init__(self, master)
        self.listbox = tk.Listbox(self, **kwargs)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.config_listbox(yscrollcommand=self.scrollbar.set)
        if compound is not tk.LEFT and compound is not tk.RIGHT:
            raise ValueError("Invalid compound value passed: {0}".format(compound))
        self.__compound = compound
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts the two whole widgets in the correct position depending on compound
        :return: None
        """
        scrollbar_column = 0 if self.__compound is tk.LEFT else 2
        self.listbox.grid(row=0, column=1, sticky="nswe")
        self.scrollbar.grid(row=0, column=scrollbar_column, sticky="ns")

    def config_listbox(self, *args, **kwargs):
        """
        Pass on arguments to listbox.configure
        """
        self.listbox.configure(*args, **kwargs)

