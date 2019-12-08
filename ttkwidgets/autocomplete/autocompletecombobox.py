"""
Authors: Mitja Martini and Russell Adams
License: "Licensed same as original by Mitja Martini or public domain, whichever is less restrictive"
Source: https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html

Edited by RedFantom for ttk and Python 2 and 3 cross-compatibility and <Enter> binding
Edited by Juliette Monsel to include Tcl code to navigate the dropdown by Pawel Salawa
(https://wiki.tcl-lang.org/page/ttk%3A%3Acombobox, copyright 2011)
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

tk_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']


class AutocompleteCombobox(ttk.Combobox):
    """:class:`ttk.Combobox` widget that features autocompletion."""
    def __init__(self, master=None, completevalues=None, **kwargs):
        """
        Create an AutocompleteCombobox.

        :param master: master widget
        :type master: widget
        :param completevalues: autocompletion values
        :type completevalues: list
        :param kwargs: keyword arguments passed to the :class:`ttk.Combobox` initializer
        """
        ttk.Combobox.__init__(self, master, values=completevalues, **kwargs)
        self._completion_list = completevalues
        if isinstance(completevalues, list):
            self.set_completion_list(completevalues)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        # navigate on keypress in the dropdown:
        # code taken from https://wiki.tcl-lang.org/page/ttk%3A%3Acombobox by Pawel Salawa, copyright 2011
        self.tk.eval("""
proc ComboListKeyPressed {w key} {
        if {[string length $key] > 1 && [string tolower $key] != $key} {
                return
        }

        set cb [winfo parent [winfo toplevel $w]]
        set text [string map [list {[} {\[} {]} {\]}] $key]
        if {[string equal $text ""]} {
                return
        }

        set values [$cb cget -values]
        set x [lsearch -glob -nocase $values $text*]
        if {$x < 0} {
                return
        }

        set current [$w curselection]
        if {$current == $x && [string match -nocase $text* [lindex $values [expr {$x+1}]]]} {
                incr x
        }

        $w selection clear 0 end
        $w selection set $x
        $w activate $x
        $w see $x
}

set popdown [ttk::combobox::PopdownWindow %s]
bind $popdown.f.l <KeyPress> [list ComboListKeyPressed %%W %%K]
""" % (self))

    def set_completion_list(self, completion_list):
        """
        Use the completion list as drop down selection menu, arrows move through menu.

        :param completion_list: completion values
        :type completion_list: list
        """
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self.configure(values=completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """
        Autocomplete the Combobox.

        :param delta: 0, 1 or -1: how to cycle through possible hits
        :type delta: int
        """
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """
        Event handler for the keyrelease event on this widget.

        :param event: Tkinter event
        """
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position -= 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if event.keysym == "Return":
            self.handle_return(None)
            return
        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

    def handle_return(self, event):
        """
        Function to bind to the Enter/Return key so if Enter is pressed the selection is cleared

        :param event: Tkinter event
        """
        self.icursor(tk.END)
        self.selection_clear()

    def config(self, **kwargs):
        """Alias for configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure widget specific keyword arguments in addition to :class:`ttk.Combobox` keyword arguments."""
        if "completevalues" in kwargs:
            self.set_completion_list(kwargs.pop("completevalues"))
        return ttk.Combobox.configure(self, **kwargs)

    def cget(self, key):
        """Return value for widget specific keyword arguments"""
        if key == "completevalues":
            return self._completion_list
        return ttk.Combobox.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = ttk.Combobox.keys(self)
        keys.append("completevalues")
        return keys

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, item):
        return self.cget(item)
