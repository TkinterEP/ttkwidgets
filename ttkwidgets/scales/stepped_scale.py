"""
Author: RedFantom
License: GNU GPLv3, as in LICENSE.md
Copyright (C) 2018 RedFantom
"""
# Basic UI imports
import tkinter as tk
from tkinter import ttk


class SteppedScale(ttk.Frame):
    """
    Frame with a Scale that can move in steps, a reset button to reset
    to a default value, and a label to show the value that is set for
    the Scale with a possible unit if it is set in the steps.
    """

    options = [
        "steps",
        "default",
        "compound",
        "show_value",
        "show_reset",
        "unit",
        "command",
        "variable",
        "reverse"
    ]

    def __init__(self, master, **kwargs):
        """
        :param steps: list of steps available
        :param default: index of step set on start and reset
        :param compound: location of reset button and value label
        :param show_value: whether to show value label
        :param show_reset: whether to show reset button
        :param unit: str appended to the label
        :param command: Callback called upon change with new value as arg
        :param variable: tk.StringVar to store value in
        :param kwargs: Keyword arguments passed on to Scale initializer
        """
        ttk.Frame.__init__(self, master)

        # Argument processing
        self._steps = kwargs.pop("steps", ["50mV", "100mV", "500mV", "1V", "5V"])
        self._default = kwargs.pop("default", 0)
        self._compound = kwargs.pop("compound", tk.BOTTOM)
        self._show_value = kwargs.pop("show_value", True)
        self._show_reset = kwargs.pop("show_reset", True)
        self._unit = kwargs.pop("unit", str())
        self._command = kwargs.pop("command", None)
        self._variable = kwargs.pop("variable", tk.StringVar())
        reverse = kwargs.pop("reverse", True)
        self.check_reverse(reverse)

        # Widget creation
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset)
        self.variable = tk.IntVar()
        self._value = tk.StringVar()
        self.scale = ttk.Scale(
            self, from_=0, to=len(self._steps) - 1, variable=self.variable, command=self.check_value, **kwargs)
        self.label = ttk.Label(self, textvariable=self._value, justify=tk.CENTER)

        # Final actions
        self.reset()
        self.grid_widgets()

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

    def check_value(self, value=None):
        """
        Limit value and set label.
        Limits: 0 to the maximum index of self._steps
        Label: Set to self._steps[value]
        """
        value = self.variable.get() if value is None else (eval(value) if isinstance(value, str) else value)
        value = max(min(int(round(value)), len(self._steps) - 1), 0)
        self.variable.set(value)
        self._value.set(self._steps[value] + self._unit)
        # Call callback
        if callable(self._command):
            self._command(self.value)
        if isinstance(self._variable, tk.StringVar):
            self._variable.set(self.value)
        return

    def reset(self):
        """Reset to the default value"""
        self.check_value(self._default)

    def check_reverse(self, reverse):
        """Reverses the steps if reverse is True"""
        if reverse is True:
            self._steps = list(reversed(self._steps))
            self._default = len(self._steps) - 1 - self._default
        return reverse

    def cget(self, key):
        """Return value for a keyword argument"""
        if key in self.options:
            return getattr(self, "_{}".format(key))
        return ttk.Scale.cget(self.scale, key)

    def config(self, **kwargs):
        """Alias of self.configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure options of widget"""
        self._steps = kwargs.pop("steps", self._steps)
        self.scale.configure(to=len(self._steps) - 1)
        self._default = kwargs.pop("default", self._default)
        self._compound = kwargs.pop("compound", self._compound)
        self._show_value = kwargs.pop("show_value", self._show_value)
        self._unit = kwargs.pop("unit", self._unit)
        self._command = kwargs.pop("command", self._command)
        self._variable = kwargs.pop("variable", self._variable)
        reverse = kwargs.pop("reverse", False)
        self.check_reverse(reverse)
        return ttk.Scale.configure(self.scale, **kwargs)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, key):
        return self.cget(key)

    @property
    def value(self):
        return self._steps[self.variable.get()]

    @property
    def raw(self):
        return self.variable.get()


if __name__ == '__main__':
    window = tk.Tk()
    scale = SteppedScale(window, orient=tk.VERTICAL)
    scale.grid()
    window.mainloop()
