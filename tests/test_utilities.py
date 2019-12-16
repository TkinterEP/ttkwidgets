# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets.utilities import move_widget, parse_geometry, coords_in_box
from tests import BaseWidgetTest
import tkinter as tk
from tkinter import ttk


class TestUtilities(BaseWidgetTest):
    def assertGeometryInfoEquals(self, info1, info2):
        info1.pop("in", None)
        info2.pop("in", None)
        self.assertEquals(info1, info2)

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
        label.pack(side=tk.LEFT)
        info = label.pack_info()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl, preserve_geometry=True)
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.pack_slaves())
        self.assertNotIn(label, self.window.pack_slaves())
        self.assertGeometryInfoEquals(info, label.pack_info())

    def test_move_widget_grid(self):
        label = ttk.Label(self.window)
        label.grid(row=1, column=1)
        info = label.grid_info()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl, preserve_geometry=True)
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.grid_slaves(row=1, column=1))
        self.assertNotIn(label, self.window.grid_slaves(row=1, column=1))
        self.assertGeometryInfoEquals(info, label.grid_info())

    def test_move_widget_place(self):
        label = ttk.Label(self.window)
        label.place(x=0, y=10)
        info = label.place_info()
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl, preserve_geometry=True)
        self.assertIsChild(label, tl)
        self.assertIn(label, tl.place_slaves())
        self.assertNotIn(label, self.window.place_slaves())
        self.assertGeometryInfoEquals(info, label.place_info())

    def test_move_widget_none(self):
        label = ttk.Label(self.window)
        self.assertFalse(label.place_info() is True)
        self.assertFalse(label.grid_info() is True)
        self.assertRaises(tk.TclError, label.pack_info)
        tl = tk.Toplevel(self.window)
        label = move_widget(label, tl, preserve_geometry=True)
        self.assertFalse(label.place_info() is True)
        self.assertFalse(label.grid_info() is True)
        self.assertRaises(tk.TclError, label.pack_info)

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

    def test_move_widget_with_children_pack(self):
        frame = ttk.Frame(self.window)
        label = ttk.Label(frame)
        parent = tk.Toplevel()
        label.pack(side=tk.BOTTOM)
        info = label.pack_info()
        frame.pack(expand=True)

        frame = move_widget(frame, parent)
        self.assertTrue(len(frame.pack_slaves()) == 1)
        label2 = frame.nametowidget(frame.pack_slaves()[0])
        self.assertTrue(label is not label2)

        self.assertGeometryInfoEquals(info, label2.pack_info())
        self.assertRaises(tk.TclError, label.pack_info)
        self.assertRaises(tk.TclError, frame.pack_info)  # Frame is not packed
        self.assertIn(label2, frame.pack_slaves())

    def test_move_widget_with_children_grid(self):
        frame = ttk.Frame(self.window)
        label = ttk.Label(frame)
        parent = tk.Toplevel()
        label.grid(row=1, column=1)
        info = label.grid_info()
        frame.grid(row=1, column=1)

        frame = move_widget(frame, parent)
        self.assertTrue(len(frame.grid_slaves()) == 1)
        label2 = frame.nametowidget(frame.grid_slaves()[0])
        self.assertTrue(label is not label2)

        self.assertGeometryInfoEquals(info, label2.grid_info())
        self.assertRaises(tk.TclError, label.grid_info)
        self.assertTrue(len(frame.grid_info()) == 0)  # Frame is not in grid
        self.assertIn(label2, frame.grid_slaves())

    def test_move_widget_with_children_place(self):
        frame = ttk.Frame(self.window)
        label = ttk.Label(frame)
        parent = tk.Toplevel()
        label.place(x=53, y=13)
        info = label.place_info()
        frame.place(x=100, y=10)

        frame = move_widget(frame, parent)
        self.assertTrue(len(frame.place_slaves()) == 1)
        label2 = frame.nametowidget(frame.place_slaves()[0])
        self.assertTrue(label is not label2)

        self.assertGeometryInfoEquals(info, label2.place_info())
        self.assertRaises(tk.TclError, label.place_info)
        self.assertTrue(len(frame.place_info()) == 0)
        self.assertIn(label2, frame.place_slaves())

    def test_move_widget_to_new_tk(self):
        label = tk.Label(self.window)
        window = tk.Tk()
        self.assertRaises(RuntimeError, move_widget, label, window)

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
        self.assertTrue(coords_in_box((0, 0), (-1, -1, 1, 1), bbox_is_x1y1x02y2=True))
