# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import LinkLabel
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestLinkLabel(BaseWidgetTest):
    def test_linklabel_init(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()
        self.window.update()

    def test_linklabel_events(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()
        self.window.update()
        label._on_enter()
        self.window.update()
        label._on_leave()
        self.window.update()
        label.open_link()
        self.window.update()

    def test_linklabel_config(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()
        self.window.update()
        label.keys()
        self.window.update()
        label.configure(link="www.wikipedia.fr")
        self.window.update()
        label.cget("hover_color")
        self.window.update()
        value = label["normal_color"]
        self.window.update()
        label["clicked_color"] = "purple"
        self.window.update()
