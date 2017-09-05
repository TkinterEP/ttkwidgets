# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.frames import Balloon
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from time import sleep


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
        self.assertEqual(balloon["headertext"], "New Help")
        self.assertEqual(balloon["text"], "This is another test for the Balloon widget.")
        self.assertEqual(balloon["width"], 400)
        self.assertEqual(balloon["timeout"], 3)
        self.assertEqual(balloon["background"], "black")

        # Keys for the Frame widget
        balloon.configure(height=40)
        self.assertEqual(balloon.cget("height"), 40)

        balloon['height'] = 50
        self.assertEqual(balloon["height"], 50)

        for key in ["headertext", "text", "width", "timeout", "background"]:
            self.assertIn(key, balloon.keys())

    def test_balloon_show(self):
        balloon = Balloon(self.window)
        self.window.update()
        balloon.show()
        self.window.update()
        balloon.config(text="Something else")
        self.window.update()
        self.assertEqual(balloon.cget("text"), "Something else")
        balloon._on_leave(None)
        self.window.update()
        self.assertIs(balloon._toplevel, None)

    def test_balloon_events(self):
        balloon = Balloon(self.window, timeout=0.2)
        balloon._on_enter(None)
        self.window.update()
        sleep(0.3)
        self.window.update()
        self.assertIsInstance(balloon._toplevel, tk.Toplevel)
        balloon._on_leave(None)
        self.assertIs(balloon._toplevel, None)

    def test_balloon_events_noshow(self):
        balloon = Balloon(self.window)
        balloon._on_enter(None)
        balloon._on_leave(None)

