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
from ttkwidgets.hook import hook_ttk_widgets, generate_hook_name, is_hooked
from ttkwidgets.frames import Balloon


OPTIONS = {"tooltip": None, "tooltip_options": {}}
NAME = generate_hook_name(OPTIONS)


def update_defaults(defaults):
    # type: (dict) -> None
    global OPTIONS
    OPTIONS["tooltip_options"] = defaults


def tooltip_updater(self, option, value):
    # type: (tk.Widget, str, (str, dict)) -> None
    """Update the tooltip held on a widget"""
    holder = getattr(self, NAME.lower())
    tooltip_widget = getattr(holder, "tooltip_widget", None)
    if option == "tooltip":
        tooltip_tooltip_updater(self, holder, tooltip_widget, value)
    elif option == "tooltip_options":
        tooltip_options_updater(self, holder, tooltip_widget, value)
    else:
        raise RuntimeError("Invalid option passed to tooltip_updater")


def tooltip_tooltip_updater(self, holder, tooltip_widget, tooltip):
    # type: ((tk.Widget, ttk.Widget), object, (Balloon, None), (str, None)) -> None
    """Update the 'tooltip' option of a widget by updating tooltip text"""
    if tooltip_widget is None and tooltip is not None:
        # Create a new tooltip
        options = OPTIONS["tooltip_options"].copy()
        options["text"] = tooltip
        options.update(getattr(holder, "tooltip_options", {}))
        tooltip_widget = Balloon(self, **options)
    elif tooltip_widget is not None and tooltip is None:
        # Destroy existing tooltip
        tooltip_widget.destroy()
        tooltip_widget = None
    else:
        # Update existing tooltip
        tooltip_widget.configure(text=tooltip)
    setattr(holder, "tooltip_widget", tooltip_widget)


def tooltip_options_updater(self, holder, tooltip_widget, options):
    """Update the options of a tooltip widget held on a widget"""
    pass


if not is_hooked(OPTIONS):
    hook_ttk_widgets(tooltip_updater, OPTIONS)

