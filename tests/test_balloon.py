# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import Balloon
from tests import BaseWidgetTest

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestBalloon(BaseWidgetTest):
    def test_balloon_init(self):
        balloon = Balloon(self.window)
        self.window.update()

    def test_balloon_kwargs(self):
        balloon = Balloon(self.window, headertext="Help", text="This is a test for the Balloon widget.", width=300,
                          timeout=2, background="white")
        self.assertEqual(balloon.cget("headertext"), "Help")
        self.assertEqual(balloon.cget("text"), "This is a test for the Balloon widget.")
        self.assertEqual(balloon.cget("width"), 300)
        self.assertEqual(balloon.cget("timeout"), 2)
        self.assertEqual(balloon.cget("background"), "white")

        balloon.config(headertext="New Help", text="This is another test for the Balloon widget.", width=400,
                       timeout=3, background="black")
        self.assertEqual(balloon.cget("headertext"), "New Help")
        self.assertEqual(balloon.cget("text"), "This is another test for the Balloon widget.")
        self.assertEqual(balloon.cget("width"), 400)
        self.assertEqual(balloon.cget("timeout"), 3)
        self.assertEqual(balloon.cget("background"), "black")

    def test_balloon_show(self):
        balloon = Balloon(self.window)
        self.window.update()
        balloon.show()
        self.window.update()
        balloon._on_leave(None)
        self.window.update()
        self.assertIs(balloon._toplevel, None)

