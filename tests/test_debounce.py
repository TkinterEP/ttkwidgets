# Copyright (c) Dogeek 2019
# For license see LICENSE

from ttkwidgets import DebouncedFrame
from tests import BaseWidgetTest
import tkinter as tk


class TestDebouncedFrame(BaseWidgetTest):
    def test_calendar_init(self):
        widget = DebouncedFrame(self.window)
        widget.pack()
        self.window.update()

    def test_debouncer_bind_instance(self):
        widget = DebouncedFrame(self.window)
        widget.pack()
        widget.bind("<KeyPress-i>", lambda evt: None, True)
        widget.bind("<KeyRelease-i>", lambda evt: None, True)

    def test_debouncer_bind_class(self):
        widget = DebouncedFrame(self.window)
        widget.pack()
        widget.bind_class("<KeyPress-c>", lambda evt: None, True)
        widget.bind_class("<KeyRelease-c>", lambda evt: None, True)

    def test_debouncer_bind_all(self):
        widget = DebouncedFrame(self.window)
        widget.pack()
        widget.bind_all("<KeyPress-a>", lambda evt: None, True)
        widget.bind_all("<KeyRelease-a>", lambda evt: None, True)

    def test_debouncedframe_kw(self):
        widget = DebouncedFrame(self.window, width=100, height=100)
        widget.pack()
