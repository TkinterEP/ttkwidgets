# Copyright (c) RedFantom 2017
import os
from PIL import Image, ImageTk
import string
from tkinter.font import Font


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def get_average_character_width(font):
    """
    Gets the average character width for a given tkinter font
    
    :param font: the font to use to measure average character width for.
    :type font: tkinter.font.Font, tuple
    
    :returns: average character width for the given font
    :rtype: float
    :raises: TypeError
    """
    
    def _avg(list_):
        return sum(list_) / len(list_)
    
    if isinstance(font, (tuple, list)):
        font = Font(font=tuple(font))
    elif not isinstance(font, Font):
        raise TypeError("font argument of function "
                        "'get_average_character_width' in "
                        "ttkwidgets.utilities is of type {} "
                        "instead of (tuple, tkinter.font.Font)".format(str(type(font))))
    return _avg([font.measure(c) for c in string.printable])