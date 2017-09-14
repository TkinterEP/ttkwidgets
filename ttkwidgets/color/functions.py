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

Functions and constants
"""


try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from PIL import Image, ImageDraw, ImageTk
from math import atan2, sqrt, pi
import colorsys


PALETTE = ("red", "dark red", "orange", "yellow", "green", "lightgreen", "blue",
           "royal blue", "sky blue", "purple", "magenta", "pink", "black",
           "white", "gray", "saddle brown", "lightgray", "wheat")


# in some python versions round returns a float instead of an int
if not isinstance(round(1.0), int):
    def round2(nb):
        """Round number to 0 digits and return an int."""
        return int(nb + 0.5)  # works because nb >= 0
else:
    round2 = round


# --- conversion functions
def rgb_to_hsv(r, g, b):
    """Convert RGB color to HSV."""
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    return round2(h * 360), round2(s * 100), round2(v * 100)


def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB."""
    r, g, b = colorsys.hsv_to_rgb(h / 360., s / 100., v / 100.)
    return round2(r * 255), round2(g * 255), round2(b * 255)


def rgb_to_hexa(*args):
    """Convert RGB(A) color to hexadecimal."""
    if len(args) == 3:
        return ("#%2.2x%2.2x%2.2x" % tuple(args)).upper()
    elif len(args) == 4:
        return ("#%2.2x%2.2x%2.2x%2.2x" % tuple(args)).upper()
    else:
        raise ValueError("Wrong number of arguments.")


def hexa_to_rgb(color):
    """Convert hexadecimal color to RGB."""
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    if len(color) == 7:
        return r, g, b
    elif len(color) == 9:
        return r, g, b, int(color[7:9], 16)
    else:
        raise ValueError("Invalid hexadecimal notation.")


def col2hue(r, g, b):
    """Return hue value corresponding to given RGB color."""
    return round2(180 / pi * atan2(sqrt(3) * (g - b), 2 * r - g - b) + 360) % 360


def hue2col(h):
    """Return the color in RGB format corresponding to (h, 100, 100) in HSV."""
    if h < 0 or h > 360:
        raise ValueError("Hue should be between 0 and 360")
    else:
        return hsv_to_rgb(h, 100, 100)


# --- Fake transparent image creation with PIL
def create_checkered_image(width, height, c1=(154, 154, 154, 255),
                           c2=(100, 100, 100, 255), s=6):
    """
    Return a checkered image of size width x height.

    Arguments:
        * width: image width
        * height: image height
        * c1: first color (RGBA)
        * c2: second color (RGBA)
        * s: size of the squares
    """
    im = Image.new("RGBA", (width, height), c1)
    draw = ImageDraw.Draw(im, "RGBA")
    for i in range(s, width, 2 * s):
        for j in range(0, height, 2 * s):
            draw.rectangle(((i, j), ((i + s - 1, j + s - 1))), fill=c2)
    for i in range(0, width, 2 * s):
        for j in range(s, height, 2 * s):
            draw.rectangle(((i, j), ((i + s - 1, j + s - 1))), fill=c2)
    return im


def overlay(image, color):
    """
    Overlay a rectangle of color (RGBA) on the image and return the result.
    """
    width, height = image.size
    im = Image.new("RGBA", (width, height), color)
    preview = Image.alpha_composite(image, im)
    return preview
