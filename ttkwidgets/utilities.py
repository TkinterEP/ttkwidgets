"""
Author: The ttkwidgets authors
License: GNU GPLv3
Source: The ttkwidgets repository
"""
import os
from PIL import Image, ImageTk
import re


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def isfloat(value):
    """
    Checks if a value is a float
    :param value: any variable
    :returns: True if value is a float, string matching \d+\.\d* or tk.FloatVar
    """
    if isinstance(value, float):
        return True
    if isinstance(value, str) and re.search(r'\d+[\.]\d*', value):
        return True
    if value.__class__.__name__ == 'StringVar' and isfloat(value.get()):
        return True
    return False


def isint(value):
    """
    Checks if a value is an int
    :param value: any variable
    :returns: True if value is an int, string matching \d+ or tk.IntVar
    """
    if isinstance(value, int):
        return True
    if isinstance(value, str) and value.isdigit():
        return True
    if value.__class__.__name__ == 'IntVar':
        return True
    if value.__class__.__name__ == 'StringVar' and isint(value.get()):
        return True
    return False


def parse_geometry_string(string):
    """Parse a Tkinter geometry string ('XxY+W+H') into a box tuple"""
    e = string.split("x")
    w = int(e[0])
    e = e[1].split("+")
    h, x, y = map(int, e)
    return x, y, w, h
