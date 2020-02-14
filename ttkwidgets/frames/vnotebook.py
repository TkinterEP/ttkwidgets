"""
Author: RedFantom
License: GNU GPLv3, as in LICENSE.md
Copyright (C) 2018 RedFantom
"""
# Basic UI imports
import tkinter as tk
from tkinter import ttk
from ttkwidgets.utilities import get_widget_options


class VNotebook(ttk.Frame):
    """
    Notebook with vertical tabs. Does not actually use the
    :class:`ttk.Notebook` widget, but a set of Toolbutton-styles
    Radiobuttons to select a Frame of a set. Provides an interface that
    behaves like a normal :class:`ttk.Notebook` widget.
    """

    options = [
        # Notebook options
        "cursor",
        "padding",
        "style",
        "takefocus",
        # VNotebook options
        "compound",
        "callback",
    ]

    tab_options = [
        "compound",
        "padding",
        "sticky",
        "image",
        "text",
        "underline",
        "font",
        "id",
    ]

    def __init__(self, master, **kwargs):
        """
        Create a VNotebook.

        :param cursor: Cursor set upon hovering Buttons
        :type cursor: str
        :param padding: Amount of pixels between the Buttons
        :type padding: int
        :param compound: Location of the Buttons
        :type compound: str
        :param kwargs: Passed on to :class:`ttk.Frame` initializer
        """
        # Argument processing
        self._cursor = kwargs.pop("cursor", "default")
        self._height = kwargs.pop("cursor", 400)
        self._width = kwargs.pop("width", 400)
        self._padding = kwargs.pop("padding", 0)
        self._style = kwargs.pop("style", "Toolbutton")
        self._compound = kwargs.pop("compound", tk.LEFT)

        kwargs["width"] = self._width
        kwargs["height"] = self._height

        # Initialize
        ttk.Frame.__init__(self, master, **kwargs)
        self.grid_propagate(False)

        # Attributes
        self._tab_buttons = dict()
        self._tab_frames = dict()
        self._tab_ids = list()
        self._frame_padding = dict()
        self._hidden = dict()
        self._variable = tk.StringVar()
        self.__current_tab = None
        self._buttons_frame = None
        self._separator = None

        # Initialize widgets
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        """Initialize child widgets."""
        self._buttons_frame = ttk.Frame(self)
        self._separator = ttk.Separator(self)

    def grid_widgets(self):
        """Put child widgets in place."""
        horizontal = self._compound in (tk.BOTTOM, tk.TOP)
        if horizontal is True:
            sticky = "sw" if self._compound == tk.BOTTOM else "nw"
            self.columnconfigure(2, weight=1)
        else:
            sticky = "nw" if self._compound == tk.RIGHT else "ne"
            self.rowconfigure(2, weight=1)

        self._buttons_frame.grid(row=2, column=2, sticky=sticky)
        self._separator.config(
            orient=tk.HORIZONTAL if horizontal is True else tk.VERTICAL)
        if self.active is None:
            return

        # Grid the position dependent widgets
        pad, sticky = self._frame_padding[self.active]
        padding = {"padx": pad, "pady": pad}
        if self._compound == tk.BOTTOM:
            self._separator.grid(row=3, column=2, pady=4, sticky="swe")
            self.__current_tab.grid(row=4, column=2, sticky=sticky, **padding)
        elif self._compound == tk.TOP:
            self._separator.grid(row=1, column=2, pady=4, sticky="nwe")
            self.__current_tab.grid(row=0, column=2, sticky=sticky, **padding)
        elif self._compound == tk.RIGHT:
            self._separator.grid(row=2, column=3, padx=4, sticky="nsw")
            self.__current_tab.grid(row=2, column=4, sticky=sticky, **padding)
        elif self._compound == tk.LEFT:
            self._separator.grid(row=2, column=1, padx=4, sticky="nse")
            self.__current_tab.grid(row=2, column=0, sticky=sticky, **padding)
        else:
            raise ValueError("Invalid compound value: {}".format(self._compound))
        self._grid_tabs()

    def grid_forget_widgets(self):
        """Remove child widgets from grid."""
        self._buttons_frame.grid_forget()
        if self.__current_tab is not None:
            self.__current_tab.grid_forget()
        for button in self._tab_buttons.values():
            button.grid_forget()

    def _grid_tabs(self):
        """Organize tab buttons."""
        for button in self._tab_buttons.values():
            button.grid_forget()
        for index, tab_id in enumerate(self._tab_ids):
            if tab_id in self._hidden and self._hidden[tab_id] is True:
                continue
            horizontal = self._compound in (tk.BOTTOM, tk.TOP)
            row = index if horizontal is False else 0
            column = index if horizontal is True else 0
            self._tab_buttons[tab_id].grid(
                row=row, column=column, pady=self._padding, padx=self._padding, sticky="nswe")
        if self.active is None and len(self._tab_ids) != 0:
            self.activate(self._tab_ids[0])
        return

    def add(self, child, **kwargs):
        """
        Create new tab in the notebook and append it to the end.
        If the child is already managed by the VNotebook widget, then update the child with its settings.

        :param child: Child widget, such as a :class:`ttk.Frame`
        :param kwargs: Keyword arguments to create tab with.
            Supports all arguments supported by :meth:`VNotebook.tab`
            function, and in addition supports:

                :param id: ID for the newly added Tab. If the ID is not given, one is generated automatically.
                :param index: Position of the new Tab.

        :return: ID for the new Tab
        :rtype: int
        """
        tab_id = kwargs.pop("id", hash(child))
        updating = child in self._tab_frames.values()
        if not updating:
            self._tab_buttons[tab_id] = ttk.Radiobutton(
                self._buttons_frame, variable=self._variable, value=tab_id)
            self._tab_frames[tab_id] = child
        else:
            self._tab_frames[tab_id].config(**get_widget_options(child))

        # Process where argument
        where = kwargs.get("index", tk.END)
        if updating and 'index' in kwargs:
            self._tab_ids.pop(where)
            self._tab_ids.insert(where, tab_id)
        else:
            if where == tk.END:
                self._tab_ids.append(tab_id)
            else:
                self._tab_ids.insert(where, tab_id)
        kwargs.pop('index', None)
        self.tab(tab_id, **kwargs)
        return tab_id

    def insert(self, index, child, **kwargs):
        """:meth:`VNotebook.add` alias with non-optional index argument."""
        kwargs.update({"index": index})
        return self.add(child, **kwargs)

    def enable_traversal(self, enable=True):
        """Setup keybinds for CTRL-TAB to switch tabs."""
        if enable is True:
            func = "bind"
            args = ("<Control-Tab>", self._switch_tab,)
        else:
            func = "unbind"
            args = ("<Control-Tab>",)
        for widget in (self, self._buttons_frame, self._separator) + tuple(self._tab_frames.values()):
            getattr(widget, func)(*args)
        return enable

    def disable_traversal(self):
        """Alias of :obj:`VNotebook.enable_traversal(enable=False)`."""
        return self.enable_traversal(enable=False)

    def forget(self, child):
        """Remove a child by widget or tab_id."""
        tab_id = self.get_id_for_tab(child)
        self._tab_buttons[tab_id].destroy()
        del self._tab_buttons[tab_id]
        del self._tab_frames[tab_id]
        self._tab_ids.remove(tab_id)
        self._grid_tabs()

    def hide(self, child, hide=True):
        """Hide or unhide a Tab."""
        tab_id = self.get_id_for_tab(child)
        self._hidden[tab_id] = hide
        if tab_id == self.active and len(self._tab_ids) != 1:
            self.activate(self._tab_ids[0])
        self.grid_widgets()

    def show(self, child):
        """Alias for :obj:`VNotebook.hide(hide=False)`"""
        return self.hide(child, hide=False)

    def index(self, child):
        """Return zero-indexed index value of a child or tab_id."""
        return self._tab_ids.index(self.get_id_for_tab(child))

    def tab(self, tab_id, option=None, **kwargs):
        """
        Configure a tab with options given in kwargs.

        :param tab_id: Non-optional tab ID of the tab to be configured
        :param option: If not None, function returns value for option
            key given in this argument
        """
        if option is not None:
            return self._tab_buttons[tab_id].cget(option)
        # Argument processing
        self._frame_padding[tab_id] = \
            (kwargs.pop("padding", self._padding), kwargs.pop("sticky", tk.N))
        kwargs["command"] = lambda tab_id=tab_id: self.activate(tab_id)
        kwargs["style"] = "Toolbutton"
        # Configure Buttons
        self._tab_buttons[tab_id].configure(**kwargs)
        self._grid_tabs()

    def tab_configure(self, tab_id, **kwargs):
        """Configure alias for :meth:`VNotebook.tab`"""
        return self.tab(tab_id, **kwargs)

    def tab_cget(self, tab_id, key):
        """cget alias for :meth:`VNotebook.tab`"""
        return self.tab(tab_id, option=key)

    @property
    def tabs(self):
        """Return list of tab IDs."""
        return self._tab_ids.copy()

    def config(self, **kwargs):
        """Alias for :meth:`VNotebook.configure`"""
        return self.configure(**kwargs)

    def configure(self, **kwargs):
        """Change settings for the widget."""
        for option in self.options:
            attr = "_{}".format(option)
            setattr(self, attr, kwargs.pop(option, getattr(self, attr)))
        return super().configure(**kwargs)

    def cget(self, key):
        """Return current value for a setting."""
        if key in self.options:
            return getattr(self, "_{}".format(key))
        return ttk.Frame.cget(self, key)

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, key, value):
        return self.configure(**{key: value})

    def activate(self, tab_id):
        """Activate a new Tab in the notebook."""
        if self.active is not None:
            self.__current_tab.grid_forget()
        self.__current_tab = self._tab_frames[tab_id]
        self.grid_widgets()
        self._variable.set(tab_id)

    def activate_index(self, index):
        """Activate Tab by zero-indexed value."""
        return self.activate(self._tab_ids[index])

    @property
    def active(self):
        """Return tab_id for currently active Tab."""
        if self.__current_tab is None:
            return None
        return self.get_id_for_tab(self.__current_tab)

    def get_id_for_tab(self, child):
        """Return tab_id for child, which can be tab_id or widget."""
        if child in self._tab_ids:
            return child
        return {widget: tab_id for tab_id, widget in self._tab_frames.items()}[child]

    def _switch_tab(self, event):
        """Callback for CTRL-TAB."""
        if self.active is None:
            self.activate(self._tab_ids[0])
            return
        to_activate = self._tab_ids.index(self.active) + 1
        if to_activate == len(self._tab_ids):
            to_activate = 0
        self.activate(self._tab_ids[to_activate])
