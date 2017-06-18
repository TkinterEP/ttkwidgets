# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ScrolledFrame
import unittest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestVerticalScrollFrame(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()

    def tearDown(self):
        self.window.destroy()

    def test_vertical_scroll_frame_init(self):
        frame = ScrolledFrame(self.window)
        frame.pack()
        self.window.update()
