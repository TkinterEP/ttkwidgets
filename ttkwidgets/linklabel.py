"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbrol/tkinter-kit)
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
import webbrowser


class LinkLabel(ttk.Label):
    """
    A ttk Label that can be clicked to open a link with a default blue color, a purple color when clicked and a bright
    blue color when hovering over the Label
    """
    def __init__(self, master=None, **kwargs):
        """
        :param master: master widget
        :param link: link to be opened
        :param normal_color: text color when widget is created
        :param hover_color: text color when hovering over the widget
        :param clicked_color: text color when link is clicked
        :param kwargs: options to be passed on to Label initializer
        """
        self._cursor = kwargs.pop("cursor", "hand1")
        self._link = kwargs.pop("link", "")
        self._normal_color = kwargs.pop("normal_color", "#0563c1")
        self._hover_color = kwargs.pop("hover_color", "#057bc1")
        self._clicked_color = kwargs.pop("clicked_color", "#954f72")
        ttk.Label.__init__(self, master, **kwargs)
        self.config(foreground=self._normal_color)
        self.__clicked = False
        self.bind("<Button-1>", self.open_link)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _on_enter(self, *args):
        """
        Sets the text color to the hover color
        :return: None
        """
        self.config(foreground=self._hover_color, cursor=self._cursor)

    def _on_leave(self, *args):
        """
        Sets the text color to either the normal color when not clicked or the clicked color when clicked
        :return: None
        """
        if self.__clicked:
            self.config(foreground=self._clicked_color)
        else:
            self.config(foreground=self._normal_color)
        self.config(cursor="")

    def reset(self):
        """
        Reset Label to unclicked status if previously clicked
        :return: None
        """
        self.__clicked = False
        self._on_leave()

    def open_link(self, *args):
        """
        Open the link in the web browser
        :return: None
        """
        if "disabled" not in self.state():
            webbrowser.open(self._link)
            self.__clicked = True
            self._on_leave()

    def cget(self, key):
        """ Return the resource value for a KEY given as string. """
        if key is "link":
            return self._link
        elif key is "hover_color":
            return self._hover_color
        elif key is "normal_color":
            return self._normal_color
        elif key is "clicked_color":
            return self._clicked_color
        else:
            return ttk.Label.cget(self, key)

    def configure(self, **kwargs):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        self._link = kwargs.pop("link", self._link)
        self._hover_color = kwargs.pop("hover_color", self._hover_color)
        self._normal_color = kwargs.pop("normal_color", self._normal_color)
        self._clicked_color = kwargs.pop("clicked_color", self._clicked_color)
        ttk.Label.configure(self, **kwargs)
        self._on_leave()

    def keys(self):
        """ Return a list of all resource names of this widget. """
        keys = ttk.Label.keys(self)
        keys.extend(["link", "normal_color", "hover_color", "clicked_color"])
        return keys


if __name__ == '__main__':
    window = tk.Tk()
    LinkLabel(window, text="Label").pack()
    window.mainloop()
