# Copyright (c) rdbende 2021
# For license see LICENSE

from ttkwidgets import NumberEntry
from tests import BaseWidgetTest
import tkinter as tk


class TestNumberEntry(BaseWidgetTest):
    def test_numberentry_init(self):
        entry = NumberEntry(self.window, expressions=True, roundto=4)
        entry.pack()
        self.window.update()

    def test_numberentry_events(self):
        entry = NumberEntry(self.window, expressions=True, roundto=4)
        entry.pack()
        self.window.update()
        entry.insert(0, "1+2-3*4/5**6")
        self.window.update()
        entry._check()
        self.window.update()
        entry._replace("1+2-3*4/5**6")
        self.window.update()
        entry._eval()
        self.window.update()

    def test_numberentry_config(self):
        entry = NumberEntry(self.window, expressions=True, roundto=4)
        entry.pack()
        self.window.update()
        entry.keys()
        self.window.update()
        entry.configure(expressions=False, roundto=0)
        self.window.update()
        entry.cget("expressions")
        self.window.update()
        value = entry["roundto"]
        self.window.update()
        entry["roundto"] = 4
        self.window.update()
