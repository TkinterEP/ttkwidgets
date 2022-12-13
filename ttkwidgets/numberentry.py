"""
Author: rdbende
License: GNU GPLv3
Copyright (c) 2021 rdbende
"""

import tkinter as tk
from tkinter import ttk


class NumberEntry(ttk.Entry):
    """
    An entry that takes only numbers, calculations or variables,
    and calculates the result of the calculation
    """
    def __init__(self, master=None, allowed_chars={}, **kwargs):
        """
        Create a NumberEntry
        
        :param allowed_chars: Set the accepted variables, the name must be one single character
            e.g.: allowed_chars={'p': 3.14}
        :type allowed_chars: dict
        :param expressions: Allow the use of expressions (default is True)
        :type expressions: bool
        :param roundto: The number of decimals in the result (default is 0)
        :type roundto: int
        :param variables: Allow the use of the user specified variables
            specified in allowed_chars (default is True)
        :type variables: bool
        """
        self._allowed = allowed_chars
        self._expr = kwargs.pop("expressions", True)
        self._round = kwargs.pop("roundto", 0)
        self._vars = kwargs.pop("variables", True)
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
        for i in current:
            if i in self._allowed.keys():
                current = current.replace(i, str(self._allowed[i]))
        if current:
            try:
                if int(self._round) == 0:
                    result = int(round(eval(current), 0))
                    self.delete(0, tk.END)
                    self.insert(0, result)         
                else:
                    result = round(float(eval(current)), self._round)
                    self.delete(0, tk.END)
                    self.insert(0, result)
            except SyntaxError:
                self.delete(0, tk.END)
                self.insert(0, "SyntaxError")
                self.select_range(0, tk.END)
            except ZeroDivisionError:
                self.delete(0, tk.END)
                self.insert(0, "ZeroDivisionError")
                self.select_range(0, tk.END)
      
    def _check(self, *args):
        typed = self.get()
        if not typed == "SyntaxError" and not typed == "ZeroDivisionError":
            if self._expr:
                allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "%", "."]
            else:
                allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
            if self._vars:
                allowed.extend(self._allowed.keys())
            for current in typed:
                if not current in allowed:
                    typed = typed.replace(current, "")
            self.delete(0, tk.END)
            self.insert(0, typed)

    def configure(self, allowed_chars={}, **kwargs):
        """Configure resources of the widget"""
        self._allowed = allowed_chars
        self._expr = kwargs.pop("expressions", self._expr)
        self._round = kwargs.pop("roundto", self._round)
        self._vars = kwargs.pop("variables", self._vars)
        ttk.Entry.configure(self, **kwargs)

    config = configure
    
    def cget(self, key):
        """Return the resource value for a KEY given as string"""
        if key == "allowed_chars":
            return self._allowed
        elif key == "expressions":
            return self._expr
        elif key == "roundto":
            return self._round
        elif key == "variables":
            return self._vars        
        else:
            return ttk.Entry.cget(self, key)
        
    def keys(self):
        """Return a list of all resource names of this widget"""
        keys = ttk.Entry.keys(self)
        keys.extend(["allowed_chars", "expressions", "roundto", "variables"])
        keys.sort()
        return keys
