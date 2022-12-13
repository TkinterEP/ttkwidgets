# Copyright (c) RedFantom 2017
# For license see LICENSE
import tkinter as tk

from tests import BaseWidgetTest
from ttkwidgets import LinkLabel


class TestLinkLabel(BaseWidgetTest):
    def test_linklabel_init(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()

    def test_linklabel_events(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()

        self.window.update()
        label._on_enter()
        self.window.update()
        label._on_leave()
        self.window.update()
        label.open_link()

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
        label.config(cursor="hand1")
        self.window.update()
        assert label.cget("cursor") == "hand1"

    def test_linklabel_cget(self):
        label = LinkLabel(self.window, link="www.google.com", text="Visit Google")
        label.pack()

        assert label.cget("link") == label._link
        assert label.cget("normal_color") == label._normal_color
        assert label.cget("hover_color") == label._hover_color
        assert label.cget("clicked_color") == label._clicked_color
        assert label.cget("text") == "Visit Google"
