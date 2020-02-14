# Copyright (c) RedFantom 2017
import os
from PIL import Image, ImageTk


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def get_widget_options(widget):
    """
    Gets the options from a widget

    :param widget: tkinter.Widget instance to get the config options from
    :return: dict of options that you can pass on to widget.config()
    """
    options = {}
    for key in widget.keys():
        value = widget.cget(key)
        if value not in ("", None):
            options[key] = value
    return options
