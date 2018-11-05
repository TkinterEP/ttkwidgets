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
from ttkwidgets import AutoHideScrollbar


class ScrolledListbox(ttk.Frame):
    """Simple :class:`tk.Listbox` with an added scrollbar."""
    def __init__(self, master=None, compound=tk.RIGHT, autohidescrollbar=True, **kwargs):
        """
        Create a Listbox with a vertical scrollbar.

        :param master: master widget
        :type master: widget
        :param compound: side for the Scrollbar to be on (:obj:`tk.LEFT` or :obj:`tk.RIGHT`)
        :type compound: str
        :param autohidescrollbar: whether to use an :class:`~ttkwidgets.AutoHideScrollbar` or a :class:`ttk.Scrollbar`
        :type autohidescrollbar: bool
        :param kwargs: keyword arguments passed on to the :class:`tk.Listbox` initializer
        """
        ttk.Frame.__init__(self, master)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.listbox = tk.Listbox(self, **kwargs)
        if autohidescrollbar:
            self.scrollbar = AutoHideScrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        else:
            self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.config_listbox(yscrollcommand=self.scrollbar.set)
        if compound is not tk.LEFT and compound is not tk.RIGHT:
            raise ValueError("Invalid compound value passed: {0}".format(compound))
        self.__compound = compound
        self._grid_widgets()

    def _grid_widgets(self):
        """Puts the two whole widgets in the correct position depending on compound."""
        scrollbar_column = 0 if self.__compound is tk.LEFT else 2
        self.listbox.grid(row=0, column=1, sticky="nswe")
        self.scrollbar.grid(row=0, column=scrollbar_column, sticky="ns")

    def config_listbox(self, *args, **kwargs):
        """Configure resources of the Listbox widget."""
        self.listbox.configure(*args, **kwargs)

