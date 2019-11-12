"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
try:
    import Tkinter as tk
    import ttk
    import tkFont as tkfont
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font as tkfont
from .familyentrylistbox import FontFamilyEntryListbox
from .sizedropdown import FontSizeDropdown
from .propertiesframe import FontPropertiesFrame


class FontChooser(tk.Toplevel):
    """
    A Toplevel to choose a :class:`~font.Font` from a list.
    Should only be used through :func:`askfont`.
    """

    def __init__(self, master=None, font=None, **kwargs):
        """
        Create a FontChooser.

        :param master: master window
        :type master: widget
        :param font: initially selected font
        :param kwargs: keyword arguments passed to :class:`tk.Toplevel` initializer
        """
        tk.Toplevel.__init__(self, master, **kwargs)
        self.wm_title("Choose a font")
        self.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("FontChooser.TLabel", font=("default", 11), relief=tk.SUNKEN, anchor=tk.CENTER)

        font_props = tkfont.Font(self, font=font, size=11).actual()

        self._font_family_header = ttk.Label(self, text="Font family", style="FontChooser.TLabel")
        self._font_family_list = FontFamilyEntryListbox(self, callback=self._on_family, wpad=4, height=8)
        self._font_properties_header = ttk.Label(self, text="Font properties", style="FontChooser.TLabel")
        self._font_properties_frame = FontPropertiesFrame(self, callback=self._on_properties, label=False)
        self._font_size_header = ttk.Label(self, text="Font size", style="FontChooser.TLabel")
        self._size_dropdown = FontSizeDropdown(self, callback=self._on_size, width=4)
        self._example_label = tk.Label(self, text="Example", anchor=tk.CENTER, background="white", height=2,
                                       relief=tk.SUNKEN, font=font)

        # initial values
        self._family = None if font is None else font_props['family']
        self._size = font_props['size']
        self._bold = font_props['weight'] == tkfont.BOLD
        self._italic = font_props['slant'] == tkfont.ITALIC
        self._underline = font_props['underline']
        self._overstrike = font_props['overstrike']
        self._ok_button = ttk.Button(self, text="OK", command=self._close)
        self._cancel_button = ttk.Button(self, text="Cancel", command=self._cancel)

        if font is not None:
            self._font_family_list.entry.insert(0, font_props['family'])
        self._size_dropdown.set(self._size)
        self._font_properties_frame.bold = self._bold
        self._font_properties_frame.italic = self._italic
        self._font_properties_frame.underline = self._underline
        self._font_properties_frame.overstrike = self._overstrike

        self._grid_widgets()

    def _grid_widgets(self):
        """Puts all the child widgets in the correct position."""
        self._font_family_header.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        self._font_family_list.grid(row=1, rowspan=4, column=1, sticky="nswe", padx=5, pady=(0, 5))
        self._font_properties_header.grid(row=0, column=2, sticky="nswe", padx=5, pady=5)
        self._font_properties_frame.grid(row=1, rowspan=2, column=2, sticky="we", padx=5, pady=5)
        self._font_size_header.grid(row=3, column=2, sticky="we", padx=5, pady=5)
        self._size_dropdown.grid(row=4, column=2, sticky="we", padx=5, pady=5)
        self._example_label.grid(row=5, column=1, columnspan=2, sticky="nswe", padx=5, pady=5)
        self._ok_button.grid(row=6, column=2, sticky="nswe", padx=5, pady=5)
        self._cancel_button.grid(row=6, column=1, sticky="nswe", padx=5, pady=5)

    def _on_family(self, family):
        """
        Callback if family is changed

        :param family: family name
        """
        self._family = family
        self._on_change()

    def _on_size(self, size):
        """
        Callback if size is changed

        :param size: int size
        """
        self._size = size
        self._on_change()

    def _on_properties(self, properties):
        """
        Callback if properties are changed.

        :param properties: (bool bold, bool italic, bool underline, bool overstrike)
        """
        self._bold, self._italic, self._underline, self._overstrike = properties
        self._on_change()

    def _on_change(self):
        """Callback if any of the values are changed."""
        font = self.__generate_font_tuple()
        self._example_label.configure(font=font)

    def __generate_font_tuple(self):
        """
        Generate a font tuple for tkinter widgets based on the user's entries.

        :return: font tuple (family_name, size, *options)
        """
        if not self._family:
            return None
        font = [self._family, self._size]
        if self._bold:
            font.append("bold")
        if self._italic:
            font.append("italic")
        if self._underline:
            font.append("underline")
        if self._overstrike:
            font.append("overstrike")
        return tuple(font)

    @property
    def font(self):
        """
        Selected font.

        :return: font tuple (family_name, size, \*options), :class:`~font.Font` object
        """
        if self._family is None:
            return None, None
        else:
            font_tuple = self.__generate_font_tuple()
            font_obj = tkfont.Font(family=self._family, size=self._size,
                                   weight=tkfont.BOLD if self._bold else tkfont.NORMAL,
                                   slant=tkfont.ITALIC if self._italic else tkfont.ROMAN,
                                   underline=1 if self._underline else 0,
                                   overstrike=1 if self._overstrike else 0)
            return font_tuple, font_obj

    def _close(self):
        """Destroy the window."""
        self.destroy()

    def _cancel(self):
        """Cancel font selection and destroy window."""
        self._family = None
        self.destroy()


def askfont(font=None, master=None):
    """
    Opens a :class:`FontChooser` toplevel to allow the user to select a font

    :param font: initially selected font

    :return: font tuple (family_name, size, \*options), :class:`~font.Font` object
    """
    chooser = FontChooser(master=master, font=font)
    chooser.wait_window()
    return chooser.font
