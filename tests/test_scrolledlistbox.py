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
