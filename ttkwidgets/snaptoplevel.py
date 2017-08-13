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

# TODO: Allow the user to move the Toplevel to a different location on the window


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
                       locked             - Whether the user is allowed to move the Toplevel at all
                       offset_sides       - Override default value
                       offset_top         - Override default value
                       allow_change       - Allow the changing of the Toplevel anchor by moving the window

                       All other keyword arguments, such as width and height, are passed to the Toplevel
        """
        # Process arguments
        if not isinstance(master, tk.Tk):
            raise ValueError("SnapWindows can only be created with a Tk instance as master.")
        self._configure_function = kwargs.pop("configure_function", None)
        self._location = kwargs.pop("location", tk.RIGHT)
        self._locked = kwargs.pop("locked", False)
        self._border = kwargs.pop("border", 40)
        self._offset_sides = kwargs.pop("offset_sides", None)
        self._offset_top = kwargs.pop("offset_top", None)
        # Tk.bind(self, event_name) returns an empty string if no function was bound to the event
        # It returns something like below if one was bound:
        # {"[55632584<lambda> %# %b %f %h %k %s %t %w %x %y %A %E %K %N %W %T %X %Y %D]" == "break"} break\n
        # This is probably because the implementation is not correct in the C bindings of Tkinter
        if not self._configure_function and not master.bind("<Configure>") == "":
            raise ValueError("No original Configure binding provided while one was bound to the master Tk instance.")
        tk.Toplevel.__init__(self, master, **kwargs)
        offset_sides, offset_top = self.get_offset_values()
        self._offset_sides = self._offset_sides if self._offset_sides is not None else offset_sides
        self._offset_top = self._offset_top if self._offset_top is not None else offset_top
        self.bind("<Configure>", self.configure_callback)
        self.master.bind("<Configure>", self.configure_callback)
        self.master.bind("<Unmap>", self.minimize)
        self.master.bind("<Map>")
        self._snapped = True
        self.update()
        self.master.update()
        self._geometry = self.wm_geometry()
        self._master_geometry = self.wm_geometry()
        self._distance = 0

        # Call the configure function to set up initial location
        # First create a fake Tkinter event
        class Event(object):
            widget = self.master

        self.configure_callback(Event())

        # Lift self to front, but focus master
        self.deiconify()
        self.master.focus_set()

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
            self.set_geometry_master()
        elif event.widget is self:
            self.set_geometry_self()
        else:
            return
        if callable(self._configure_function):
            self._configure_function(event)

    def _unlock(self):
        self._locked = False

    def set_geometry_self(self):
        if self._locked:
            self.set_geometry_master()
        else:
            if self.wm_geometry() != self._geometry:
                if self._snapped:
                    self._geometry = self.wm_geometry()
                    distance = self.get_distance_to_master()
                    if distance > self._border:
                        self._snapped = False
                        pass
                else:
                    distance = self.get_distance_to_master()
                    if distance < self._border:
                        self._snapped = True
                        self._locked = True
                        self.after(500, self._unlock)
                        self.set_geometry_master()
            else:
                return

    def get_distance_to_master(self):
        return max((abs(self.winfo_rootx() - self.master.winfo_rootx()) - self.winfo_width(),
                    abs(self.winfo_rooty() - self.master.winfo_rooty()) - self.winfo_height()))

    def set_geometry_master(self):
        """
        Function to calculate the new geometry of the window if it is snapped to the master and the master was moved
        """
        # If the Toplevel is not snapped to the window, we want to do nothing
        if not self.snapped:
            return
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        required_width, required_height = self.winfo_reqwidth(), self.winfo_reqheight()
        master_width, master_height = self.master.winfo_width(), self.master.winfo_height()
        if self._location == tk.RIGHT:
            new_x = master_x + master_width + self._offset_sides * 2
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._location == tk.LEFT:
            new_x = master_x - required_width - self._offset_sides * 2
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._location == tk.TOP:
            new_x = master_x
            new_y = master_y - required_height - self._offset_top - self._offset_sides
            new_width = master_width
            new_height = required_height
        elif self._location == tk.BOTTOM:
            new_x = master_x
            new_y = master_y + required_height + self._offset_sides * 2
            new_width = master_width
            new_height = required_height
        else:
            raise ValueError("Location is not a valid value: {0}. Was the private attribute altered?".
                             format(self._location))
        self.wm_geometry("{}x{}+{}+{}".format(new_width, new_height, new_x, new_y))

    def get_offset_values(self):
        """
        Function to get the window offset values
        :return: offset_sides, offset_top (int, int)
        """
        self.master.update()
        root_x, root_y = self.master.winfo_rootx(), self.master.winfo_rooty()
        content_x, content_y = self.master.winfo_x(), self.master.winfo_y()
        offset_sides = abs(content_x - root_x)
        offset_top = abs(content_y - root_y)
        return offset_sides, offset_top

    def cget(self, *args):
        pass

    def config(self, **kwargs):
        pass

    def configure(self, **kwargs):
        self.config(**kwargs)

    @property
    def snapped(self):
        return self._snapped

if __name__ == '__main__':
    window = tk.Tk()
    snap = SnapToplevel(window, location=tk.LEFT)
    window.mainloop()
