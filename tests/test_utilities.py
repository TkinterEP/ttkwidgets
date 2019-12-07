# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets.utilities import move_widget, parse_geometry, coords_in_box
from tests import BaseWidgetTest
import tkinter as tk
import tkinter.ttk as ttk


class TestUtilities(BaseWidgetTest):
    def _dummy_bind(self, event):
        pass
    
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
        label = ttk.Label(self.window)
        label.bind('<Enter>', self._dummy_bind)
        label.pack()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.pack()
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())
        self.assertIn('<Enter>', label.bind())

    def test_move_widget_with_binding_on_parent(self):
        self.window.bind('<Enter>', self._dummy_bind)
        label = ttk.Label(self.window)
        label.pack()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl)
        label.pack()
        self.assertTrue(label.winfo_parent() == '.' + tl.winfo_name())
        self.assertIn('<Enter>', tl.bind())
    
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
