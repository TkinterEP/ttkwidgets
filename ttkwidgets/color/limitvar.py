# -*- coding: utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: https://github.com/j4321/tkColorPicker

Edited by RedFantom for Python 2/3 cross-compatibility and docstring formatting


tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Limited StringVar
"""


from .functions import tk


class LimitVar(tk.StringVar):
    def __init__(self, from_, to, master=None, value=None, name=None):
        tk.StringVar.__init__(self, master, value, name)
        try:
            self._from = int(from_)
            self._to = int(to)
        except ValueError:
            raise ValueError("from_ and to should be integers.")
        if self._from >= self._to:
            raise ValueError("from_ should be smaller than to.")
        # ensure that the initial value is valid
        val = self.get()
        self.set(val)

    def get(self):
        """
        Convert the content to int between the limits of the variable.

        If the content is not an integer between the limits, the value is
        corrected and the corrected result is returned.
        """
        val = tk.StringVar.get(self)
        try:
            val = int(val)
            if val < self._from:
                val = self._from
                self.set(val)
            elif val > self._to:
                val = self._to
                self.set(val)
        except ValueError:
            val = 0
            self.set(0)
        return val
