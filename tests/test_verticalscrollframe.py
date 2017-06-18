# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ScrolledFrame
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestVerticalScrollFrame(BaseWidgetTest):
    def test_vertical_scroll_frame_init(self):
        frame = ScrolledFrame(self.window)
        frame.pack()
        self.window.update()
