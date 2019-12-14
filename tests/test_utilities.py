# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets.utilities import move_widget, parse_geometry, coords_in_box
from tests import BaseWidgetTest
import tkinter as tk
from tkinter import ttk


class TestUtilities(BaseWidgetTest):
    def setUp(self):
        BaseWidgetTest.setUp(self)
        self._dummy_flag = False

    def assertIsChild(self, child, parent):
        self.assertIn(child, parent.children.values())
        parent_of_parent = parent.winfo_parent()
        if not parent_of_parent.endswith("."):
            parent_of_parent += "."
        self.assertEquals(child.winfo_parent(), parent_of_parent + parent.winfo_name())

    def assertHasBeenInvoked(self):
        self.assertTrue(self._dummy_flag)
        self._dummy_flag = False
    
    def _dummy_bind(self, _=None):
        self._dummy_flag = True
    
    def test_move_widget(self):
        label = ttk.Label(self.window)
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        self.assertIsChild(label, tl)

    def test_move_widget_pack(self):
        label = ttk.Label(self.window)
        label.pack()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.pack()
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.pack_slaves())

    def test_move_widget_grid(self):
        label = ttk.Label(self.window)
        label.grid()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.grid()
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.grid_slaves())

    def test_move_widget_place(self):
        label = ttk.Label(self.window)
        label.place()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.place()
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.place_slaves())

    def test_move_widget_with_binding(self):
        label = ttk.Label(self.window)
        label.bind('<Enter>', self._dummy_bind)
        label.pack()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.pack()
        self.assertIsChild(label, tl)
        self.assertIn('<Enter>', label.bind())

    def test_move_widget_with_command(self):
        widget = ttk.Button(self.window, command=self._dummy_bind)
        self.assertIsChild(widget, self.window)
        widget.invoke()
        self.assertHasBeenInvoked()

        parent = tk.Toplevel()
        child = move_widget(widget, parent)
        self.assertIsChild(child, parent)
        widget.invoke()
        self.assertHasBeenInvoked()

    def test_move_widget_with_bound_method_on_parent(self):
        tl1 = tk.Toplevel(self.window)
        tl2 = tk.Toplevel(self.window)
        tl1._dummy_bind = self._dummy_bind

        button = ttk.Button(tl1)
        button.bind("<Enter>", tl1._dummy_bind)
        button.event_generate("<Enter>")
        self.assertHasBeenInvoked()

        button = move_widget(button, tl2)
        button.event_generate("<Enter>")
        self.assertHasBeenInvoked()

    def test_move_widget_with_command_method_on_parent(self):
        tl1 = tk.Toplevel(self.window)
        tl2 = tk.Toplevel(self.window)
        tl1._dummy_bind = self._dummy_bind

        button = ttk.Button(tl1, command=tl1._dummy_bind)
        button.invoke()
        self.assertHasBeenInvoked()

        button = move_widget(button, tl2)
        button.invoke()
        self.assertHasBeenInvoked()

    def test_move_widget_with_binding_on_parent(self):
        widget = ttk.Label(self.window)
        widget._dummy_bind = self._dummy_bind
        self.window.bind("<Enter>", widget._dummy_bind)

        self.window.event_generate("<Enter>")
        self.assertHasBeenInvoked()

        move_widget(widget, tk.Toplevel())
        self.window.event_generate("<Enter>")
        self.assertHasBeenInvoked()

    def test_parse_geometry(self):
        g = parse_geometry('1x1+1+1')
        self.assertEqual(g, (1, 1, 1, 1))
        g = parse_geometry('1x1-1-1')
        self.assertEqual(g, (-1, -1, 1, 1))

    def test_coordinates_in_box(self):
        with self.assertRaises(ValueError):
            coords_in_box((1,), (1, 1, 3, 3))
        
        with self.assertRaises(ValueError):
            coords_in_box((1, 1), (1, 1, 3, 3, 4))

        self.assertTrue(coords_in_box((1, 1), (0, 0, 2, 2)))
        self.assertFalse(coords_in_box((1, 1), (1, 1, 2, 2), include_edges=False))
        self.assertTrue(coords_in_box((0, 0), (-1, -1, 1, 1), bbox_is_x1y1x2y2=True))
