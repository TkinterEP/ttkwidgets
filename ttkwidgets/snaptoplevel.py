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
from math import sqrt, pow


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
                       anchor             - either tk.LEFT, tk.RIGHT, tk.TOP or tk.BOTTOM - Location of the SnapToplevel
                                            relative to the master Tk instance, defaults to tk.RIGHT
                       locked             - Whether the user is allowed to move the Toplevel at all
                       offset_sides       - Override default value
                       offset_top         - Override default value
                       allow_change       - Allow the changing of the Toplevel anchor by moving the window
                       resizable          - Argument to self.resizable()

                       All other keyword arguments, such as width and height, are passed to the Toplevel
        """
        # Process given arguments
        if not isinstance(master, tk.Tk):
            raise ValueError("SnapWindows can only be created with a Tk instance as master.")
        self._configure_function = kwargs.pop("configure_function", None)
        self._anchor = kwargs.pop("anchor", tk.RIGHT)
        self._locked = kwargs.pop("locked", False)
        self._border = kwargs.pop("border", 40)
        self._offset_sides = kwargs.pop("offset_sides", None)
        self._offset_top = kwargs.pop("offset_top", None)
        self._resizable = kwargs.pop("resizable", False)
        self._allow_change = kwargs.pop("allow_change", False)

        # Tk.bind(self, event_name) returns an empty string if no function was bound to the event
        # It returns something like below if one was bound:
        # {"[55632584<lambda> %# %b %f %h %k %s %t %w %x %y %A %E %K %N %W %T %X %Y %D]" == "break"} break\n
        # This is probably because the implementation is not correct in the C bindings of Tkinter
        if not self._configure_function and not master.bind("<Configure>") == "":
            raise ValueError("No original Configure binding provided while one was bound to the master Tk instance.")

        # Initialize Toplevel
        tk.Toplevel.__init__(self, master, **kwargs)

        # Set the offset values
        offset_sides, offset_top = self.get_offset_values()
        self._offset_sides = self._offset_sides if self._offset_sides is not None else offset_sides
        self._offset_top = self._offset_top if self._offset_top is not None else offset_top

        # Check if the keyword arguments are all valid values
        self.check_keyword_arguments()

        # Bind to <Configure>, <Map> and <Unmap> events
        self.bind("<Configure>", self.configure_callback)
        self.master.bind("<Configure>", self.configure_callback)
        self.master.bind("<Unmap>", self.minimize)
        self.master.bind("<Map>", self.deminimize)

        # Get the current geometry of windows
        self._snapped = True
        self._temp_lock = False
        self.update()
        self.master.update()
        self._geometry = self.wm_geometry()
        self._master_geometry = self.wm_geometry()
        self._distance = 0

        # Call the configure function to set up initial anchor
        # First create a fake Tkinter event
        class Event(object):
            widget = self.master

        self.configure_callback(Event())

        # Lift self to front, but focus master
        self.deminimize(None)

        # Set resizability
        self.wm_resizable(self._resizable, self._resizable)

    def check_keyword_arguments(self):
        """
        Check if all the attribute values set through arguments are valid
        :raises: ValueError if an invalid value is found
        """
        if (self._anchor != tk.LEFT and self._anchor != tk.RIGHT and self._anchor != tk.TOP and
                    self._anchor != tk.BOTTOM):
            raise ValueError("anchor can only be set to tk.LEFT, tk.RIGHT, tk.TOP, tk.BOTTOM and not {}".
                             format(self._anchor))
        if not isinstance(self._locked, bool):
            raise ValueError("locked can only be set to a bool value, not {}".format(self._locked))
        if not isinstance(self._border, int):
            raise ValueError("border can only be set to an int value, not {}".format(self._border))
        if not isinstance(self._offset_sides, int):
            raise ValueError("offset_sides can only be set to an int value, not {}".format(self._offset_sides))
        if not isinstance(self._offset_top, int):
            raise ValueError("offset_top can only be set to an int value, not {}".format(self._offset_top))
        if not isinstance(self._resizable, bool):
            raise ValueError("resizable can only be set to a bool value, not {}".format(self._resizable))
        if not isinstance(self._allow_change, bool):
            raise ValueError("allow_change can only be set to a bool value, not {}".format(self._allow_change))
        return

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
        self.master.focus_set()

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
        """
        Function to unlock the temporary lock on movement
        """
        self._temp_lock = False

    def set_geometry_self(self):
        """
        Set geometry when <Configure> is created with self as widget
        """
        distance_dictionary = self.get_distance_to_master()
        # If the widget is locked, we want to reset the geometry to match the master widget
        if self._locked or self._temp_lock:
            self.set_geometry_master()
            return

        elif self._snapped:
            self._geometry = self.wm_geometry()
            # If the minimum distance is larger than the border distance, the window is not snapped
            if distance_dictionary[self._anchor] > self._border:
                self._snapped = False
                return

        elif not self._allow_change:
            # Changing of the anchor point is not allowed
            if distance_dictionary[self._anchor] < self._border and not self._snapped:
                self._snap()
            else:
                return
        else:
            # Changing of the anchor point is allowed
            distance = min(distance_dictionary.values())
            # Check if the anchor point as to be changed
            if distance <= distance_dictionary[self._anchor] and distance < self._border + self._offset_sides:

                for anchor, anchor_distance in distance_dictionary.items():
                    if distance == anchor_distance:
                        self._anchor = anchor
                        self._snap()
                        return
            elif distance_dictionary[self._anchor] < self._border:
                self._snap()
        return

    def _snap(self):
        """
        Function to set everything so the window can be snapped into place again
        """
        self._snapped = True
        self._temp_lock = True
        self.after(500, self._unlock)
        self.set_geometry_master()

    def get_distance_to_master(self):
        """
        Return an int value of distance in pixels to the master window for each of the four sides
        """
        # Get the required values
        master_left, master_right, master_top, master_bottom = self.get_points_sides_for_window(self.master)
        self_left, self_right, self_top, self_bottom = self.get_points_sides_for_window(self)

        # Calculate the distances
        distance_left = self.get_distance_between_points(master_left, self_right)
        distance_right = self.get_distance_between_points(master_right, self_left)
        distance_top = self.get_distance_between_points(master_top, self_bottom)
        distance_bottom = self.get_distance_between_points(master_bottom, self_top)

        return {
            tk.LEFT: distance_left,
            tk.RIGHT: distance_right,
            tk.TOP: distance_top,
            tk.BOTTOM: distance_bottom
        }

    @staticmethod
    def get_distance_between_points(point_one, point_two):
        """
        Calculate the distance in pixels between two points
        :param point_one: (x, y)
        :param point_two: (x, y)
        :return: distance (int)
        """
        dx = abs(point_one[0] - point_two[0])
        dy = abs(point_one[1] - point_two[1])
        return int(sqrt(pow(dx, 2) + pow(dy, 2)))

    @staticmethod
    def get_points_sides_for_window(window):
        """
        Get the coordinates of the middle of each of the sides of a tkinter window (Toplevel or Tk)
        """
        master_width, master_height = window.winfo_width(), window.winfo_height()
        master_rootx, master_rooty = window.winfo_rootx(), window.winfo_rooty()
        master_left = (master_rootx, master_rooty + master_height // 2)
        master_right = (master_rootx + master_width, master_rooty + master_height // 2)
        master_bottom = (master_rootx + master_width // 2, master_rooty + master_height)
        master_top = (master_rootx + master_width // 2, master_rooty)
        return master_left, master_right, master_top, master_bottom

    def set_geometry_master(self):
        """
        Function to set the new geometry of the window if it is snapped to the master and the master was moved
        """
        # If the Toplevel is not snapped to the window, we want to do nothing
        if not self.snapped:
            return
        new_x, new_y, new_width, new_height = self.get_new_geometry_master()
        if self._resizable:
            new_width, new_height = self.winfo_width(), self.winfo_height()
        self.wm_geometry("{}x{}+{}+{}".format(new_width, new_height, new_x, new_y))

    def get_new_geometry_master(self):
        """
        Function to calculate the new geometry of the window
        """
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        required_width, required_height = self.winfo_reqwidth(), self.winfo_reqheight()
        master_width, master_height = self.master.winfo_width(), self.master.winfo_height()
        if self._anchor == tk.RIGHT:
            new_x = master_x + master_width + self._offset_sides * 2
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._anchor == tk.LEFT:
            new_x = master_x - required_width - self._offset_sides * 2
            new_y = master_y
            new_width = required_width
            new_height = master_height
        elif self._anchor == tk.TOP:
            new_x = master_x
            new_y = master_y - required_height - self._offset_top - self._offset_sides
            new_width = master_width
            new_height = required_height
        elif self._anchor == tk.BOTTOM:
            new_x = master_x
            new_y = master_y + required_height + self._offset_top + self._offset_sides
            new_width = master_width
            new_height = required_height
        else:
            raise ValueError("Location is not a valid value: {0}. Was the private attribute altered?".
                             format(self._anchor))
        return new_x, new_y, new_width, new_height

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

    def cget(self, key):
        if key == "configure_function":
            return self._configure_function
        elif key == "anchor":
            return self._anchor
        elif key == "locked":
            return self._locked
        elif key == "border":
            return self._border
        elif key == "offset_sides":
            return self._offset_sides
        elif key == "offset_top":
            return self._offset_top
        elif key == "resizable":
            return self._resizable
        elif key == "allow_change":
            return self._allow_change
        else:
            return tk.Toplevel.cget(self, key)

    def config(self, **kwargs):
        self._configure_function = kwargs.pop("configure_function", self._configure_function)
        self._anchor = kwargs.pop("anchor", self._anchor)
        self._locked = kwargs.pop("locked", self._locked)
        self._border = kwargs.pop("border", self._border)
        self._offset_sides = kwargs.pop("offset_sides", self._offset_sides)
        self._offset_top = kwargs.pop("offset_top", self._offset_top)
        self._resizable = kwargs.pop("resizable", self._resizable)
        self._allow_change = kwargs.pop("allow_change", self._allow_change)
        self.check_keyword_arguments()
        return tk.Toplevel.config(self, **kwargs)

    def configure(self, **kwargs):
        self.config(**kwargs)

    @property
    def snapped(self):
        return self._snapped

if __name__ == '__main__':
    window = tk.Tk()
    snap = SnapToplevel(window, allow_change=True)
    window.mainloop()
