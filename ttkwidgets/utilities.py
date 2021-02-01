"""
Author: The ttkwidgets authors
License: GNU GPLv3
Source: The ttkwidgets repository
"""
import os
from PIL import Image, ImageTk


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def parse_geometry_string(string):
    """Parse a Tkinter geometry string ('XxY+W+H') into a box tuple"""
    e = string.split("x")
    w = int(e[0])
    e = e[1].split("+")
    h, x, y = map(int, e)
    return x, y, w, h
