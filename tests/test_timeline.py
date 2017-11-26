# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import TimeLine
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestTimeLine(BaseWidgetTest):
    def test_initialization(self):
        TimeLine(self.window)

    def test_kwargs_errors(self):
        timeline = TimeLine(self.window)
        for option in timeline.options:
            self.assertRaises((TypeError, ValueError), lambda: timeline.config(**{option: None}))

    def test_categories(self):
        TimeLine(self.window, categories=("category",))
        TimeLine(self.window, categories={"category": {"text": "Category"}})
        self.assertRaises(TypeError, lambda: TimeLine(self.window, categories=["category",]))

    def test_marker_creation(self):
        timeline = TimeLine(self.window, categories={"category": {"foreground": "cyan", "text": "Category"}})
        iid = timeline.create_marker("category", 1.0, 2.0)
        self.assertTrue(iid in timeline.markers)
