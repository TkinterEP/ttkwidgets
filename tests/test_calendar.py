# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import Calendar
import unittest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()

    def test_calendar_init(self):
        calendar = Calendar(self.window)
        calendar.pack()
        self.window.update()

    def tearDown(self):
        self.window.destroy()
