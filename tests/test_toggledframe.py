# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import ToggledFrame
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestToggledFrame(BaseWidgetTest):
    def test_toggledframe_init(self):
        frame = ToggledFrame(self.window)
        frame.pack()
        self.window.update()

    def test_toggledframe_open(self):
        frame = ToggledFrame(self.window)
        frame.pack()
        frame.toggle()
        self.assertTrue(frame._open)

    def test_toggledframe_open_close(self):
        frame = ToggledFrame(self.window)
        frame.pack()
        frame.toggle()
        self.assertTrue(frame._open)
        frame.toggle()
        self.assertFalse(frame._open)
