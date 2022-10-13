# -*- coding: utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: https://github.com/j4321/tkColorPicker

Edited by RedFantom for Python 2/3 cross-compatibility and docstring formatting

tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Nicer Spinbox than the tk.Spinbox
"""


from .functions import tk, ttk


class Spinbox(tk.Spinbox):
    """Spinbox closer to ttk look (designed to be used with clam)."""

    def __init__(self, parent, **kwargs):
        """
        Create a Spinbox.

        The keyword arguments are the same as for a tk.Spinbox.
        """
        self.style = ttk.Style(parent)
        self.frame = ttk.Frame(parent, class_="ttkSpinbox",
                               relief=kwargs.get("relief", "sunken"),
                               borderwidth=1)
        self.style.configure("%s.spinbox.TFrame" % self.frame,
                             background=self.style.lookup("TSpinbox",
                                                          "fieldbackground",
                                                          default='white'))
        self.frame.configure(style="%s.spinbox.TFrame" % self.frame)
        kwargs["relief"] = "flat"
        kwargs["highlightthickness"] = 0
        kwargs["selectbackground"] = self.style.lookup("TSpinbox",
                                                       "selectbackground",
                                                       ("focus",))
        kwargs["selectforeground"] = self.style.lookup("TSpinbox",
                                                       "selectforeground",
                                                       ("focus",))
        kwargs["background"] = self.style.lookup("TSpinbox",
                                                 "fieldbackground",
                                                 default='white')
        kwargs["foreground"] = self.style.lookup("TSpinbox",
                                                 "foreground")
        kwargs["buttonbackground"] = self.style.lookup("TSpinbox",
                                                       "background")
        tk.Spinbox.__init__(self, self.frame, **kwargs)
        tk.Spinbox.pack(self, padx=1, pady=1)
        self.frame.spinbox = self

        # pack/place/grid methods
        self.pack = self.frame.pack
        self.pack_slaves = self.frame.pack_slaves
        self.pack_propagate = self.frame.pack_propagate
        self.pack_configure = self.frame.pack_configure
        self.pack_info = self.frame.pack_info
        self.pack_forget = self.frame.pack_forget

        self.grid = self.frame.grid
        self.grid_slaves = self.frame.grid_slaves
        self.grid_size = self.frame.grid_size
        self.grid_rowconfigure = self.frame.grid_rowconfigure
        self.grid_remove = self.frame.grid_remove
        self.grid_propagate = self.frame.grid_propagate
        self.grid_info = self.frame.grid_info
        self.grid_location = self.frame.grid_location
        self.grid_columnconfigure = self.frame.grid_columnconfigure
        self.grid_configure = self.frame.grid_configure
        self.grid_forget = self.frame.grid_forget
        self.grid_bbox = self.frame.grid_bbox
        try:
            self.grid_anchor = self.frame.grid_anchor
        except AttributeError:
            pass

        self.place = self.frame.place
        self.place_configure = self.frame.place_configure
        self.place_forget = self.frame.place_forget
        self.place_info = self.frame.place_info
        self.place_slaves = self.frame.place_slaves

        self.bind('<1>', lambda e: self.focus_set())
        self.frame.bind("<FocusIn>", self.focusin)
        self.frame.bind("<FocusOut>", self.focusout)

    def focusout(self, event):
        """Change style on focus out events."""
        bc = self.style.lookup("TEntry", "bordercolor", ("!focus",))
        dc = self.style.lookup("TEntry", "darkcolor", ("!focus",))
        lc = self.style.lookup("TEntry", "lightcolor", ("!focus",))
        self.style.configure("%s.spinbox.TFrame" % self.frame, bordercolor=bc,
                             darkcolor=dc, lightcolor=lc)

    def focusin(self, event):
        """Change style on focus in events."""
        self.old_value = self.get()
        bc = self.style.lookup("TEntry", "bordercolor", ("focus",))
        dc = self.style.lookup("TEntry", "darkcolor", ("focus",))
        lc = self.style.lookup("TEntry", "lightcolor", ("focus",))
        self.style.configure("%s.spinbox.TFrame" % self.frame, bordercolor=bc,
                             darkcolor=dc, lightcolor=lc)
