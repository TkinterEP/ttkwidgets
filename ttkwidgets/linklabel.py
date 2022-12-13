"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende: change default widget colors, use native cursors by default, add virtual event
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbrol/tkinter-kit)
# Available from fork: https://www.github.com/RedFantom/tkinter-kit
import tkinter as tk
import webbrowser
from tkinter import ttk


class LinkLabel(ttk.Label):
    """
    A :class:`ttk.Label` that can be clicked to open a link with a default blue color,
    a purple when clicked and dark blue when hovering over the Label.
    """

    def __init__(self, master=None, **kwargs):
        """
        Create a LinkLabel.

        :param master: master widget
        :param link: link to be opened
        :type link: str
        :param normal_color: text color when the widget is in neutral state
        :type normal_color: str
        :param hover_color: text color when hovering over the widget
        :type hover_color: str
        :param clicked_color: text color when the widget has been clicked
        :type clicked_color: str
        :param kwargs: options to be passed on to the :class:`ttk.Label` initializer
        """
        self._link = kwargs.pop("link", "")
        self._normal_color = kwargs.pop("normal_color", "#005fff")
        self._hover_color = kwargs.pop("hover_color", "#000fff")
        self._clicked_color = kwargs.pop("clicked_color", "#6600a6")

        parent = master or tk._default_root
        is_mac = parent.tk.call("tk", "windowingsystem") == "aqua"
        kwargs.setdefault("cursor", "pointinghand" if is_mac else "hand2")

        ttk.Label.__init__(self, parent, **kwargs)

        if "disabled" not in self.state():
            self.configure(foreground=self._normal_color)

        self._clicked = False
        self.bind("<Button-1>", self.open_link)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _on_enter(self, *args):
        """Set the text color to the hover color."""
        if self._clicked:
            self.config(foreground=self._clicked_color)
        else:
            self.config(foreground=self._hover_color)

    def _on_leave(self, *args):
        """Set the text color to either the normal color when not clicked or the clicked color when clicked."""
        if self._clicked:
            self.config(foreground=self._clicked_color)
        else:
            self.config(foreground=self._normal_color)

    def reset(self):
        """Reset Label to unclicked status if previously clicked."""
        self._clicked = False
        self._on_leave()

    def open_link(self, *args):
        """Open the link in the web browser."""
        if "disabled" in self.state():
            return

        webbrowser.open(self._link)
        self._clicked = True
        self._on_leave()
        self.event_generate("<<LinkOpened>>")

    def configure(self, **kwargs):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method :meth:`~LinkLabel.keys`.
        See :meth:`~LinkLabel.__init__` for a description of the widget specific option.
        """
        self._link = kwargs.pop("link", self._link)
        self._normal_color = kwargs.pop("normal_color", self._normal_color)
        self._hover_color = kwargs.pop("hover_color", self._hover_color)
        self._clicked_color = kwargs.pop("clicked_color", self._clicked_color)
        ttk.Label.configure(self, **kwargs)

    config = configure

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method :meth:`~LinkLabel.keys`.
        """
        if key == "link":
            return self._link
        elif key == "hover_color":
            return self._hover_color
        elif key == "normal_color":
            return self._normal_color
        elif key == "clicked_color":
            return self._clicked_color
        else:
            return ttk.Label.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = ttk.Label.keys(self)
        keys.extend(["link", "normal_color", "hover_color", "clicked_color"])
        keys.sort()
        return keys
