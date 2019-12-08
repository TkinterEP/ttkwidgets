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

HSV gradient bar
"""


from .functions import tk, round2, rgb_to_hexa, hue2col


class GradientBar(tk.Canvas):
    """HSV gradient colorbar with selection cursor."""

    def __init__(self, parent, hue=0, height=11, width=256, variable=None,
                 **kwargs):
        """
        Create a GradientBar.

        :param parent: parent widget
        :type parent: widget
        :param hue: initially selected hue value (between 0 and 360)
        :type hue: int
        :param variable: variable linked to the hue value
        :type variable: IntVar
        :param height: height of the widget in pixels
        :type height: int
        :param width: width of the widget in pixels
        :type width: int
        :param kwargs: options to be passed on to the :class:`tk.Canvas` initializer
        """
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)

        self._variable = variable
        if variable is not None:
            try:
                hue = int(variable.get())
            except Exception:
                pass
        else:
            self._variable = tk.IntVar(self)
        if hue > 360:
            hue = 360
        elif hue < 0:
            hue = 0
        self._variable.set(hue)
        try:
            self._variable.trace_add("write", self._update_hue)
        except Exception:
            self._variable.trace("w", self._update_hue)

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        self.bind('<Configure>', lambda e: self._draw_gradient(hue))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _draw_gradient(self, hue):
        """Draw the gradient and put the cursor on hue."""
        self.delete("gradient")
        self.delete("cursor")
        del self.gradient
        width = self.winfo_width()
        height = self.winfo_height()

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        line = []
        for i in range(width):
            line.append(rgb_to_hexa(*hue2col(float(i) / width * 360)))
        line = "{" + " ".join(line) + "}"
        self.gradient.put(" ".join([line for j in range(height)]))
        self.create_image(0, 0, anchor="nw", tags="gradient",
                          image=self.gradient)
        self.lower("gradient")

        x = hue / 360. * width
        self.create_line(x, 0, x, height, width=2, tags='cursor')

    def _on_click(self, event):
        """Move selection cursor on click."""
        x = event.x
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((360. * x) / self.winfo_width()))

    def _on_move(self, event):
        """Make selection cursor follow the cursor."""
        w = self.winfo_width()
        x = min(max(event.x, 0), w)
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((360. * x) / w))

    def _update_hue(self, *args):
        hue = int(self._variable.get())
        if hue > 360:
            hue = 360
        elif hue < 0:
            hue = 0
        self.set(hue)
        self.event_generate("<<HueChanged>>")

    def get(self):
        """Return hue of color under cursor."""
        coords = self.coords('cursor')
        return round2(360 * coords[0] / self.winfo_width())

    def set(self, hue):
        """
        Set cursor position on the color corresponding to the hue value.

        :param hue: new hue value (between 0 and 360)
        :type hue: int
        """
        if hue > 360:
            hue = 360
        elif hue < 0:
            hue = 0
        x = hue / 360. * self.winfo_width()
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(hue)
