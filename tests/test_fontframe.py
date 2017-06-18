# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import FontChooser, FontSelectFrame
from tests import BaseWidgetTest
try:
    import Tkinter as tk
    import tkFont as font
except ImportError:
    import tkinter as tk
    from tkinter import font


class TestFontChooser(BaseWidgetTest):
    def test_fontchooser_init(self):
        chooser = FontChooser(self.window)
        self.window.update()

    def test_fontchooser_selection(self):
        chooser = FontChooser(self.window)
        self.window.update()
        chooser._font_family_list.listbox.selection_set(1)
        chooser._font_family_list._on_click()
        self.window.update()
        results = chooser.font
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)
        self.assertIsInstance(results[1], font.Font)

    def test_fontchooser_properties(self):
        chooser = FontChooser(self.window)
        self.window.update()
        chooser._font_family_list.listbox.selection_set(1)
        chooser._font_family_list._on_click()
        self.window.update()
        chooser._font_properties_frame._bold.set(True)
        chooser._font_properties_frame._on_click()
        self.window.update()
        results = chooser.font
        print(results)
        self.assertTrue("bold" in results[0])

    def test_fontchooser_size(self):
        chooser = FontChooser(self.window)
        self.window.update()
        chooser._font_family_list.listbox.selection_set(1)
        chooser._font_family_list._on_click()
        self.window.update()
        chooser._size_dropdown.delete(0, tk.END)
        chooser._size_dropdown.insert(0, "14")
        self.window.update()
        chooser._size_dropdown._on_click(None)
        self.window.update()
        results = chooser.font
        self.assertEqual(results[0][1], 14)


