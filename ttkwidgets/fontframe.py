"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Nelson Brochado (https://www.github.com/nbro/tkinter-kit)
try:
    import Tkinter as tk
    import ttk
    import tkFont as font
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font
from ttkwidgets import ScrolledListbox
from ttkwidgets.autocomplete import AutocompleteCombobox


class FontFamilyListbox(ScrolledListbox):
    """
    ScrolledListbox listing all font families available on the system with a Scrollbar on the right with the option
    of a callback when double clicked and a property to get the font family name
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :param callback: callable object with one argument: the font family name
        :param kwargs: keyword arguments passed to ScrolledListbox, in turn passed to Listbox
        """
        ScrolledListbox.__init__(self, master, compound=tk.RIGHT, **kwargs)
        self._callback = callback
        font_names = sorted(font.families())
        index = 0
        self.font_indexes = {}
        for name in font_names:
            self.listbox.insert(index, name)
            self.font_indexes[index] = name
            index += 1
        self.listbox.bind("<Button-1>", self._on_click)

    def _on_click(self, *args):
        """
        Function bound to double click on Listbox that calls the callback if a valid callback object is passed
        :param args: Tkinter event
        :return: None
        """
        if callable(self._callback):
            self._callback(self.selection)

    @property
    def selection(self):
        """
        Selection property returns None if no font is selected and font family name if one is selected
        :return:
        """
        selection = self.listbox.curselection()
        if len(selection) is 0:
            return None
        return self.font_indexes[self.listbox.curselection()[0]]


class FontFamilyDropdown(AutocompleteCombobox):
    """
    A dropdown menu to select a font family with callback support and selection property
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :param callback: callable object with single argument: font family name
        :param kwargs: keyword arguments passed on to AutocompleteCombobox initializer
        """
        font_families = sorted([item for item in font.families()])
        self._fonts = font_families
        self._font = tk.StringVar()
        self.__callback = callback
        AutocompleteCombobox.__init__(self, master, textvariable=self._font, completevalues=font_families, **kwargs)
        self.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, *args):
        """
        Function bound to event of selection in the Combobox, calls callback if callable
        :param args: Tkinter event
        :return: None
        """
        if callable(self.__callback):
            self.__callback(self.selection)

    @property
    def selection(self):
        """
        Selection property returns None if no font is selected and font family name if one is selected
        :return:
        """
        if self._font.get() is "" or self._font.get() not in self._fonts:
            return None
        else:
            return self._font.get()


class FontSizeDropdown(AutocompleteCombobox):
    """
    A dropdown with default font sizes
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :param callback: callback on click with signle argument: int size
        :param kwargs: keyword arguments passed on to AutocompleteCombobox initializer
        """
        int_values = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        values = [str(value) for value in int_values]
        AutocompleteCombobox.__init__(self, master, completevalues=values, **kwargs)
        self.bind("<<ComboboxSelected>>", self._on_click)
        self.__callback = callback
        self.insert(0, "12")

    def _on_click(self, event):
        """
        Function bound to event of selection in the Combobox, calls callback if callable
        :param event: Tkinter event
        :return: None
        """
        if callable(self.__callback):
            self.__callback(self.selection)

    @property
    def selection(self):
        """
        Property that returns None if no value is selected and int size if selected
        :return: None
        """
        if self.get() is "":
            return None
        else:
            return int(self.get())


