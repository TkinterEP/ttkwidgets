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
        self.assertEqual(scale.cget_entry('width'), 10)
        scale._entry.delete(0, tk.END)
        scale._entry.insert(0, "5")
        scale._on_entry(None)
        self.assertEqual(scale._variable.get(), 5)
        scale._entry.insert(0, "a")
        scale._on_entry(None)
        self.assertEqual(scale._variable.get(), 5)
        scale._entry.insert(0, "")
        scale._on_entry(None)
        self.assertEqual(scale._variable.get(), 5)

    def test_scaleentry_scale(self):
        scale = ScaleEntry(self.window)
        scale.pack()
        self.window.update()
        scale.config_scale(length=100)
        self.window.update()
        self.assertEqual(scale.cget_scale('length'), 100)
        try:
            info = scale._scale.grid_info()
        except TypeError:
            # bug in some tkinter versions
            res = str(scale.tk.call('grid', 'info', scale._scale._w)).split("-")
            info = {}
            for i in res:
                if i:
                    key, val = i.strip().split()
                    info[key] = val
        self.assertEqual(info['sticky'], 'ew')
        scale.config_scale(orient='vertical')
        self.window.update()
        try:
            info = scale._scale.grid_info()
        except TypeError:
            # bug in some tkinter versions
            res = str(scale.tk.call('grid', 'info', scale._scale._w)).split("-")
            info = {}
            for i in res:
                if i:
                    key, val = i.strip().split()
                    info[key] = val
        self.assertEqual(info['sticky'], 'ns')
        scale._variable.set(20)
        scale._on_scale(None)
        self.assertEqual(scale._variable.get(), 20)

    def test_scaleentry_limitedintvar(self):
        var = ScaleEntry.LimitedIntVar(5, 55)
        var.set(60)
        self.assertEqual(var.get(), 55)
        var.set(0)
        self.assertEqual(var.get(), 5)
        var.configure(low=10)
        self.assertEqual(var._low, 10)
        self.assertEqual(var.get(), 10)
        var.set(54)
        var.configure(high=20)
        self.assertEqual(var._high, 20)
        self.assertEqual(var.get(), 20)
        self.assertRaises(TypeError, lambda: var.set('a'))

    def test_scaleentry_property(self):
        scale = ScaleEntry(from_=50)
        self.assertEqual(scale.value, 50)

    def test_scaleentry_methods(self):
        scale = ScaleEntry(self.window, scalewidth=100, entrywidth=4, from_=-10,
                           to=10, orient=tk.VERTICAL, compound=tk.TOP,
                           entryscalepad=10)
        scale.pack()
        self.window.update()
        keys = ['borderwidth', 'padding', 'relief', 'width', 'height',
                'takefocus', 'cursor', 'style', 'class', 'scalewidth', 'orient',
                'entrywidth', 'from', 'to', 'compound', 'entryscalepad']
        keys.sort()
        self.assertEqual(scale.keys(), keys)
        self.assertEqual(scale['orient'], tk.VERTICAL)
        self.assertEqual(scale['scalewidth'], 100)
        self.assertEqual(scale['entrywidth'], 4)
        self.assertEqual(scale['from'], -10)
        self.assertEqual(scale['to'], 10)
        self.assertEqual(scale['compound'], tk.TOP)
        self.assertEqual(scale['entryscalepad'], 10)

        scale.configure({'to': 50, 'compound': tk.RIGHT}, padding=2, from_=20,
                        orient='horizontal', entryscalepad=0)
        scale['entrywidth'] = 5
        self.window.update()
        self.assertEqual(scale.cget('compound'), tk.RIGHT)
        self.assertEqual(str(scale.cget('padding')[0]), '2')
        self.assertEqual(scale.cget('entryscalepad'), 0)
        self.assertEqual(scale.cget('entrywidth'), 5)
        self.assertEqual(str(scale.cget_scale('orient')), 'horizontal')
        self.assertEqual(scale.cget_scale('from'), 20)
        self.assertEqual(scale.cget_scale('to'), 50)
        self.assertEqual(scale._variable._low, 20)
        self.assertEqual(scale._variable._high, 50)
        scale.config({'scalewidth': 50, 'from': -10}, compound=tk.BOTTOM)
        self.assertEqual(scale.cget_scale('from'), -10)
        self.assertEqual(scale.cget('scalewidth'), 50)
        self.assertEqual(scale.cget_scale('length'), 50)

        with self.assertRaises(ValueError):
            scale['compound'] = 'topp'

        with self.assertRaises(ValueError):
            scale['entryscalepad'] = 'a'

    def test_scaleentry_kwargs(self):
        self.assertRaises(ValueError, lambda: ScaleEntry(compound="something!"))
        self.assertRaises(TypeError, lambda: ScaleEntry(self.window, entryscalepad='a'))

