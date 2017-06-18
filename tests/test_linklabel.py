# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import LinkLabel
import unittest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestLinkLabel(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()
        self.window.update()

    def tearDown(self):
        self.window.update()
        self.window.destroy()

    def test_linklabel_init(self):
        label = LinkLabel(self.window, link="google.com", text="Visit Google")
        label.pack()
        self.window.update()

    def test_linklabel_events(self):
        label = LinkLabel(self.window, link="google.com", text="Visit Google")
        label.pack()
        self.window.update()
        label._on_enter()
        self.window.update()
        label._on_leave()
        self.window.update()
        label.open_link()
        self.window.update()
