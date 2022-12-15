"""
Author: RedFantom
License: GNU GPLv3
Source: This repository

Edited by rdbende: translation, autocompleteentrylistbox, and defult font option
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from .familylistbox import FontFamilyListbox
from .sizedropdown import FontSizeDropdown
from .propertiesframe import FontPropertiesFrame
from .familydropdown import FontFamilyDropdown
from locale import getdefaultlocale


# --- Translation
EN = {"Font family": "Font family", "Font properties": "Font properties",
      "Font size": "Font size", "Cancel": "Cancel", "Font Chooser": "Font Chooser"}

FR = {"Font family": "Famille", "Font properties": "Propriétés",
      "Font size": "Taille", "Cancel": "Annuler", "Font Chooser": "Sélecteur de polices"}

DE = {"Font family": "Familie", "Font properties": "Eigenschaften",
      "Font size": "Schriftgröße", "Cancel": "Abbrechen", "Font Chooser": "Schriftauswahl"}

HU = {"Font family": "Betűtípus", "Font properties": "Betűstílus",
      "Font size": "Méret", "Cancel": "Mégse", "Font Chooser": "Betűtípus"}

try:
    if getdefaultlocale()[0][:2] == "fr":
        TR = FR
    elif getdefaultlocale()[0][:2] == "de":
        TR = DE
    elif getdefaultlocale()[0][:2] == "hu":
        TR = HU
    else:
        TR = EN
except ValueError:
    TR = EN


def tr(text):
    """Translate text."""
    return TR.get(text, text)


class FontChooser(tk.Toplevel):
    """
    A Toplevel to choose a :class:`~font.Font` from a list.
    Should only be used through :func:`askfont`.
    """

    def __init__(self, master=None, title=None, default=("Arial", 9), **kwargs):
        """
        Create a FontChooser.
        
        :param master: master window
        :type master: widget
        :param title: dialog title
        :type title: str
        :param default: set the default font, family and size must be specified: (family, size, options)
        :type default: tuple
        :param kwargs: keyword arguments passed to :class:`tk.Toplevel` initializer
        """
        tk.Toplevel.__init__(self, master, **kwargs)
        
        self.title(title)
        self.transient(self.master)
        self.resizable(False, False)

        self._family = default[0]
        self._size = default[1]
        self._bold = True if "bold" in default else False
        self._italic = True if "italic" in default else False
        self._underline = True if "underline" in default else False
        self._overstrike = True if "overstrike" in default else False
        
        self._font_family_frame = ttk.LabelFrame(self, text=tr("Font family"))
        # I don't know why, but search with lowercase characters doesn't work for me
        self._font_family_list = FontFamilyListbox(self._font_family_frame, callback=self._on_family,
                                                   font=default, listboxheight=8)
        self._font_properties_frame = ttk.LabelFrame(self, text=tr("Font properties"))
        self._font_properties = FontPropertiesFrame(self._font_properties_frame, callback=self._on_properties,
                                                    font=self.__generate_font_tuple()[2:], label=False)
        self._font_size_frame = ttk.LabelFrame(self, text=tr("Font size"))
        self._size_dropdown = FontSizeDropdown(self._font_size_frame, font=default, callback=self._on_size, width=6)
        self._example_label = tk.Label(self, text="AaBbYyZz01", height=2, anchor=tk.CENTER, relief=tk.SOLID, borderwidth=1)
        
        self._font = None
        self._ok_button = ttk.Button(self, text="Ok", command=self._close)
        self._cancel_button = ttk.Button(self, text=tr("Cancel"), command=self._cancel)
        self._grid_widgets()
        self._on_change()
        
        # To be consistent with colorpicker
        self.wait_visibility()
        self.lift()
        self.grab_set()

    def _grid_widgets(self):
        """Puts all the child widgets in the correct position."""
        self._font_family_frame.grid(row=0, rowspan=2, column=0, sticky="nswe", padx=5, pady=5)
        self._font_family_list.grid(row=0, column=0, sticky="nswe", padx=5, pady=(0, 5))
        
        self._font_properties_frame.grid(row=0, column=1, columnspan=2, sticky="nswe", padx=5, pady=5)
        self._font_properties.pack(anchor=tk.CENTER, pady=15)
        
        self._font_size_frame.grid(row=1, column=1, columnspan=2, sticky="nswe", padx=5, pady=5)
        self._size_dropdown.pack(anchor=tk.CENTER, pady=15)
        
        self._example_label.grid(row=2, column=0, columnspan=3, sticky="nswe", padx=5, pady=5)
        
        self._ok_button.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self._cancel_button.grid(row=3, column=2, sticky="e", padx=5, pady=5)

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


def askfont(master=None, title=tr("Font Chooser"), default=("Arial", 9)):
    """
    Opens a :class:`FontChooser` dialog and return the chosen font.
    
    :return: font tuple (family_name, size, \*options), :class:`~font.Font` object

    :param master: parent widget
    :type master: widget
    :param title: dialog title
    :type title: str
    :param default: set the default font, family and size must be specified: (family, size, options)
    :type default: tuple 
    """
    chooser = FontChooser(master, title, default)
    chooser.wait_window(chooser)
    return chooser.font
