"""
Author: Juliette Monsel
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets import AutoHideScrollbar


class AutocompleteEntryListbox(ttk.Frame):
    """
    :class:`ttk.Entry` that features autocompletion combined with a
    :class:`tk.Listbox` to display the completion list.
    """
    def __init__(self, master=None, completevalues=[], allow_other_values=False,
                 autohidescrollbar=True, **kwargs):
        """
        Create an Entry + Listbox widget with autocompletion.

        :param master: master widget
        :type master: widget
        :param completevalues: autocompletion values
        :type completevalues: list
        :param allow_other_values: whether the user is allowed to enter values not in the list
        :type allow_other_values: bool
        :param width: widget width (in characters)
        :type width: int
        :param exportselection: whether to automatically export selected text to the clipboard
        :type exportselection: bool
        :param justify: text alignment in entry and listbox
        :type justify: str
        :param font: font in entry and listbox
        :param autohidescrollbar: whether to use an :class:`~ttkwidgets.AutoHideScrollbar` or a :class:`ttk.Scrollbar`
        :type autohidescrollbar: bool
        :param kwargs: keyword arguments passed to the :class:`ttk.Frame` initializer
        """
        exportselection = kwargs.pop('exportselection', False)
        width = kwargs.pop('width', None)
        justify = kwargs.pop('justify', None)
        font = kwargs.pop('font', None)
        kwargs.setdefault('padding', 4)

        ttk.Frame.__init__(self, master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._allow_other_values = allow_other_values
        self._completevalues = completevalues
        validatecmd = self.register(self._validate)
        self.entry = ttk.Entry(self, width=width, justify=justify, font=font,
                               validate='key', exportselection=exportselection,
                               validatecommand=(validatecmd, "%d", "%S", "%i", "%s", "%P"))
        f = ttk.Frame(self, style='border.TFrame', padding=1)
        self.listbox = tk.Listbox(f, width=width, font=font,
                                  exportselection=exportselection, selectmode="browse",
                                  highlightthickness=0, relief='flat')
        try:
            self.listbox.configure(justify=justify)   # this is an option only for tk >= 8.6.5
        except tk.TclError:
            pass
        self.listbox.pack(fill='both', expand=True)
        if autohidescrollbar:
            self._scrollbar = AutoHideScrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        else:
            self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self._scrollbar.set)
        self.entry.grid(sticky='ew')
        f.grid(sticky='nsew')
        self._scrollbar.grid(row=1, column=1, sticky='ns')
        for c in self._completevalues:
            self.listbox.insert('end', c)

        self.listbox.bind('<<ListboxSelect>>', self._update_entry)
        self.listbox.bind("<KeyPress>", self._listbox_keypress)
        self.entry.bind("<Tab>", self._tab)
        self.entry.bind("<Right>", self._right)
        self.entry.bind("<Down>", self._down)
        self.listbox.bind("<Down>", self._down)
        self.entry.bind("<Up>", self._up)
        self.listbox.bind("<Up>", self._up)
        self.entry.bind("<Control-a>", self._select_all)
        self.entry.focus_set()

    def _select_all(self, event):
        """Select all entry content."""
        self.entry.selection_range(0, 'end')
        return "break"

    def _right(self, event):
        """Move at the end of selected text on right press."""
        if self.entry.selection_present():
            self.entry.select_clear()
            self.entry.icursor("end")
            return "break"

    def _tab(self, event):
        """Move at the end of selected text on tab press."""
        self.entry.select_clear()
        self.entry.icursor("end")
        return "break"

    def _listbox_keypress(self, event):
        """Select the first item which name begin by the key pressed."""
        key = event.char.lower()
        l = [i for i in self._completevalues if i[0].lower() == key]
        if l:
            i = self._completevalues.index(l[0])
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(i)
            self.listbox.see(i)
            self._update_entry()

    def _up(self, event):
        """Navigate in the listbox with up key."""
        try:
            i = self.listbox.curselection()[0]
            self.listbox.selection_clear(0, "end")
            if i <= 0:
                i = len(self._completevalues)
            self.listbox.see(i - 1)
            self.listbox.select_set(i - 1)
            self.listbox.activate(i - 1)
        except (tk.TclError, IndexError):
            self.listbox.selection_clear(0, "end")
            i = len(self._completevalues)
            self.listbox.see(i - 1)
            self.listbox.select_set(i - 1)
            self.listbox.activate(i - 1)
        self.listbox.event_generate('<<ListboxSelect>>')
        return "break"

    def _down(self, event):
        """Navigate in the listbox with down key."""
        try:
            i = self.listbox.curselection()[0]
            self.listbox.selection_clear(0, "end")
            if i >= len(self._completevalues) - 1:
                i = -1
            self.listbox.see(i + 1)
            self.listbox.select_set(i + 1)
            self.listbox.activate(i + 1)
        except (tk.TclError, IndexError):
            self.listbox.selection_clear(0, "end")
            self.listbox.see(0)
            self.listbox.select_set(0)
            self.listbox.activate(0)
        self.listbox.event_generate('<<ListboxSelect>>')
        return "break"

    def _validate(self, action, modif, pos, prev_txt, new_txt):
        """Complete the text in the entry with values."""
        try:
            sel = self.entry.selection_get()
            txt = prev_txt.replace(sel, '')
        except tk.TclError:
            txt = prev_txt
        if action == "0":
            txt = txt[:int(pos)] + txt[int(pos) + 1:]
            return True
        else:
            txt = txt[:int(pos)] + modif + txt[int(pos):]
            l = [i for i in self._completevalues if i[:len(txt)] == txt]
            if l:
                i = self._completevalues.index(l[0])
                self.listbox.selection_clear(0, "end")
                self.listbox.selection_set(i)
                self.listbox.see(i)
                index = self.entry.index("insert")
                self.entry.delete(0, "end")
                self.entry.insert(0, l[0].replace("\ ", " "))
                self.entry.selection_range(index + 1, "end")
                self.entry.icursor(index + 1)
                return True
            else:
                return self._allow_other_values

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        return self.configure({key: value})

    def _update_entry(self, event=None):
        """Update entry when an item is selected in the listbox."""
        try:
            sel = self.listbox.get(self.listbox.curselection()[0])
        except (tk.TclError, IndexError):
            return
        self.entry.delete(0, "end")
        self.entry.insert(0, sel)
        self.entry.selection_clear()
        self.entry.icursor("end")
        self.event_generate('<<ItemSelect>>')

    def keys(self):
        keys = ttk.Frame.keys(self)
        keys.extend(['completevalues', 'allow_other_values', 'exportselection',
                     'justify', 'font'])
        return keys

    def get(self):
        "Return the text in the entry."
        return self.entry.get()

    def cget(self, key):
        if key == 'allow_other_values':
            return self._allow_other_values
        elif key == 'completevalues':
            return self._completevalues
        elif key == 'autohidescrollbar':
            return isinstance(self._scrollbar, AutoHideScrollbar)
        elif key in ['justify', 'font', 'exportselection', 'width']:
            return self.entry.cget(key)
        else:
            return ttk.Frame.cget(self, key)

    def configure(self, cnf={}, **kw):
        kwargs = {}
        kwargs.update(cnf)
        kwargs.update(kw)
        # completion settings
        self._allow_other_values = kwargs.pop('allow_other_values', self._allow_other_values)
        if 'completevalues' in kwargs:
            completevalues = kwargs.pop('completevalues')
            self._completevalues = completevalues
            self.listbox.delete(0, 'end')
            for c in self._completevalues:
                self.listbox.insert('end', c)

        # autohidescrollbar
        autohidescrollbar = isinstance(self._scrollbar, AutoHideScrollbar)
        autohidescrollbar2 = kwargs.pop('autohidescrollbar', autohidescrollbar)
        if autohidescrollbar != autohidescrollbar2:
            self._scrollbar.destroy()
            if autohidescrollbar2:
                self._scrollbar = AutoHideScrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
            else:
                self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
            self.listbox.configure(yscrollcommand=self._scrollbar.set)
            self._scrollbar.grid(row=1, column=1, sticky='ns')
        # entry/listbox settings
        entry_listbox_kw = {}
        for key in ['font', 'exportselection', 'width']:
            if key in kwargs:
                entry_listbox_kw[key] = kwargs.pop(key)
        self.entry.configure(entry_listbox_kw)
        self.listbox.configure(entry_listbox_kw)
        if 'justify' in kwargs:
            justify = kwargs.pop('justify')
            self.entry.configure(justify=justify)
            try:
                self.listbox.configure(justify=justify)   # this is an option only for tk >= 8.6.5
            except tk.TclError:
                pass
        # frame settings
        ttk.Frame.config(self, kwargs)

    config = configure
