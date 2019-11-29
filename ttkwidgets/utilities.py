# Copyright (c) RedFantom 2017
import os
from PIL import Image, ImageTk
import tkinter as tk
import textwrap
import string

from ttkwidgets.errors import I18NError, AssetNotFoundError, AssetMaskNotFoundError
import ttkwidgets.bitmap_assets


def get_assets_directory():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))


def open_icon(icon_name):
    return ImageTk.PhotoImage(Image.open(os.path.join(get_assets_directory(), icon_name)))


def get_bitmap(bitmap_name, has_mask=True, **kwargs):
    """
    Gets a tkinter.BitmapImage from the ttkwidgets.bitmap_assets submodule.
    
    :param bitmap_name: name of the bitmap to get from the ttkwidgets.bitmap_assets submodule
    :type bitmap_name: str
    :param has_mask: boolean that defines if the selected bitmap has a mask
    :type has_mask: bool
    :param **kwargs: dictionary of keyword arguments to pass to tkinter.BitmapImage()
    :type kwargs: dict
    
    :returns: Bitmap image constructed from the data in bitmap_assets
    :raises: ttkwidgets.errors.AssetNotFoundError if the bitmap can't be found
    :raises: ttkwidgets.errors.AssetMaskNotFoundError if the bitmap has a mask, and the mask can't be found.
    """
    bitmask = kwargs.pop("maskdata", None) or bitmap_name + "_mask"
    if bitmap_name not in ttkwidgets.bitmap_assets.__dict__:
        raise AssetNotFoundError("Asset {} was not found in module 'ttkwidgets.bitmap_assets'".format(bitmap_name))
    if bitmask not in ttkwidgets.bitmap_assets.__dict__ and has_mask:
        raise AssetMaskNotFoundError("Asset mask {} was not found in module 'ttkwidgets.bitmap_assets'".format(bitmask))
    
    return tk.BitmapImage(data=ttkwidgets.bitmap_assets.__dict__[bitmap_name],
                          maskdata=ttkwidgets.bitmap_assets.__dict__[bitmask],
                          **kwargs)


def auto_scroll(sbar, first, last):
    """
    Hide and show scrollbar as needed.

    :param sbar: tk.Scrollbar to show/hide
    :param first: float representing the start point of the scrollbar
    :param last: float representing the end point of the scrollbar

    :returns: None, sets the scrollbar to the tuple (first, last) and shows/hides
    the scrollbar depending on whether it is necessary for it to show up or not.
    """
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


def get_root_widget(widget):
    """
    Gets the root widget from any child widget.

    :param widget: tkinter.Widget to get the root widget from.

    :return: root widget
    """
    while widget.master is not None:
        widget = widget.master
    return widget


def i18n(text, dst_lang=None, wrapping=0):
    """
    Translates a text from a source lang to another.

    :param text: (required) source text to translate
    :param dst_lang: (default: None) dictionary mapping {src:dst} from source
                     lang to destination lang. Use tkinterpp.utils.get_i18n_dict to
                     load a matching dict from a file.
    :param wrapping: (default: 0) number of characters to wrap the resulting string at
                      using textwrap.wrap, long uninterrupted lines will still be wrapped at
                      the exact desired width. If wrapping <= 0, no wrapping will be applied.
    :return: translated text
    :raises: ttkwidgets.errors.I18NError if dst_lang is not None or dict.
    """
    if dst_lang is None:
        return text if wrapping <= 0 else textwrap.wrap(text, wrapping)

    if isinstance(dst_lang, dict):
        dst_text = dst_lang.get(text, text)
        if wrapping > 0:
            dst_text = textwrap.wrap(dst_text, wrapping)
        return dst_text

    raise I18NError("dst_lang argument should be of type NoneType or dict")


def get_i18n_dict(file_path):
    """
    Gets a tkinterpp.utils.i18n compatible dictionary from a file.

    The file should be formatted as such :

    "Original language text" : "texte dans la langue originale"
    "Another string" : "Une autre chaîne de caractères"

    and so on.

    :param file_path: a path to the file to load
    :return: dict of <src>:<dst> pairs to use in i18n function.
    """
    rv = {}
    with open(file_path, "r") as f:
        for line in f:
            splits = line.split('"')
            key = splits[1]
            value = splits[-2]
            rv[key] = value
    return rv

def get_widget_type(widget):
    """
    Gets the type of a given widget

    :param widget: widget to get the type of
    :return: string of the type of the widget
    """
    class_ = widget.winfo_class()
    if class_[0] == "T" and class_[1] in string.ascii_uppercase:
        class_ = "ttk::" + class_[1:].lower()
    else:
        class_ = class_.lower()
    return class_

def get_widget_options(widget):
    """
    Gets the options from a widget

    :param widget: tkinter.Widget instance to get the config options from
    :return: dict of options that you can pass on to widget.config()
    """
    return {
        key: value for key, value in zip(widget.keys(),
                                         [widget.cget(k) for k in widget.keys()]
                                         )}


def copy_widget(widget, new_parent, level=0):
    """
    Recursive function that copies a widget to a new parent.

    Ported to python from this tcl code :
    https://stackoverflow.com/questions/6285648/can-you-change-a-widgets-parent-in-python-tkinter

    :param widget: widget to copy (tkinter.Widget instance)
    :param new_parent: new widget to parent to.
    :param level: (default: 0) current level of the recursive algorithm

    :return: tkinter.Widget instance, the copied widget.
    """
    rv = widget.__class__(master=new_parent, **get_widget_options(widget))
    for b in widget.bind():
        script = widget.bind(b)
        # TODO: bind the script to the new widget (rv)
        # set type [ getWidgetType $w ]
        # set name [ string trimright $newparent.[lindex [split $w "." ] end ] "." ]
        # set retval [ $type $name {*}[ getConfigOptions $w ] ]
        # foreach b [ bind $w ] {
        #     puts "bind $retval $b [subst { [bind $w $b ] } ] "
        #     bind $retval $b  [subst { [bind $w $b ] } ]
        # }

    if level > 0:
        if widget.grid_info():  # if geometry manager is grid
            temp = widget.grid_info()
            del temp['in']
            rv.grid(**temp)
        elif widget.place_info():  # if geometry manager is place
            temp = widget.place_info()
            del temp['in']
            rv.place(**temp)
        else:  # if geometry manager is pack
            temp = widget.pack_info()
            del temp['in']
            rv.pack(**temp)
    level += 1
    if widget.pack_slaves():  # subwidgets are using the pack() geometry manager
        for child in widget.pack_slaves():
            copy_widget(child, rv, level)
    else:
        for child in widget.winfo_children():
            copy_widget(child, rv, level)
    return rv


def move_widget(widget, new_parent):
    """
    Moves widget to new_parent

    :param widget: widget to move
    :param new_parent: new parent for the widget

    :return: moved widget reference
    """
    rv = copy_widget(widget, new_parent)
    widget.destroy()
    return rv
