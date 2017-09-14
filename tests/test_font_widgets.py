# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.font import FontChooser, FontSelectFrame
from tests import BaseWidgetTest
try:
    import Tkinter as tk
    import tkFont as font
except ImportError:
    import tkinter as tk
    from tkinter import font
import os


if "TRAVIS" not in os.environ:
    class TestFontChooser(BaseWidgetTest):
        def test_fontchooser_init(self):
            chooser = FontChooser(self.window)
            self.window.update()
            chooser._close()

        def test_fontchooser_noselection(self):
            chooser = FontChooser(self.window)
            self.window.update()
            results = chooser.font
            self.assertEqual(results, (None, None))

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
            chooser._on_family('')
            self.window.update()
            results = chooser.font
            self.assertIsNone(results[0])

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
            self.assertTrue("bold" in results[0])

            chooser._on_properties((True, True, True, True))
            self.window.update()
            results = chooser.font
            self.assertEqual(results[0][2:], ('bold', 'italic',
                                              'underline', 'overstrike'))

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

    class TestFontSelectFrame(BaseWidgetTest):
        def test_fontselectframe_init(self):
            frame = FontSelectFrame(self.window)
            frame.pack()
            self.window.update()

        def test_fontselectframe_family(self):
            frame = FontSelectFrame(self.window)
            frame.pack()
            self.window.update()
            frame._family_dropdown.set(font.families()[1])
            self.window.update()
            frame._on_family(frame._family_dropdown.get())
            results = frame.font
            self.assertIsInstance(results, tuple)
            self.assertEqual(len(results), 2)
            self.assertIsInstance(results[0], tuple)
            self.assertEqual(len(results[0]), 2)
            self.assertIsInstance(results[1], font.Font)

            frame._on_size(20)
            frame._on_family('Arial')
            frame._on_properties((True, True, True, True))
            self.window.update()
            results = frame.font
            self.assertEqual(results[0], ('Arial', 20, 'bold', 'italic',
                                          'underline', 'overstrike'))
