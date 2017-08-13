"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

# TODO: Implement the automatic snap-in-place when Toplevel is brought close to the window again
# TODO: Allow the user to move the Toplevel to a different location on the window
# TODO: Allow the developer to lock the SnapToplevel in place


class SnapToplevel(tk.Toplevel):
    """
    A Toplevel window that can be snapped to a side of the Tk instance

    At first glance, the code doesn't allow multiple of these to be opened at the same time (see the second ValueError),
    but it can be worked around if it is actually the intention of the programmer to have multiple of these. This can be
    done by unbinding <Configure> from the master instance before opening, and after that rebinding to a function that
    calls the configure_callback functions of all SnapToplevel instances, and then calling the original <Configure>
    callback of the master window, if present.

    Is not guaranteed to work on all platforms due to Tkinter event and window manager restrictions. Functionality
    depends on whether a <Configure> event is generated upon moving the Tk instance.
    """
    def __init__(self, master, **kwargs):
        """
        :param master: master Tk instance
        :param kwargs: configure_function - callable object which has to be called upon a <Configure> event of either
                                            the master Tk instance or this SnapToplevel instance
                       location           - either tk.LEFT, tk.RIGHT, tk.TOP or tk.BOTTOM - Location of the SnapToplevel
                                            relative to the master Tk instance, defaults to tk.RIGHT
                       offset             - A custom offset in pixels for the window. The platform the user is using
                                            may call for different values. For the tk.TOP location, the top_offset value
                                            is used.
                       top_offset         - The offset for the tk.TOP position
                       locked             - Whether the user is allowed to move the Toplevel at all
                       All other keyword arguments, such as width and height, are passed to the Toplevel
        """
        if not isinstance(master, tk.Tk):
            raise ValueError("SnapWindows can only be created with a Tk instance as master.")
        self._configure_function = kwargs.pop("configure_function", None)
        self._location = kwargs.pop("location", tk.RIGHT)
        # TODO: Gather different offset values for different platforms
        """
        Windows 7: 15, 37 pixels (no DPI scaling)
        """
        self._offset = kwargs.pop("offset", 15)
        self._top_offset = kwargs.pop("top_offset", 37)
        if not isinstance(self._offset, int):
            raise ValueError("offset option must be of int type. Given value is of {0} type.".
                             format(type(self._offset)))
        # Tk.bind(self, event_name) returns an empty string if no function was bound to the event
        # It returns something like below if one was bound:
        # {"[55632584<lambda> %# %b %f %h %k %s %t %w %x %y %A %E %K %N %W %T %X %Y %D]" == "break"} break\n
        # This is probably because the implementation is not correct in the C bindings of Tkinter
        if not self._configure_function and not master.bind("<Configure>") == "":
            raise ValueError("No original Configure binding provided while one was bound to the master Tk instance.")
        tk.Toplevel.__init__(self, master, **kwargs)
        self.bind("<Configure>", self.configure_callback)
        self.master.bind("<Configure>", self.configure_callback)
        self.master.bind("<Unmap>", self.minimize)
        self.master.bind("<Map>")

        # Call the configure function to set up initial location
        # First create a fake Tkinter event
        class Event(object):
            widget = self.master
        self.configure_callback(Event())
        # Lift self to front
        self.deiconify()

    def minimize(self, event):
        """
        Callback for an <Unmap> event on the master widget
        """
        self.wm_iconify()

    def deminimize(self, event):
        """
        Callback for a <Map> event on the master widget
        """
        self.deiconify()

    def configure_callback(self, event):
        """
        The callback for the <Configure> Tkinter event, generated when a window is moved or resized.
        """
        if event.widget is self.master:
            new_width, new_height, new_x, new_y = self.calculate_geometry_master()
        elif event.widget is self:
            return
        else:
            return
        self.wm_geometry("{}x{}+{}+{}".format(new_width, new_height, new_x, new_y))
        self.lift()
        if callable(self._configure_function):
            self._configure_function(event)

    def calculate_geometry_master(self):
        """
        Function to calculate the new geometry of the window
        """
        if not isinstance(self.master, tk.Tk):
            raise ValueError()
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        required_width, required_height = self.winfo_reqwidth(), self.winfo_reqheight()
        master_width, master_height = self.master.winfo_width(), self.master.winfo_height()
        if self._location == tk.RIGHT:
            new_x = master_x + master_width + self._offset
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._location == tk.LEFT:
            new_x = master_x - required_width - self._offset
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._location == tk.TOP:
            new_x = master_x
            new_y = master_y - required_height - self._top_offset
            new_width = master_width
            new_height = required_height
        elif self._location == tk.BOTTOM:
            new_x = master_x
            new_y = master_y + required_height + self._offset
            new_width = master_width
            new_height = required_height
        else:
            raise ValueError("Location is not a valid value: {0}. Was the private attribute altered?".
                             format(self._location))
        return new_width, new_height, new_x, new_y


if __name__ == '__main__':
    window = tk.Tk()
    snap = SnapToplevel(window, location=tk.TOP)
    window.mainloop()



