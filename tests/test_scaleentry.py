# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ScaleEntry
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestScaleEntry(BaseWidgetTest):
    def test_scaleentry_init(self):
        scale = ScaleEntry(self.window)
        scale.pack()
        self.window.update()

    def test_scaleentry_entry(self):
        scale = ScaleEntry(self.window, from_=0, to=50)
        scale.pack()
        self.window.update()
        scale.config_entry(width=10)
        self.window.update()
        scale._entry.delete(0, tk.END)
        scale._entry.insert(0, "5")
        scale._on_entry(None)
        self.assertEqual(scale._variable.get(), 5)

    def test_scaleentry_scale(self):
        scale = ScaleEntry(self.window)
        scale.pack()
        self.window.update()
        scale.config_scale(length=100)
        self.window.update()
        scale._variable.set(20)
        scale._on_scale(None)
        self.assertEqual(scale._variable.get(), 20)

    def test_scaleentry_limitedintvar(self):
        var = ScaleEntry.LimitedIntVar(5, 55)
        var.set(60)
        self.assertEqual(var.get(), 55)
        var.set(0)
        self.assertEqual(var.get(), 5)

    def test_scaleentry_property(self):
        scale = ScaleEntry(from_=50)
        self.assertEqual(scale.value, 50)

    def test_scaleentry_kwargs(self):
        self.assertRaises(ValueError, lambda: ScaleEntry(compound="something!"))


