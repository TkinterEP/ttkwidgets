"""
Author: RedFantom and Juliette Monsel
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
    def __init__(self, master=None, scalewidth=50, entrywidth=5, from_=0, to=50,
                 orient=tk.HORIZONTAL, compound=tk.RIGHT, entryscalepad=0, **kwargs):
        """
        Create a ScaleEntry.
        
        :param master: master widget
        :type master: widget
        :param scalewidth: width of the Scale in pixels
        :type scalewidth: int
        :param entrywidth: width of the Entry in characters
        :type entrywidth: int
        :param from\_: start value of the scale
        :type from\_: int
        :param to: end value of the scale
        :type to: int
        :param orient: scale orientation. Supports :obj:`tk.HORIZONTAL` and :obj:`tk.VERTICAL`
        :type orient: str
        :param compound: side the Entry must be on. Supports :obj:`tk.LEFT`,
                         :obj:`tk.RIGHT`, :obj:`tk.TOP` and :obj:`tk.BOTTOM`
        :type compound: str
        :param entryscalepad: space between the entry and the scale
        :type entryscalepad: int
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        if compound is not tk.RIGHT and compound is not tk.LEFT and compound is not tk.TOP and \
           compound is not tk.BOTTOM:
            raise ValueError("Invalid value for compound passed {0}".format(compound))
        self.__compound = compound
        if not isinstance(entryscalepad, int):
            raise TypeError("entryscalepad not of int type")
        self.__entryscalepad = entryscalepad
        self._variable = self.LimitedIntVar(from_, to)
        self._scale = ttk.Scale(self, from_=from_, to=to, length=scalewidth,
                                orient=orient, command=self._on_scale,
                                variable=self._variable)
        # Note that the textvariable keyword argument is not used to pass the LimitedIntVar
        self._entry = ttk.Entry(self, width=entrywidth)
        self._entry.insert(0, str(from_))
        self._entry.bind("<KeyRelease>", self._on_entry)
        self._grid_widgets()

    def _grid_widgets(self):
        """Put the widgets in the correct position based on self.__compound."""
        orient = str(self._scale.cget('orient'))
        self._scale.grid(row=2, column=2, sticky='ew' if orient == tk.HORIZONTAL else 'ns',
                         padx=(0, self.__entryscalepad) if self.__compound is tk.RIGHT else
                              (self.__entryscalepad, 0) if self.__compound is tk.LEFT else 0,
                         pady=(0, self.__entryscalepad) if self.__compound is tk.BOTTOM else
                              (self.__entryscalepad, 0) if self.__compound is tk.TOP else 0)
        self._entry.grid(row=1 if self.__compound is tk.TOP else 3 if self.__compound is tk.BOTTOM else 2,
                         column=1 if self.__compound is tk.LEFT else 3 if self.__compound is tk.RIGHT else 2)

        if orient == tk.HORIZONTAL:
            self.columnconfigure(0, weight=0)
            self.columnconfigure(2, weight=1)
            self.columnconfigure(4, weight=0)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(2, weight=0)
            self.rowconfigure(4, weight=1)

        else:
            self.rowconfigure(0, weight=0)
            self.rowconfigure(2, weight=1)
            self.rowconfigure(4, weight=0)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(2, weight=0)
            self.columnconfigure(4, weight=1)

    def _on_entry(self, event):
        """
        Callback for the Entry widget, sets the Scale variable to the appropriate value.
        
        :param event: Tkinter event
        """
        contents = self._entry.get()
        if contents == "":
            return
        try:
            value = self._variable.set(int(contents))
        except ValueError:
            value = None
        if not value:
            self._on_scale(None)

    def _on_scale(self, event):
        """
        Callback for the Scale widget, inserts an int value into the Entry.

        :param event: Tkinter event
        """
        self._entry.delete(0, tk.END)
        self._entry.insert(0, str(self._variable.get()))

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        return self.configure({key: value})

    def keys(self):
        keys = ttk.Frame.keys(self)
        keys.extend(['scalewidth', 'entrywidth', 'from', 'to',
                     'compound', 'entryscalepad', 'orient'])
        keys.sort()
        return keys

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method :meth:`~ScaleEntry.keys`.
        """
        if key == 'scalewidth':
            return self._scale.cget('length')
        elif key == 'from':
            return self._scale.cget('from')
        elif key == 'to':
            return self._scale.cget('to')
        elif key == 'entrywidth':
            return self._entry.cget('width')
        elif key == 'entryscalepad':
            return self.__entryscalepad
        elif key == 'compound':
            return self.__compound
        elif key == 'orient':
            return str(self._scale.cget('orient'))
        else:
            return ttk.Frame.cget(self, key)

    def cget_entry(self, key):
        """
        Query the Entry widget's option.

        :param key: option name
        :type key: str
        :return: value of the option
        """
        return self._entry.cget(key)

    def cget_scale(self, key):
        """
        Query the Scale widget's option.

        :param key: option name
        :type key: str
        :return: value of the option
        """
        return self._scale.cget(key)

    def configure(self, cnf={}, **kw):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method :meth:`~ScaleEntry.keys`.
        See :meth:`~ScaleEntry.__init__` for a description of the widget specific option.
        """
        kw.update(cnf)
        reinit = False
        if 'scalewidth' in kw:
            self._scale.configure(length=kw.pop('scalewidth'))
        if 'from' in kw:
            from_ = kw.pop('from')
            self._scale.configure(from_=from_)
            self._variable.configure(low=from_)
        if 'from_' in kw:
            from_ = kw.pop('from_')
            self._scale.configure(from_=from_)
            self._variable.configure(low=from_)
        if 'to' in kw:
            to = kw.pop('to')
            self._scale.configure(to=to)
            self._variable.configure(high=to)
        if 'entrywidth' in kw:
            self._entry.configure(width=kw.pop('entrywidth'))
        if 'compound' in kw:
            compound = kw.pop('compound')
            if compound is not tk.RIGHT and compound is not tk.LEFT and \
               compound is not tk.TOP and compound is not tk.BOTTOM:
                raise ValueError("Invalid value for compound passed {0}".format(compound))
            else:
                self.__compound = compound
                reinit = True
        if 'orient' in kw:
            self._scale.configure(orient=kw.pop('orient'))
            reinit = True
        if 'entryscalepad' in kw:
            entryscalepad = kw.pop('entryscalepad')
            try:
                self.__entryscalepad = int(entryscalepad)
                reinit = True
            except ValueError:
                raise ValueError("Invalid value for entryscalepad passed {0}".format(entryscalepad))
        ttk.Frame.configure(self, kw)
        if reinit:
            self._grid_widgets()

    config = configure

    def config_entry(self, cnf={}, **kwargs):
        """Configure resources of the Entry widget."""
        self._entry.config(cnf, **kwargs)

    def config_scale(self, cnf={}, **kwargs):
        """Configure resources of the Scale widget."""
        self._scale.config(cnf, **kwargs)
        # Update self._variable limits in case the ones of the scale have changed
        self._variable.configure(high=self._scale['to'],
                                 low=self._scale['from'])
        if 'orient' in cnf or 'orient' in kwargs:
            self._grid_widgets()

    @property
    def value(self):
        """Get the value of the :class:`LimitedIntVar` instance of the class."""
        return self._variable.get()

    class LimitedIntVar(tk.IntVar):
        """Subclass of :class:`tk.IntVar` that allows limits in the value of the variable stored."""
        def __init__(self, low, high):
            self._low = low
            self._high = high
            tk.IntVar.__init__(self, value=low)

        def configure(self, **kwargs):
            """Configure the limits of the LimitedIntVar."""
            self._low = kwargs.get('low', self._low)
            self._high = kwargs.get('high', self._high)
            if self.get() < self._low:
                self.set(self._low)
            elif self.get() > self._high:
                self.set(self._high)

        def set(self, value):
            """
            Set a new value.

            Check whether value is in limits first. If not, return False and set
            the new value to either be the minimum (if value is smaller than the
            minimum) or the maximum (if the value is larger than the maximum).
            Both str and int are supported as value types, as long as the str
            contains an int.

            :param value: new value
            :type value: int
            """
            if not isinstance(value, int):
                raise TypeError("value can only be of int type")
            limited_value = max(min(self._high, value), self._low)
            tk.IntVar.set(self, limited_value)
            # Return False if the value had to be limited
            return limited_value is value
