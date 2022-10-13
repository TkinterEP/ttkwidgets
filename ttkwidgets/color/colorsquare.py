# -*- coding: utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: https://github.com/j4321/tkColorPicker

Edited by RedFantom for Python 2/3 cross-compatibility and docstring formatting
"""

"""
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

Color square gradient with selection cross
"""


from .functions import tk, round2, rgb_to_hexa, hue2col, rgb_to_hsv


class ColorSquare(tk.Canvas):
    """Square color gradient with selection cross."""

    def __init__(self, parent, hue, color=None, height=256, width=256, **kwargs):
        """
        Create a ColorSquare.

        :param parent: parent widget
        :type parent: widget
        :param hue: hue (between 0 and 360) of the color square gradient
                   (color in top right corner is (hue, 100, 100) in HSV)
        :type hue: int
        :param color: initially selected color given in HSV format
        :type color: tuple[int]
        :param height: height of the widget in pixels
        :type height: int
        :param width: width of the widget in pixels
        :type width: int
        :param kwargs: options to be passed on to the :class:`tk.Canvas` initializer
        """
        tk.Canvas.__init__(self, parent, height=height, width=width, **kwargs)
        self.bg = tk.PhotoImage(width=width, height=height, master=self)
        self._hue = hue
        if not color:
            color = hue2col(self._hue)
        self.bind('<Configure>', lambda e: self._draw(color))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _fill(self):
        """Create the gradient."""
        r, g, b = hue2col(self._hue)
        width = self.winfo_width()
        height = self.winfo_height()
        h = float(height - 1)
        w = float(width - 1)
        if height:
            c = [(r + i / h * (255 - r), g + i / h * (255 - g), b + i / h * (255 - b)) for i in range(height)]
            data = []
            for i in range(height):
                line = []
                for j in range(width):
                    rij = round2(j / w * c[i][0])
                    gij = round2(j / w * c[i][1])
                    bij = round2(j / w * c[i][2])
                    color = rgb_to_hexa(rij, gij, bij)
                    line.append(color)
                data.append("{" + " ".join(line) + "}")
            self.bg.put(" ".join(data))

    def _draw(self, color):
        """Draw the gradient and the selection cross on the canvas."""
        width = self.winfo_width()
        height = self.winfo_height()
        self.delete("bg")
        self.delete("cross_h")
        self.delete("cross_v")
        del self.bg
        self.bg = tk.PhotoImage(width=width, height=height, master=self)
        self._fill()
        self.create_image(0, 0, image=self.bg, anchor="nw", tags="bg")
        self.tag_lower("bg")
        h, s, v = color
        x = v / 100.
        y = (1 - s / 100.)
        self.create_line(0, y * height, width, y * height, tags="cross_h",
                         fill="#C2C2C2")
        self.create_line(x * width, 0, x * width, height, tags="cross_v",
                         fill="#C2C2C2")

    def get_hue(self):
        """Return current hue."""
        return self._hue

    def set_hue(self, value):
        """
        Change hue.

        :param value: new hue value (between 0 and 360)
        :type value: int
        """
        old = self._hue
        self._hue = value
        if value != old:
            self._fill()
            self.event_generate("<<ColorChanged>>")

    def _on_click(self, event):
        """Move cross on click."""
        x = event.x
        y = event.y
        self.coords('cross_h', 0, y, self.winfo_width(), y)
        self.coords('cross_v', x, 0, x, self.winfo_height())
        self.event_generate("<<ColorChanged>>")

    def _on_move(self, event):
        """Make the cross follow the cursor."""
        w = self.winfo_width()
        h = self.winfo_height()
        x = min(max(event.x, 0), w)
        y = min(max(event.y, 0), h)
        self.coords('cross_h', 0, y, w, y)
        self.coords('cross_v', x, 0, x, h)
        self.event_generate("<<ColorChanged>>")

    def get(self):
        """
        Get selected color.

        :return: color under cursor as a (RGB, HSV, HEX) tuple
        """
        x = self.coords('cross_v')[0]
        y = self.coords('cross_h')[1]
        xp = min(x, self.bg.width() - 1)
        yp = min(y, self.bg.height() - 1)
        try:
            r, g, b = self.bg.get(round2(xp), round2(yp))
        except ValueError:
            r, g, b = self.bg.get(round2(xp), round2(yp)).split()
            r, g, b = int(r), int(g), int(b)
        hexa = rgb_to_hexa(r, g, b)
        h = self.get_hue()
        s = round2((1 - float(y) / self.winfo_height()) * 100)
        v = round2(100 * float(x) / self.winfo_width())
        return (r, g, b), (h, s, v), hexa

    def set_rgb(self, sel_color):
        """
        Put cursor on sel_color given in RGB.

        :param sel_color: color in RBG format
        :type sel_color: sequence(int)
        """
        width = self.winfo_width()
        height = self.winfo_height()
        h, s, v = rgb_to_hsv(*sel_color)
        self.set_hue(h)
        x = v / 100.
        y = (1 - s / 100.)
        self.coords('cross_h', 0, y * height, width, y * height)
        self.coords('cross_v', x * width, 0, x * width, height)

    def set_hsv(self, sel_color):
        """
        Put cursor on sel_color given in HSV.

        :param sel_color: color in HSV format
        :type sel_color: sequence(int)
        """
        width = self.winfo_width()
        height = self.winfo_height()
        h, s, v = sel_color
        self.set_hue(h)
        x = v / 100.
        y = (1 - s / 100.)
        self.coords('cross_h', 0, y * height, width, y * height)
        self.coords('cross_v', x * width, 0, x * width, height)