class FontPropertiesFrame(ttk.Frame):
    """
    Simple frame with buttons for Bold, Italic and Undelrine font types
    """

    def __init__(self, master=None, callback=None, label=True, fontsize=11, **kwargs):
        """
        :param master: master widget
        :param callback: callback with argument (bool bold, bool italic, bool underline, bool overstrike)
        :param label: show a header label
        :param fontsize: size of the font on the buttons
        :param kwargs: keyword arguments passed on to Frame initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self._style = ttk.Style()
        self.__label = label
        self.__callback = callback
        self._header_label = ttk.Label(self, text="Font properties:")
        self._style.configure("Bold.Toolbutton", font=("default", fontsize, "bold"), anchor=tk.CENTER)
        self._style.configure("Italic.Toolbutton", font=("default", fontsize, "italic"), anchor=tk.CENTER)
        self._style.configure("Underline.Toolbutton", font=("default", fontsize, "underline"), anchor=tk.CENTER)
        self._style.configure("Overstrike.Toolbutton", font=("default", fontsize, "overstrike"), anchor=tk.CENTER)
        self._bold = tk.BooleanVar()
        self._italic = tk.BooleanVar()
        self._underline = tk.BooleanVar()
        self._overstrike = tk.BooleanVar()
        self._bold_button = ttk.Checkbutton(self, style="Bold.Toolbutton", text="B", width=2, command=self._on_click,
                                            variable=self._bold)
        self._italic_button = ttk.Checkbutton(self, style="Italic.Toolbutton", text="I", width=2,
                                              command=self._on_click, variable=self._italic)
        self._underline_button = ttk.Checkbutton(self, style="Underline.Toolbutton", text="U", width=2,
                                                 command=self._on_click, variable=self._underline)
        self._overstrike_button = ttk.Checkbutton(self, style="Overstrike.Toolbutton", text="O", width=2,
                                                  command=self._on_click, variable=self._overstrike)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Place the widgets in the correct positions
        :return: None
        """
        if self.__label:
            self._header_label.grid(row=0, column=1, columnspan=3, sticky="nw", padx=5, pady=(5, 0))
        self._bold_button.grid(row=1, column=1, sticky="nswe", padx=5, pady=2)
        self._italic_button.grid(row=1, column=2, sticky="nswe", padx=(0, 5), pady=2)
        self._underline_button.grid(row=1, column=3, sticky="nswe", padx=(0, 5), pady=2)
        self._overstrike_button.grid(row=1, column=4, sticky="nswe", padx=(0, 5), pady=2)

    def _on_click(self):
        """
        Handles clicks and calls callback
        :return: None
        """
        if callable(self.__callback):
            self.__callback((self.bold, self.italic, self.underline, self.overstrike))

    @property
    def bold(self):
        """
        :return: True if bold is selected
        """
        return self._bold.get()

    @property
    def italic(self):
        """
        :return: True if italic is selected
        """
        return self._italic.get()

    @property
    def underline(self):
        """
        :return: True if underline is selected
        """
        return self._underline.get()

    @property
    def overstrike(self):
        """
        :return: True if overstrike is selected
        """
        return self._overstrike.get()


