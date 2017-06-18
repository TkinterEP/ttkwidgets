# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import Calendar
from tests import BaseWidgetTest
import calendar
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestCalendar(BaseWidgetTest):
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
