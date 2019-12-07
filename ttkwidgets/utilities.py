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


def parse_geometry_string(string):
    """Parse a Tkinter geometry string ('XxY+W+H') into a box tuple"""
    e = string.split("x")
    w = int(e[0])
    e = e[1].split("+")
    h, x, y = map(int, e)
    return x, y, w, h


def get_widget_options(widget):
    """
    Gets the options from a widget

    :param widget: tkinter.Widget instance to get the config options from
    :return: dict of options that you can pass on to widget.config()
    """
    return {key: widget.cget(key) for key in widget.keys()}


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
        rv.bind(b, script)  # Not sure it will work tho
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


def parse_geometry(geometry):
    """
    Parses a tkinter geometry string into a 4-tuple (x, y, width, height)

    :param geometry: a tkinter geometry string in the format (wxh+x+y)
    :type geometry: str
    :returns: 4-tuple (x, y, width, height)
    :rtype: tuple
    """
    match = re.search(r'(\d+)x(\d+)(\+|-)(\d+)(\+|-)(\d+)', geometry)
    xmod = -1 if match.group(3) == '-' else 1
    ymod = -1 if match.group(5) == '-' else 1
    return ( xmod * int(match.group(4)), ymod * int(match.group(6)),
             int(match.group(1)), int(match.group(2)))


def coords_in_box(coords, bbox, include_edges=True):
    """
    Checks whether coords are inside bbox

    :param coords: 2-tuple of coordinates x, y
    :type coords: tuple
    :param bbox: 4-tuple (x, y, width, height) of a bounding box
    :type bbox: tuple
    :param include_edges: default True whether to include the edges
    :type include_edges: bool
    :returns: whether coords is inside bbox
    :rtype: bool
    :raises: ValueError if length of bbox or coords do not match the specifications
    """
    if len(coords) != 2:
        raise ValueError("Coords argument is supposed to be of length 2")
    if len(bbox) != 4:
        raise ValueError("Bbox argument is supposed to be of length 4")

    x, y = coords
    xmin, ymin, width, height = bbox
    xmax, ymax = xmin + width, ymin + height
    if include_edges:
        xmin = max(xmin - 1, 0)
        xmax += 1
        ymin = max(ymin - 1, 0)
        ymax += 1
    return xmin < x < xmax and ymin < y < ymax