class FontSelectFrame(ttk.Frame):
    """
    A frame to use in your own application to let the user choose a font

    For tkFont object, use font property
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widgets
        :param callback: callback passed argument (str family, int size, bool bold, bool italic, bool underline,
                                                   bool overstrike)
        :param kwargs: passed on to Frame initializer
        """
        ttk.Frame.__init__(self, master, **kwargs)
        self.__callback = callback
        self._family = None
        self._size = 11
        self._bold = False
        self._italic = False
        self._underline = False
        self._overstrike = False
        self._family_dropdown = FontFamilyDropdown(self, callback=self._on_family)
        self._size_dropdown = FontSizeDropdown(self, callback=self._on_size, width=4)
        self._properties_frame = FontPropertiesFrame(self, callback=self._on_properties, label=False)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts all the widgets in the correct place
        :return: None
        """
        self._family_dropdown.grid(row=0, column=0, sticky="nswe")
        self._size_dropdown.grid(row=0, column=1, sticky="nswe")
        self._properties_frame.grid(row=0, column=2, sticky="nswe")

    def _on_family(self, name):
        """
        Callback if family is changed
        :param name: font family name
        :return: None
        """
        self._family = name
        self._on_change()

    def _on_size(self, size):
        """
        Callback if size is changed
        :param size: font size int
        :return: None
        """
        self._size = size
        self._on_change()

    def _on_properties(self, properties):
        """
        Callback if properties are changed
        :param properties: tuple (bold, italic, underline, overstrike)
        :return: None
        """
        self._bold, self._italic, self._underline, self._overstrike = properties
        self._on_change()

    def _on_change(self):
        """
        Call callback if any property is changed
        :return: None
        """
        if callable(self.__callback):
            self.__callback((self._family, self._size, self._bold, self._italic, self._underline, self._overstrike))

    def __generate_font_tuple(self):
        """
        Generate a font tuple for tkinter widgets based on the user's entries
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
        Returns a Font object if family is set, else None
        :return: Font or None
        """
        if not self._family:
            return None
        font_obj = font.Font(family=self._family, size=self._size,
                             weight=font.BOLD if self._bold else font.NORMAL,
                             slant=font.ITALIC if self._italic else font.ROMAN,
                             underline=1 if self._underline else 0,
                             overstrike=1 if self._overstrike else 0)
        font_tuple = self.__generate_font_tuple()
        return font_tuple, font_obj


class FontChooser(tk.Toplevel):
    """
    A Toplevel to choose a Font from a list. Should only be used through askfont()
    """

    def __init__(self, master=None, **kwargs):
        """
        :param master: master tk.Tk instance
        :param kwargs: keyword arguments passed to Toplevel initializer
        """
        tk.Toplevel.__init__(self, master, **kwargs)
        self.wm_title("Choose a font")
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("FontChooser.TLabel", font=("default", 11), relief=tk.SUNKEN, anchor=tk.CENTER)
        self._font_family_header = ttk.Label(self, text="Font family", style="FontChooser.TLabel")
        self._font_family_list = FontFamilyListbox(self, callback=self._on_family, height=8)
        self._font_label_variable = tk.StringVar()
        self._font_label = ttk.Label(self, textvariable=self._font_label_variable, background="white")
        self._font_properties_header = ttk.Label(self, text="Font properties", style="FontChooser.TLabel")
        self._font_properties_frame = FontPropertiesFrame(self, callback=self._on_properties, label=False)
        self._font_size_header = ttk.Label(self, text="Font size", style="FontChooser.TLabel")
        self._size_dropdown = FontSizeDropdown(self, callback=self._on_size, width=4)
        self._example_label = tk.Label(self, text="Example", anchor=tk.CENTER, background="white", height=2,
                                       relief=tk.SUNKEN)

        self._family = None
        self._size = 11
        self._bold = False
        self._italic = False
        self._underline = False
        self._overstrike = False
        self._font = None
        self._ok_button = ttk.Button(self, text="OK", command=self._close)
        self._cancel_button = ttk.Button(self, text="Cancel", command=self._cancel)
        self._grid_widgets()

    def _grid_widgets(self):
        """
        Puts all the child widgets in the correct position
        :return: None
        """
        self._font_family_header.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        self._font_label.grid(row=1, column=1, sticky="nswe", padx=5, pady=(0, 5))
        self._font_family_list.grid(row=2, rowspan=3, column=1, sticky="nswe", padx=5, pady=(0, 5))
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
        :return: None
        """
        self._font_label_variable.set(family)
        self._family = family
        self._on_change()

    def _on_size(self, size):
        """
        Callback if size is changed
        :param size: int size
        :return: None
        """
        self._size = size
        self._on_change()

    def _on_properties(self, properties):
        """
        Callback if properties are changed
        :param properties: (bool bold, bool italic, bool underline, bool overstrike)
        :return: None
        """
        self._bold, self._italic, self._underline, self._overstrike = properties
        self._on_change()

    def _on_change(self):
        """
        Callback if any of the values are changed
        :return: None
        """
        font = self.__generate_font_tuple()
        self._example_label.configure(font=font)

    def __generate_font_tuple(self):
        """
        Generate a font tuple for tkinter widgets based on the user's entries
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
        :return: font tuple (family_name, size, *options), font object
        """
        if self._family is None:
            return None, None
        else:
            font_tuple = self.__generate_font_tuple()
            font_obj = font.Font(family=self._family, size=self._size,
                                 weight=font.BOLD if self._bold else font.NORMAL,
                                 slant=font.ITALIC if self._italic else font.ROMAN,
                                 underline=1 if self._underline else 0,
                                 overstrike=1 if self._overstrike else 0)
            return font_tuple, font_obj

    def _close(self):
        """
        Destroy the window
        :return: None
        """
        self.destroy()

    def _cancel(self):
        """
        Cancel font selection and destroy window
        :return: None
        """
        self._family = None
        self.destroy()


def askfont():
    """
    Opens a FontChooser Toplevel to allow the user to select a font
    :return: chooser.font result
    """
    chooser = FontChooser()
    chooser.wait_window()
    return chooser.font
