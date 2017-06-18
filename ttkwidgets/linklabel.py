"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
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
    def __init__(self, master=None, link="", normal_color="#0563c1", hover_color="#057bc1", clicked_color="#954f72",
                 **kwargs):
        """
        :param master: master widget
        :param link: link to be opened
        :param normal_color: text color when widget is created
        :param hover_color: text color when hovering over the widget
        :param clicked_color: text color when link is clicked
        :param kwargs: options to be passed on to Label initializer
        """
        ttk.Label.__init__(self, master, foreground=normal_color, **kwargs)
        self._normal_color = normal_color
        self._hover_color = hover_color
        self._clicked_color = clicked_color
        self.__link = link
        self.__clicked = False
        self.bind("<Button-1>", self.open_link)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, *args):
        """
        Sets the text color to the hover color
        :return: None
        """
        self.config(foreground=self._hover_color)

    def _on_leave(self, *args):
        """
        Sets the text color to either the normal color when not clicked or the clicked color when clicked
        :return: None
        """
        if self.__clicked:
            self.config(foreground=self._clicked_color)
        else:
            self.config(foreground=self._normal_color)

    def reset(self):
        """
        Reset Label to unclicked status if previously clicked
        :return:
        """
        self.__clicked = False
        self._on_leave()

    def open_link(self, *args):
        """
        Open the link in the web browser
        :return: None
        """
        webbrowser.open(self.__link)
        self.__clicked = True
        self._on_leave()
