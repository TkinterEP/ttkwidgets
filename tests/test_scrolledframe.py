# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import ScrolledFrame
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestScrolledFrame(BaseWidgetTest):
    def test_scrollframe_init(self):
        frame = ScrolledFrame(self.window)
        frame.pack()
        self.window.update()
