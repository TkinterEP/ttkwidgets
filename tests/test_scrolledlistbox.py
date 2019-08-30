# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ScrolledListbox
from tests import BaseWidgetTest

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestScrolledListBox(BaseWidgetTest):
    def test_scrolledlistbox_init(self):
        listbox = ScrolledListbox(self.window, height=10, width=10, compound=tk.LEFT)
        listbox.pack()
        self.window.update()
        self.assertFalse(listbox.scrollbar.winfo_ismapped())
        listbox.destroy()
        
        listbox = ScrolledListbox(self.window, height=20, width=10, compound=tk.RIGHT, autohidescrollbar=False)
        listbox.pack()
        self.window.update()
        self.assertTrue(listbox.scrollbar.winfo_ismapped())
