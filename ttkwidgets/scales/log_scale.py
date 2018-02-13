"""
Author: RedFantom
License: GNU GPLv3, as in LICENSE.md
Copyright (C) 2018 RedFantom
"""
# Basic UI imports
import tkinter as tk
from tkinter import ttk
# Standard library
import math


class LogarithmicScale(ttk.Frame):
    """
    ttk.Scale child widget that supports a logarithmic scale with
    specific unit processing.
    """

    options = [
        "start",
        "end",
        "precision",
        "unit",
        "show_value",
        "show_reset",
        "compound",
        "command",
        "default",
        "variable"
    ]

    prefixes = {
        -12: "p",
        -9:  "n",
        -6:  "\u03BC",
        -3:  "m",
        0:   "",
        3:   "k",
        6:   "M",
        9:   "G",
        12:  "T",
    }

    orders = [-12, -9, -6, -3, 0, 3, 6, 9, 12]

    def __init__(self, master, **kwargs):
        """
        :param start: Starting order of magnitude (0.001, 0.1, 10)
        :param end: Ending order of magnitude
        :param precision: Amount of supported relevant digits
        :param unit: str, without SI prefix
        :param show_value: Whether to show label with value
        :param show_reset: Whether to show reset Button
        :param compound: Location of value Label and reset Button
        :param default: Default value to set
        :param variable: tk.DoubleVar that gets updated with the value
            of the widget whenever the value is changed by callback or
            by UI change
        :param kwargs: Keyword arguments passed on to **ttk.Scale**
        """
        ttk.Frame.__init__(self, master)

        # Argument processing
        self._start = kwargs.pop("start", -3)
        self._end = kwargs.pop("end", 3)
        self._precision = kwargs.pop("precision", 3)
        self._unit = kwargs.pop("unit", "m")
        self._show_value = kwargs.pop("show_value", True)
        self._show_reset = kwargs.pop("show_reset", False)
        self._compound = kwargs.pop("compound", tk.BOTTOM)
        self._command = kwargs.pop("command", None)
        self._default = kwargs.pop("default", 1)
        self._variable = kwargs.pop("variable", tk.DoubleVar())

        # Widget creation
        self.variable = tk.IntVar()
        self._value = tk.DoubleVar()
        self._string = tk.StringVar()
        self.scale = ttk.Scale(self, **kwargs)
        self.label = ttk.Label(self, textvariable=self._string, justify=tk.CENTER)
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset)

        # Final actions
        self.configure_widgets()
        self.reset()
        self.grid_widgets()

    def configure_widgets(self):
        """Configure widgets with the arguments in attributes"""
        self.scale.config(
            from_=0, to=(self._end - self._start) * pow(10, self._precision),
            variable=self.variable, command=self._set_value
        )

    def grid_widgets(self):
        """
        Place widgets in the correct position based on compound
        """
        self.scale.grid(row=3, column=3, sticky="ns", padx=5, pady=5)
        # Support for different compound locations
        if self._compound == tk.BOTTOM:
            label_kwargs = {"row": 4, "column": 3, "padx": 5, "pady": (0, 5)}
            reset_kwargs = {"row": 5, "column": 3, "padx": 5, "pady": (0, 5)}
        elif self._compound == tk.TOP:
            label_kwargs = {"row": 1, "column": 3, "padx": 5, "pady": (5, 0)}
            reset_kwargs = {"row": 2, "column": 3, "padx": 5, "pady": (5, 0)}
        elif self._compound == tk.LEFT:
            label_kwargs = {"row": 3, "column": 2, "padx": (5, 0), "pady": 5}
            reset_kwargs = {"row": 3, "column": 1, "padx": (5, 0), "pady": 5}
        else:  # self._compound == tk.RIGHT:
            label_kwargs = {"row": 3, "column": 4, "padx": (0, 5), "pady": 5}
            reset_kwargs = {"row": 3, "column": 5, "padx": (0, 5), "pady": 5}
        # Label
        if self._show_value is True:
            self.label.grid(**label_kwargs)
        if self._show_reset is True:
            self.reset_button.grid(**reset_kwargs)
        # Configure rows and columns
        self.rowconfigure(tk.ALL, weight=1)
        self.columnconfigure(tk.ALL, weight=1)

    def grid_forget_widgets(self):
        """
        Removes all widgets from the grid
        """
        self.scale.grid_forget()
        self.label.grid_forget()
        self.reset_button.grid_forget()

    def _set_value(self, *args):
        """Set a new value for the Scale"""
        magn_r, val = divmod(self.raw, pow(10, self._precision))
        magn = magn_r + self._start
        value = (val / pow(10, self._precision - 1) * pow(10, magn)) if val != 0 else pow(10, magn)
        value = LogarithmicScale.round_precision(value, self._precision)
        self._value.set(value)
        # Update string
        prefix = None
        for order in self.orders:
            if abs(order - magn) <= 1:
                prefix = self.prefixes[order]
                break
        if prefix is not None:
            val = LogarithmicScale.round_precision(value * pow(10, -order), self._precision)
            raw_str = "{:" + str(self._precision) + "} {}{}"
            string = raw_str.format(val, prefix, self._unit)
        else:
            string = "{} {}".format(value, self._unit)
        self._string.set(string)
        # Master interaction
        if callable(self._command):
            self._command(value)
        self._variable.set(value)

    def reset(self):
        """Reset to the default value"""
        self._set_value(self._default)

    def cget(self, key):
        """Return option value"""
        if key in self.options:
            return getattr(self, "_{}".format(key))
        return ttk.Scale.cget(self.scale, key)

    def config(self, **kwargs):
        """Alias for self.configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure widget options"""
        for option in self.options:
            attr = "_{}".format(option)
            setattr(self, attr, kwargs.pop(option, getattr(self, attr)))
        self.configure_widgets()
        return ttk.Scale.configure(self.scale, **kwargs)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, key):
        return self.cget(key)

    @property
    def value(self):
        return self._value.get()

    @property
    def raw(self):
        return self.variable.get()

    @property
    def string(self):
        return self._string.get()

    @staticmethod
    def get_magnitude(value):
        return int(math.log10(value))

    @staticmethod
    def round_precision(value, precision):
        return round(value, -int(math.floor(math.log10(abs(value))) - (precision - 1))) if value != 0 else 0


if __name__ == '__main__':
    window = tk.Tk()
    scale = LogarithmicScale(window, orient=tk.VERTICAL, start=-3, end=3)
    scale.grid()
    window.mainloop()
