"""
Author: rdbende
License: GNU GPLv3
Copyright (c) 2021 rdbende
"""

import tkinter as tk
from tkinter import ttk


class NumberEntry(ttk.Entry):
    """
    An entry that takes only numbers or calculations and calculates the result of the calculation
    """
    def __init__(self, master=None, **kwargs):
        """
        Create a NumberEntry
        
        :param expressions: Allow the use of expressions (default is True)
        :type expressions: bool
        :param roundto: The number of decimals in the result (default is 0)
        :type roundto: int
        """
        self._expr = kwargs.pop("expressions", True)
        self._round = kwargs.pop("roundto", 0)
        ttk.Entry.__init__(self, master, **kwargs)
        self.bind("<Return>", self._eval)
        self.bind("<FocusOut>", self._eval)
        self.bind("<KeyRelease>", self._check)
        
    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})
    
    def _eval(self, *args):
        """Calculate the result of the entered calculation"""
        current = self.get()
        try:
            if len(current) > 0:
                if int(self._round) == 0:
                    result = int(round(eval(current), 0))
                    self.delete(0, "end")
                    self.insert(0, result)         
                else:
                    result = round(float(eval(current)), self._round)
                    self.delete(0, "end")
                    self.insert(0, result)
        except SyntaxError:
            self.delete(0, "end")
            self.insert(0, "SyntaxError")
            self.select_range(0, "end")
        except ZeroDivisionError:
            self.delete(0, "end")
            self.insert(0, "ZeroDivisionError")
            self.select_range(0, "end")
        
    def _check(self, *args):
        typed = self.get()
        if not typed == "SyntaxError" and not typed == "ZeroDivisionError":
            checked = self._replace(typed)
            self.delete(0, "end")
            self.insert(0, checked)
        
    def _replace(self, typed) -> str:
        """Delete the not allowed characters"""
        if self._expr:
            allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "%", "."]
        else:
            allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        for current in typed:
            if not current in allowed:
                typed = typed.replace(current, "")
        return typed

    def configure(self, **kwargs):
        """Configure resources of the widget."""
        self._expr = kwargs.pop("expressions", self._expr)
        self._round = kwargs.pop("roundto", self._round)
        ttk.Entry.configure(self, **kwargs)

    config = configure
    
    def cget(self, key):
        """Return the resource value for a KEY given as string"""
        if key == "expressions":
            return self._expr
        elif key == "roundto":
            return self._round
        else:
            return ttk.Entry.cget(self, key)
        
    def keys(self):
        """Return a list of all resource names of this widget"""
        keys = ttk.Entry.keys(self)
        keys.extend(["expressions", "roundto"])
        keys = sorted(keys)
        return keys
