# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import AutoScrollbar
from tests import BaseWidgetTest


class TestAutoScrollbar(BaseWidgetTest):
    def test_autoscrollbar_init(self):
        AutoScrollbar(self.window)
        self.window.update()

    def test_autoscrollbar_methods(self):
        scroll = AutoScrollbar(self.window, orient='vertical')
        # pack layout
        scroll.pack(side='right', fill='y')
        self.window.update()
        scroll.set(-0.1, 1.1)
        self.window.update()
        self.assertFalse(scroll.winfo_ismapped())
        scroll.set(0.1, 0.8)
        self.window.update()
        self.window.update()
        self.assertTrue(scroll.winfo_ismapped())
        scroll.pack_forget()
        self.window.update()
        # place layout
        scroll.place(anchor='ne', relx=1, rely=0, relheight=1)
        self.window.update()
        scroll.set(-0.1, 1.1)
        self.window.update()
        self.assertFalse(scroll.winfo_ismapped())
        scroll.set(0.1, 0.8)
        self.window.update()
        self.window.update()
        self.assertTrue(scroll.winfo_ismapped())
        scroll.place_forget()
        self.window.update()
        # grid layout
        scroll.grid(row=0, column=1, sticky='ns')
        self.window.update()
        scroll.set(-0.1, 1.1)
        self.window.update()
        self.assertFalse(scroll.winfo_ismapped())
        scroll.set(0.1, 0.8)
        self.window.update()
        self.window.update()
        self.assertTrue(scroll.winfo_ismapped())
