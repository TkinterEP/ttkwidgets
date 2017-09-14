"""
Author: Juliette Monsel
License: GNU GPLv3
Source: This repository
"""
# Based on an idea by Fredrik Lundh (effbot.org/zone/tkinter-autoscrollbar.htm)
# adapted to support all layouts
try:
    import ttk
except ImportError:
    from tkinter import ttk


class AutoScrollbar(ttk.Scrollbar):
    """Scrollbar that automatically hide when not needed."""
    def __init__(self, *args, **kwargs):
        """
        Create the scrollbar.

        Take the same arguments than ttk.Scrollbar
        """
        ttk.Scrollbar.__init__(self, *args, **kwargs)
        self._pack_kw = {}
        self._place_kw = {}
        self._layout = 'place'

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            if self._layout == 'place':
                self.place_forget()
            elif self._layout == 'pack':
                self.pack_forget()
            else:
                self.grid_remove()
        else:
            if self._layout == 'place':
                self.place(**self._place_kw)
            elif self._layout == 'pack':
                self.pack(**self._pack_kw)
            else:
                self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def place(self, **kw):
        ttk.Scrollbar.place(self, **kw)
        self._place_kw = self.place_info()
        self._layout = 'place'

    def pack(self, **kw):
        ttk.Scrollbar.pack(self, **kw)
        self._pack_kw = self.pack_info()
        self._layout = 'pack'

    def grid(self, **kw):
        ttk.Scrollbar.grid(self, **kw)
        self._layout = 'grid'
