"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository

By importing this file at some point in a program, the
ttk.Widget parent classes get dynamically mixed in with class that
adds the functionality of adding a tooltip (Balloon) to any widget.

Tooltips are only added when a string to show in them is explicitly
given. Options for a Balloon may be given as a dictionary of keyword
arguments upon widget initialization.

The default options for the Balloon widget for the program may also be
changed by using the update_defaults function.

# TODO: Convert current implementation to a mixin
# TODO: Apply mixin to tkWidget also
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets.frames import Balloon


DEFAULTS = {}


def update_defaults(defaults):
    # type: (dict) -> None
    global DEFAULTS
    DEFAULTS.update(defaults)


class ToolTippableWidget(ttk.Widget):
    def __init__(self, *args):
        master, widget_type, kwargs = args
        self._tooltip = kwargs.pop("tooltip", None)
        self._tooltip_options = DEFAULTS.copy()
        self._tooltip_options.update(kwargs.pop("tooltip_options", {}))
        ttk.Widget._init__original(self, master, widget_type, kwargs)
        self.__widget = None
        self._update_tooltip()

    def configure(self, *args, **kwargs):
        self._tooltip = kwargs.pop("tooltip", None)
        self._tooltip_options.update(kwargs.pop("tooltip_options", {}))
        self._update_tooltip()
        return ttk.Widget._configure_original(self, *args, **kwargs)

    def cget(self, key):
        if key == "tooltip":
            return self._tooltip
        elif key == "tooltip_options":
            return self._tooltip_options
        return ttk.Widget._cget_original(self, key)

    def config(self, *args, **kwargs):
        return self.configure(*args, **kwargs)

    def _update_tooltip(self):
        self._tooltip_options["text"] = self._tooltip
        if self._tooltip is None and self.__widget is not None:
            self.__widget.destroy()
        elif self._tooltip is not None and self.__widget is not None:
            self.__widget.configure(**self._tooltip_options)
        elif not isinstance(self, Balloon):  # Balloons may not have Balloons -> recursion
            self.__widget = Balloon(self, **self._tooltip_options)


if ttk.Widget.__init__ is not ToolTippableWidget.__init__:

    # Save the original functions
    ttk.Widget._init__original = ttk.Widget.__init__
    ttk.Widget._configure_original = ttk.Widget.configure
    ttk.Widget._config_original = ttk.Widget.config
    ttk.Widget._cget_original = ttk.Widget.cget

    # Apply the modified functions
    ttk.Widget.__init__ = ToolTippableWidget.__init__
    ttk.Widget.configure = ToolTippableWidget.configure
    ttk.Widget.config = ToolTippableWidget.config
    ttk.Widget.cget = ToolTippableWidget.cget
    ttk.Widget._update_tooltip = ToolTippableWidget._update_tooltip
