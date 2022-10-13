# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import ScrolledFrame
from tests import BaseWidgetTest
import tkinter as tk


class TestScrolledFrame(BaseWidgetTest):
    def test_scrollframe_init(self):
        frame = ScrolledFrame(self.window)
        frame.pack()
        self.window.update()
        self.assertFalse(frame._scrollbar.winfo_ismapped())
        
        frame.destroy()
        frame = ScrolledFrame(self.window, autohidescrollbar=False)
        frame.pack()
        self.window.update()
        self.assertTrue(frame._scrollbar.winfo_ismapped())

    def test_scrollframe_methods(self):
        frame = ScrolledFrame(self.window)
        frame.pack(fill='both', expand=True)
        self.window.update()
        frame.resize_canvas(200, 200)
        self.window.update()
        self.window.geometry('300x100')
        self.window.update()
        tk.Button(frame.interior, text='Test').pack()
