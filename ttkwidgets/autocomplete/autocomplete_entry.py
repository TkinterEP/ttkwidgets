"""
Authors: Mitja Martini and Russell Adams
License: "Licensed same as original by Mitja Martini or public domain, whichever is less restrictive"
Source: https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html

Edited by RedFantom for ttk and Python 2 and 3 cross-compatibility and <Enter> binding
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

tk_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']


class AutocompleteEntry(ttk.Entry):
    """
    Subclass of tk.Entry that features autocompletion.

    To enable autocompletion use set_completion_list(list) to define
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.
    """
    def __init__(self, master=None, completevalues=None, **kwargs):
        """
        :param master: master widget
        :param completevalues: autocompletion values list
        :param kwargs: keyword arguments passed on to Entry initializer
        """
        ttk.Entry.__init__(self, master, **kwargs)
        self._completion_list = completevalues
        self.set_completion_list(completevalues)
        self._hits = []
        self._hit_index = 0
        self.position = 0

    def set_completion_list(self, completion_list):
        """
        Set a new auto completion list
        :param completion_list: list of values
        :return: None
        """
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """
        Autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits
        :param delta: int
        :return: None
        """
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case-insensitively
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
        Event handler for the keyrelease event on this widget
        :param event: Tkinter event
        :return: None
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
        if event.keysym == "Down":
            self.autocomplete(1)  # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        if event.keysym == "Return":
            self.handle_return(None)
            return
        if len(event.keysym) == 1 or event.keysym in tk_umlauts:
            self.autocomplete()

    def handle_return(self, event):
        """
        Function to bind to the Enter/Return key so if Enter is pressed the selection is cleared
        :param event: Tkinter event
        :return: None
        """
        self.icursor(tk.END)
        self.selection_clear()
