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

Alpha channel gradient bar
"""


from PIL import Image, ImageTk
from .functions import tk, round2, rgb_to_hsv
from .functions import create_checkered_image


class AlphaBar(tk.Canvas):
    """Bar to select alpha value."""

    def __init__(self, parent, alpha=255, color=(255, 0, 0), height=11,
                 width=256, variable=None, **kwargs):
        """
        Create a bar to select the alpha value.

        :param parent: parent widget
        :type parent: widget
        :param alpha: initially selected alpha value (between 0 and 255)
        :type alpha: int
        :param color: gradient color in RGB format
        :type color: tuple[int]
        :param variable: variable linked to the alpha value
        :type variable: IntVar
        :param height: height of the widget in pixels
        :type height: int
        :param width: width of the widget in pixels
        :type width: int
        :param kwargs: options to be passed on to the :class:`tk.Canvas` initializer
        """
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)
        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        self._variable = variable
        if variable is not None:
            try:
                alpha = int(variable.get())
            except Exception:
                pass
        else:
            self._variable = tk.IntVar(self)
        if alpha > 255:
            alpha = 255
        elif alpha < 0:
            alpha = 0
        self._variable.set(alpha)
        try:
            self._variable.trace_add("write", self._update_alpha)
        except Exception:
            self._variable.trace("w", self._update_alpha)

        self.bind('<Configure>', lambda e: self._draw_gradient(alpha, color))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _draw_gradient(self, alpha, color):
        """Draw the gradient and put the cursor on alpha."""
        self.delete("gradient")
        self.delete("cursor")
        del self.gradient
        width = self.winfo_width()
        height = self.winfo_height()

        bg = create_checkered_image(width, height)
        r, g, b = color
        w = width - 1.
        gradient = Image.new("RGBA", (width, height))
        for i in range(width):
            for j in range(height):
                gradient.putpixel((i, j), (r, g, b, round2(i / w * 255)))
        self.gradient = ImageTk.PhotoImage(Image.alpha_composite(bg, gradient),
                                           master=self)

        self.create_image(0, 0, anchor="nw", tags="gardient",
                          image=self.gradient)
        self.lower("gradient")

        x = alpha / 255. * width
        h, s, v = rgb_to_hsv(r, g, b)
        if v < 50:
            fill = "gray80"
        else:
            fill = 'black'
        self.create_line(x, 0, x, height, width=2, tags='cursor', fill=fill)

    def _on_click(self, event):
        """Move selection cursor on click."""
        x = event.x
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((255. * x) / self.winfo_width()))

    def _on_move(self, event):
        """Make selection cursor follow the cursor."""
        w = self.winfo_width()
        x = min(max(event.x, 0), w)
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((255. * x) / w))

    def _update_alpha(self, *args):
        alpha = int(self._variable.get())
        if alpha > 255:
            alpha = 255
        elif alpha < 0:
            alpha = 0
        self.set(alpha)
        self.event_generate("<<AlphaChanged>>")

    def get(self):
        """Return alpha value of color under cursor."""
        coords = self.coords('cursor')
        return round2((255. * coords[0]) / self.winfo_width())

    def set(self, alpha):
        """
        Set cursor position on the color corresponding to the alpha value.

        :param alpha: new alpha value (between 0 and 255)
        :type alpha: int
        """
        if alpha > 255:
            alpha = 255
        elif alpha < 0:
            alpha = 0
        x = alpha / 255. * self.winfo_width()
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(alpha)

    def set_color(self, color):
        """
        Change gradient color and change cursor position if an alpha value is supplied.

        :param color: new gradient color in RGB(A) format
        :type color: tuple[int]
        """
        if len(color) == 3:
            alpha = self.get()
        else:
            alpha = color[3]
        self._draw_gradient(alpha, color[:3])
