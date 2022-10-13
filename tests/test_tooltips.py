"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
from unittest import TestCase
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets.hook import is_hooked
from ttkwidgets import tooltips


class TestTooltipsModule(TestCase):
    def test_hook_exists(self):
        self.assertTrue(is_hooked(tooltips.OPTIONS))

    def test_hook_works(self):
        tooltip = "This is a great tooltip."
        widget = ttk.Button(text="Hello World", tooltip=tooltip)

        # Check the holder existence
        holder = getattr(widget, tooltips.NAME.lower(), None)
        self.assertIsNotNone(holder)
        self.assertTrue(hasattr(holder, "tooltip_widget"))

        # Check that the tooltip widget exists and is created with the given value
        tooltip_widget = getattr(holder, "tooltip_widget", None)
        self.assertIsNotNone(tooltip_widget)
        self.assertEqual(tooltip_widget["text"], tooltip)

        # Check that the text is updated when configuring the widget only
        tooltip = "This is another great tooltip."
        widget["tooltip"] = tooltip
        self.assertEqual(tooltip_widget["text"], tooltip)
        self.assertEqual(widget["tooltip"], tooltip)

        # Check that the tooltip is destroyed when configured with None
        widget["tooltip"] = None
        tooltip_widget = getattr(holder, "tooltip_widget")
        self.assertIsNone(tooltip_widget)

        # Check that the tooltip is updated when its options are changed
        widget.configure(tooltip_options={"headertext": "header"}, tooltip=tooltip)
        tooltip_widget = getattr(holder, "tooltip_widget", None)
        self.assertIsNotNone(tooltip_widget)
        self.assertEqual(tooltip_widget["headertext"], "header")
        self.assertEqual(tooltip_widget["text"], tooltip)
        self.assertEqual(widget["tooltip"], tooltip)
        self.assertEqual(widget["tooltip_options"], {"headertext": "header"})
