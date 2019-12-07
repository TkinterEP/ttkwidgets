# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets.utilities import move_widget, parse_geometry
from tests import BaseWidgetTest
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class TestUtilities(BaseWidgetTest):
    def test_move_widget(self):
        label = ttk.Label(self.window)
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())

    def test_move_widget_pack(self):
        label = ttk.Label(self.window)
        label.pack()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.pack()
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())
        self.assertIn(label, tl.pack_slaves())

    def test_move_widget_grid(self):
        label = ttk.Label(self.window)
        label.grid()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.grid()
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())
        self.assertIn(label, tl.grid_slaves())

    def test_move_widget_place(self):
        label = ttk.Label(self.window)
        label.place()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.place()
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())
        self.assertIn(label, tl.place_slaves())

    def test_move_widget_with_binding(self):
        raise NotImplementedError

    def test_move_widget_with_binding_on_parent(self):
        raise NotImplementedError

    def test_parse_geometry(self):
        g = parse_geometry('1x1+1+1')
        self.assertEqual(g, (1, 1, 1, 1))
        g = parse_geometry('1x1-1-1')
        self.assertEqual(g, (1, 1, -1, -1))
