"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository

By importing this file at some point in a program, the
ttk.Widget parent classes get dynamically mixed in with a class that
adds the functionality of adding a tooltip (Tooltip) to any widget.

Tooltips are only added when a string to show in them is explicitly
given. Options for a Tooltip may be given as a dictionary of keyword
arguments upon widget initialization.

The default options for the Tooltip widget for the program may also be
changed by using the update_defaults function.
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets.hook import hook_ttk_widgets, generate_hook_name, is_hooked
from ttkwidgets.frames import Tooltip


OPTIONS = {"tooltip": None, "tooltip_options": {}}
NAME = generate_hook_name(OPTIONS)


def update_defaults(defaults):
    # type: (dict) -> None
    """
    Update the default options applied to the tooltip of a widget

    Updating the default options of the hook is no longer possible after
    the hook has been setup, but the :meth:`tooltip_updater` applies
    the default options first to all tooltips and only overwrites them
    if custom options have been given for the tooltip.
    """
    global OPTIONS
    OPTIONS["tooltip_options"] = defaults


def tooltip_options_hook(self, option, value):
    # type: (ttk.Widget, str, (str, dict)) -> None
    """
    Updater function for the 'tooltip' and 'tooltip_options' kwargs hook

    Given option ``tooltip``, configures the text of the tooltip of a
    widget.
    Given option ``tooltip_options``, updates the options the tooltip
    widget is configured with.

    :param self: ttk.Widget for which the hook is executed
    :param option: Option to be updated on the ttk.Widget
    :param value: The value of the given option. Will be a ``str`` for
        option ``tooltip`` and a dictionary for option
        ``tooltip_options``.
    """
    holder = getattr(self, NAME.lower())  # Instance of OriginalFunctions
    tooltip_widget = getattr(holder, "tooltip_widget", None)
    if option == "tooltip":
        tooltip_tooltip_updater(self, holder, tooltip_widget, value)
    elif option == "tooltip_options":
        tooltip_options_updater(self, holder, tooltip_widget, value)
    else:
        raise RuntimeError("Invalid option passed to tooltip_updater")


def tooltip_tooltip_updater(self, holder, tooltip_widget, tooltip):
    # type: ((tk.Widget, ttk.Widget), object, (Tooltip, None), (str, None)) -> None
    """Update the ``tooltip`` option of a widget by updating tooltip text"""
    if tooltip_widget is None and tooltip is not None:
        # Create a new tooltip
        options = OPTIONS["tooltip_options"].copy()
        options.update(getattr(holder, "tooltip_options", {}))
        options["text"] = tooltip
        tooltip_widget = Tooltip(self, **options)
    elif tooltip_widget is not None and tooltip is None:
        # Destroy existing tooltip
        tooltip_widget.destroy()
        tooltip_widget = None
    elif tooltip_widget is not None:
        # Update existing tooltip
        tooltip_widget.configure(text=tooltip)
    else:  # tooltip_widget is None and tooltip is None
        pass
    setattr(holder, "tooltip_widget", tooltip_widget)


def tooltip_options_updater(self, holder, tooltip_widget, options):
    """Update the options of a tooltip widget held on a widget"""
    # Update options for when a new tooltip is created
    new_options = getattr(holder, "tooltip_options", {})
    new_options.update(options)
    setattr(holder, "tooltip_options", new_options)
    if tooltip_widget is not None:
        # Tooltip already exists, configure it with new options
        tooltip_widget.configure(**new_options)


if not is_hooked(OPTIONS):
    hook_ttk_widgets(tooltip_options_hook, OPTIONS)
