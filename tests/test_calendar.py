# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import Calendar
import unittest
import calendar
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.window = tk.Tk()

    def test_calendar_init(self):
        widget = Calendar(self.window)
        widget.pack()
        self.window.update()

    def test_calendar_buttons_functions(self):
        widget = Calendar(self.window)
        widget.pack()
        widget._prev_month()
        widget._next_month()

    def test_calendar_kw(self):
        widget = Calendar(self.window, firstweekday=calendar.SUNDAY, year=2016, month=12)
        widget.pack()

    def tearDown(self):
        self.window.destroy()
