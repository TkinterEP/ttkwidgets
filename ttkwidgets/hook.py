"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


def is_hooked(options):
    # type: (dict) -> bool
    """Return whether a class is hooked for the given options"""
    return hasattr(ttk.Widget, generate_hook_name(options))


def generate_hook_name(options):
    # type: (dict) -> str
    return "WidgetHook_" + "_".join(sorted(options))


def hook_ttk_widgets(updater, options):
    # type: (callable, dict) -> str
    """
    Create a hook in either tk.Widget or ttk.Widget to support options

    :param updater: Function to update the option
    :type updater: (widget: t(t)k.Widget, option: str, value: Any) -> None
    :param options: A list of string options supported by the functions
    :type options: Dict[str, Any]
    :return: Name of the attribute created to store values
    :rtype: str
    """

    assert len(options) > 0

    # Create a unique name so that multiple hooks do not interfere
    name = generate_hook_name(options)
    # Check to see if the hook already exists
    if hasattr(ttk.Widget, name):
        return name  # Hook already installed

    # Create a class with the original functions
    class OriginalFunctions(object):
        original_init = ttk.Widget.__init__
        original_config = ttk.Widget.config
        original_configure = ttk.Widget.configure
        original_cget = ttk.Widget.cget

    # Move the OriginalFunctions class to the target class
    setattr(ttk.Widget, name, OriginalFunctions)

    def setter(self, option, value):
        """Store an option on the embedded object and then call updater"""
        setattr(getattr(self, name.lower()), option, value)
        updater(self, option, value)

    def getter(self, option):
        """Retrieve an option value from the embedded object"""
        return getattr(getattr(self, name.lower()), option, options[option])

    def __init__(self, *args):
        master, widget, widget_options = args
        values = options.copy()
        for (option, default) in options.items():
            value = widget_options.pop(option, default)
            values[option] = value
        getattr(self, name).original_init(self, master, widget, widget_options)
        setattr(self, name.lower(), OriginalFunctions())
        for option, value in values.items():  # updater only called after init is done
            setter(self, option, value)

    def configure(self, *args, **kwargs):
        for widget_options in args + (kwargs,):  # Loop over all sets of options available
            for option, _ in options.items():
                current = getter(self, option)
                value = widget_options.pop(option, current)
                setter(self, option, value)
        return getattr(self, name).original_configure(self, *args, **kwargs)

    def cget(self, key):
        if key in options:
            return getter(self, key)
        return getattr(self, name).original_cget(self, key)

    ttk.Widget.__init__ = __init__
    ttk.Widget.configure = configure
    ttk.Widget.config = configure
    ttk.Widget.cget = cget

    return name


if __name__ == '__main__':
    hook_ttk_widgets(lambda s, o, v: print(s, o, v), {"tooltip": "Default Value"})
    hook_ttk_widgets(lambda s, o, v: print(s, o, v), {"hello_world": "second_hook"})

    original_init = ttk.Button.__init__

    def __init__(self, *args, **kwargs):
        print("User custom hook")
        original_init(self, *args, **kwargs)

    ttk.Button.__init__ = __init__

    window = tk.Tk()
    button = ttk.Button(window, text="Destroy", command=window.destroy, tooltip="Destroys Window")
    button.pack()
    print([name for name in dir(button) if name.startswith("WidgetHook")])
    window.after(1000, lambda: button.configure(tooltip="Does not destroy window", command=lambda: None))
    window.mainloop()
