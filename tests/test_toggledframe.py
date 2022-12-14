# Copyright (c) RedFantom 2017
# For license see LICENSE
import tkinter as tk

from tests import BaseWidgetTest
from ttkwidgets.frames import ToggledFrame


class TestToggledFrame(BaseWidgetTest):
    def test_toggledframe_init(self):
        frame = ToggledFrame(self.window)
        frame.pack()

    def test_toggledframe_open(self):
        frame = ToggledFrame(self.window)
        frame.pack()
        self.window.update()
        frame.toggle()
        assert frame.opened

    def test_toggledframe_open_close(self):
        frame = ToggledFrame(self.window)
        frame.pack()
        self.window.update()
        frame.toggle()
        self.window.update()
        assert frame.opened
        frame.close()
        self.window.update()
        assert not frame.opened
        frame.open()
        self.window.update()
        assert frame.opened
        frame._button.invoke()
        self.window.update()
        assert not frame.opened
