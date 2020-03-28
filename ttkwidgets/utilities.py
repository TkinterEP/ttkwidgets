# Copyright (c) RedFantom 2017
import os
from PIL import Image, ImageTk
import re


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def isfloat(value):
    if isinstance(value, float):
        return True
    if isinstance(value, str) and re.search(r'\d+[\.]\d*', value):
        return True
    if value.__class__.__name__ == 'FloatVar':
        return True
    return False


def isint(value):
    if isinstance(value, int):
        return True
    if isinstance(value, str) and value.isdigit():
        return True
    if value.__class__.__name__ == 'IntVar':
        return True
    return False
