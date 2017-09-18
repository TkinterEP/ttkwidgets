# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import AutoHideScrollbar
from tests import BaseWidgetTest


class TestAutoHideScrollbar(BaseWidgetTest):
    def test_autohidescrollbar_init(self):
        AutoHideScrollbar(self.window)
        self.window.update()

    def test_autohidescrollbar_methods(self):
        scroll = AutoHideScrollbar(self.window, orient='vertical')
        # pack layout
        scroll.pack(side='right', fill='y')
        info = scroll._get_info("pack")
        self.assertEqual(info["side"], "right")
        self.assertEqual(info["fill"], "y")
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
