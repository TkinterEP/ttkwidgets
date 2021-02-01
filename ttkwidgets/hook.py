"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository

This file provides a set of functions that can be used for adding
options to all classes that inherit from ``ttk.Widget``, so `ttk.Button``,
for example, but also every widget contained in this package.

When an option is changed, an updater function is called that the
developer creating the hook has to provide. This updater is called
after the widget has initialized if the option is set upon
initialization of the widget.

Default values may be specified as well. For more details, see
:meth:`hook_ttk_widgets` for more details. See :meth:`tooltip_updater`
for a practical implementation of a hook.
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


def is_hooked(options):
    # type: (dict) -> bool
    """Return whether ``ttk.Widget`` is hooked for any of the given options"""
    for hookname in [hook for hook in dir(ttk.Widget) if hook.startswith("WidgetHook_")]:
        hookoptions = getattr(ttk.Widget, hookname).defaults
        if any(option in hookoptions for option in options):
            return True
    return hasattr(ttk.Widget, generate_hook_name(options))


def generate_hook_name(options):
    # type: (dict) -> str
    """Generate a unique name for a hook given a set of options"""
    return "WidgetHook_" + "_".join(sorted(options))


def hook_ttk_widgets(updater, options):
    # type: (callable, dict) -> str
    """
    Create a hook in either tk.Widget or ttk.Widget to support options

    This function works by overriding the ``__init__``, ``configure``,
    ``config``, ``cget`` and ``keys`` functions of the ``ttk.Widget``
    class. The original functions are stored safely inside a class
    object created upon the ``ttk.Widget`` class, so that they can
    still be executed when necessary.

    Multiple hooks are allowed at the same time and a custom hook
    overwriting any of the functions (as long as it is done properly)
    does not cause any issues.

    The order in which hooks are executed is not guaranteed as a stable
    library feature.

    :param updater: Function to call when an option in the given options
        is changed. The function should support updating for all the
        options given in the hook.
    :type updater: (widget: ttk.Widget, option: str, value: Any) -> None
    :param options: A dictionary of options where the keys are the
        keyword argument names and the values are their respective
        default values. A default value must be specified for every
        option. All option names must be allowed in valid Python syntax.
    :type options: Dict[str, Any]
    :return: Name of the attribute created to store values
    :rtype: str
    """
    NULL = object()

    assert len(options) > 0

    # Create a unique name so that multiple hooks do not interfere
    name = generate_hook_name(options)
    # Check to see if the hook already exists
    if hasattr(ttk.Widget, name):  # Hook already exists, will be updated
        if updater is not None:
            raise RuntimeError("Invalid parameter: Updater may not be changed after hook creation")
        getattr(ttk.Widget, name).defaults = options.copy()
        return name
    elif is_hooked(options):
        raise RuntimeError("Invalid options: Cannot replace full hook with partial hook")

    # Create a class with the original functions
    class OriginalFunctions(object):
        original_init = ttk.Widget.__init__
        original_config = ttk.Widget.config
        original_configure = ttk.Widget.configure
        original_cget = ttk.Widget.cget
        original_keys = ttk.Widget.keys
        defaults = options

    # Move the OriginalFunctions class to the target class
    setattr(ttk.Widget, name, OriginalFunctions)

    def setter(self, option, value):
        """Store an option on the embedded object and then call updater"""
        current = getter(self, option)
        if current != value:
            setattr(getattr(self, name.lower()), option, value)
            updater(self, option, value)

    def getter(self, option):
        """Retrieve an option value from the embedded object"""
        return getattr(getattr(self, name.lower()), option, NULL)

    def __init__(self, *args):
        """Catch initialization and pop all the custom options"""
        master, widget, widget_options = args
        # Pop all the options, taking default values first
        values = getattr(self, name).defaults.copy()
        for (option, default) in options.items():
            value = widget_options.pop(option, default)
            values[option] = value
        # Perform initialization of the widget
        getattr(self, name).original_init(self, master, widget, widget_options)
        # Create an instance object to store options on
        setattr(self, name.lower(), OriginalFunctions())
        # Set all the options only after widget init is complete
        for option, value in values.items():  # updater only called after init is done
            setter(self, option, value)

    def configure(self, *args, **kwargs):
        """Catch configure to pop custom options and configure them"""
        for widget_options in args + (kwargs,):  # Loop over all sets of options available
            if widget_options is None:
                continue
            for option, _ in options.items():
                current = getter(self, option)
                value = widget_options.pop(option, current)
                setter(self, option, value)
        return getattr(self, name).original_configure(self, *args, **kwargs)

    def cget(self, key):
        """Return the value of a custom option if key is a custom option"""
        if key in options:
            return getter(self, key)
        return getattr(self, name).original_cget(self, key)

    def keys(self):
        """Return an updated list of keys with the custom options"""
        keys = getattr(self, name).original_keys(self)
        keys.extend(options.keys())
        return keys

    ttk.Widget.__init__ = __init__
    ttk.Widget.configure = configure
    ttk.Widget.config = configure
    ttk.Widget.cget = cget
    ttk.Widget.__getitem__ = cget
    ttk.Widget.keys = keys

    return name
