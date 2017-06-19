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


class ScaleEntry(ttk.Frame):
    """
    A simple combination of a Scale and an Entry widget suitable for use with int ranges.
    """
    def __init__(self, master=None, scalewidth=50, entrywidth=5, from_=0, to=50, compound=tk.RIGHT, **kwargs):
        """
        :param master: master widget
        :param scalewidth: width of the Scale in pixels
        :param entrywidth: width of the Entry in characters
        :param from_: start value of the scale
        :param to: end value of the scale
        :param compound: side the Entry must be on. Supports tk.LEFT, RIGHT, TOP and BOTTOM
        :param kwargs: keyword arguments passed on to Frame initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self.__limits = (from_, to)
        if compound is not tk.RIGHT and compound is not tk.LEFT and compound is not tk.TOP and \
                        compound is not tk.BOTTOM:
            raise ValueError("Invalid value for compound passed {0}".format(compound))
        self.__compound = compound
        self._variable = self.LimitedIntVar(from_, to)
        self._scale = ttk.Scale(self, from_=from_, to=to, length=scalewidth, command=self._on_scale,
                                variable=self._variable)
        # Note that the textvariable keyword argument is not used to pass the LimitedIntVar
        self._entry = ttk.Entry(self, width=entrywidth)
        self._entry.insert(0, str(from_))
        self._entry.bind("<KeyRelease>", self._on_entry)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts the widgets in the correct position based on self.__compound
        :return: None
        """
        self._scale.grid(row=1, column=1)
        self._entry.grid(row=0 if self.__compound is tk.TOP else 2 if self.__compound is tk.BOTTOM else 1,
                         column=0 if self.__compound is tk.LEFT else 2 if self.__compound is tk.RIGHT else 1)

    def _on_entry(self, event):
        """
        Callback for the Entry widget, sets the Scale variable to the appropriate value
        :param event: Tkinter event
        :return: None
        """
        contents = self._entry.get()
        if contents == "":
            return
        value = self._variable.set(int(contents))
        if not value:
            self._on_scale(None)

    def _on_scale(self, event):
        """
        Callback for the Scale widget, inserts an int value into the Entry
        :param event: Tkinter event
        :return:
        """
        self._entry.delete(0, tk.END)
        self._entry.insert(0, str(self._variable.get()))

    def config_entry(self, *args, **kwargs):
        """
        Wrapper around the Entry widget's config function for the user
        """
        self._entry.config(*args, **kwargs)

    def config_scale(self, *args, **kwargs):
        """
        Wrapper around the Scale widget's config function for the user
        """
        self._scale.config(*args, **kwargs)

    @property
    def value(self):
        """
        Get the value of the LimitedIntVar instance of the class
        """
        return self._variable.get()

    class LimitedIntVar(tk.IntVar):
        """
        Subclass of tk.IntVar that allows limits in the value of the variable stored
        """
        def __init__(self, low, high):
            self._low = low
            self._high = high
            tk.IntVar.__init__(self, value=low)

        def set(self, value):
            """
            Set a new value, but check whether it is in limits first. If not, return False and set the new value to
            either be the minimum (if value is smaller than the minimum) or the maximum (if the value is larger than
            the maximum). Both str and int are supported as value types, as long as the str contains an int.
            """
            if not isinstance(value, int):
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError("value argument passed is not int and cannot be converted to int")
            limited_value = max(min(self._high, value), self._low)
            tk.IntVar.set(self, limited_value)
            # Return False if the value had to be limited
            return limited_value is value
