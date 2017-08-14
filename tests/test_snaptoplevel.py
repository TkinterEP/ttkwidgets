# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import SnapToplevel
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestSnapToplevel(BaseWidgetTest):
    def test_snaptoplevel_init(self):
        snap = SnapToplevel(self.window)

    def test_snaptoplevel_kwargs(self):
        snap = SnapToplevel(self.window, border=50, anchor=tk.LEFT, offset_sides=10, offset_top=30, allow_change=True,
                            resizable=True)

        def configure_function(event):
            assert isinstance(event.widget, tk.Toplevel) or isinstance(event.widget, tk.Tk)

        snap = SnapToplevel(self.window, configure_function=configure_function)
        self.window.update()

        snap.configure(border=50)
        snap.config(border=50, anchor=tk.LEFT, offset_sides=10, offset_top=30, allow_change=True, resizable=True,
                    configure_function=None, locked=False, width=300)

        self.assertEqual(snap.cget("border"), 50)
        self.assertEqual(snap.cget("anchor"), tk.LEFT)
        self.assertEqual(snap.cget("offset_sides"), 10)
        self.assertEqual(snap.cget("offset_top"), 30)
        self.assertEqual(snap.cget("allow_change"), True)
        self.assertEqual(snap.cget("resizable"), True)
        self.assertEqual(snap.cget("configure_function"), None)
        self.assertEqual(snap.cget("locked"), False)
        self.assertEqual(snap.cget("width"), 300)

    def test_snaptoplevel_kwargs_raise(self):
        self.assertRaises(ValueError, lambda: SnapToplevel(tk.Label()))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, anchor=tk.W))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, border="50"))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, offset_sides="5"))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, offset_top="5"))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, allow_change="True"))
        self.assertRaises(ValueError, lambda: SnapToplevel(self.window, resizable="False"))

    def test_snaptoplevel_get_offset_values(self):
        snap = SnapToplevel(self.window)
        sides, top = snap.get_offset_values()
        self.assertIsInstance(sides, int)
        self.assertIsInstance(top, int)
        self.assertGreaterEqual(sides, 0)
        self.assertGreaterEqual(top, 0)

    def test_snaptoplevel_get_new_geometry_master(self):
        snap = SnapToplevel(self.window)
        results = snap.get_new_geometry_master()
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 4)
        for value in results:
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)

    def test_snaptoplevel_set_geometry_master(self):
        for anchor in (tk.RIGHT, tk.LEFT, tk.TOP, tk.BOTTOM):
            window = tk.Toplevel()
            snap = SnapToplevel(window, anchor=anchor)
            snap.set_geometry_master()

    def test_snaptoplevel_get_points_sides_for_window(self):
        self.window.update()
        results = SnapToplevel.get_points_sides_for_window(self.window)
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 4)
        for value in results:
            self.assertIsInstance(value, tuple)
            self.assertEqual(len(value), 2)
            for number in value:
                self.assertIsInstance(number, int)

    def test_get_distance_between_points(self):
        distance = SnapToplevel.get_distance_between_points((0, 0), (0, 0))
        self.assertEqual(distance, 0)
        distance = SnapToplevel.get_distance_between_points((0, 0), (0, 4))
        self.assertEqual(distance, 4)

    def test_snaptoplevel_changestate_callbacks(self):
        snap = SnapToplevel(self.window)
        self.window.update()
        snap.minimize(None)
        self.window.update()
        snap.deminimize(None)
        self.window.update()

    def test_snaptoplevel_snap(self):
        snap = SnapToplevel(self.window)
        self.window.update()
        snap._snap()

    def test_snaptoplevel_get_distance_to_master(self):
        results = SnapToplevel(self.window).get_distance_to_master()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 4)
        self.assertTrue(tk.RIGHT in results)
        self.assertTrue(tk.LEFT in results)
        self.assertTrue(tk.TOP in results)
        self.assertTrue(tk.BOTTOM in results)
        for value in results.values():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)

    def test_snaptoplevel_set_geometry_self_not_allow_change(self):
        snap = SnapToplevel(self.window, allow_change=False)
        self.window.update()
        snap.set_geometry_self()

    def test_snaptoplevel_set_geometry_self_allow_change(self):
        snap = SnapToplevel(self.window, allow_change=True)
        self.window.update()
        snap.set_geometry_self()
