# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import TickScale
from tests import BaseWidgetTest
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class TestTickScale(BaseWidgetTest):
    def test_tickscale_init(self):
        TickScale(self.window, orient='vertical', style='my.Vertical.TScale',
                  tickinterval=0.2, from_=-1, to=1, showvalue=True,
                  digits=2, length=400, cursor='watch').pack()
        self.window.update()
        TickScale(self.window, orient='horizontal', from_=0, to=10,
                  tickinterval=0, showvalue=False,
                  command=lambda value: print(value)).pack()
        self.window.update()

    def test_tickscale_methods(self):
        scale = TickScale(self.window, from_=0, to=10, orient='horizontal')
        scale.pack()
        self.window.update()
        self.assertEqual(scale.cget('digits'), 0)
        self.assertEqual(scale['tickinterval'], 0)
        self.assertTrue(scale.cget('showvalue'))
        self.assertEqual(scale['from'], 0)
        self.assertEqual(scale.cget('to'), 10)
        keys = ['command',
                'variable',
                'orient',
                'from',
                'to',
                'value',
                'length',
                'takefocus',
                'cursor',
                'style',
                'class',
                'tickinterval',
                'showvalue',
                'digits']
        self.assertEqual(sorted(scale.keys()), sorted(keys))

        scale.config(from_=-1)
        self.window.update()
        self.assertEqual(scale['from'], -1)

        scale.configure({'to': 20, 'tickinterval': 5, 'digits': 1})
        self.window.update()
        self.assertEqual(scale['to'], 20)
        self.assertEqual(scale['digits'], 1)
        self.assertEqual(scale['tickinterval'], 5)

        scale['orient'] = 'vertical'
        self.window.update()

        style = ttk.Style(self.window)
        scale.configure(style='my.Vertical.TScale')
        self.window.update()
        style.configure('my.Vertical.TScale', font='TkDefaultFont 20 italic',
                        sliderlength=50)

        scale.x = 0

        def cmd(value):
            scale.x = 2 * float(value)

        scale.configure(command=cmd)
        self.window.update()
        scale.set(10)
        self.window.update()
        self.assertEqual(scale.x, 20)
        self.assertEqual(scale.label.cget('text'), '10.0')

        scale['showvalue'] = False
        self.window.update()
        self.assertEqual(scale.label.place_info(), {})

        scale['orient'] = 'horizontal'
        self.window.update()
        scale['style'] = ''
        scale['showvalue'] = True
        self.window.update()
        scale['length'] = 200
        scale['digits'] = 3
        style.configure('Horizontal.TScale', font='TkDefaultFont 20 italic',
                        sliderlength=10)
        self.window.update()
        scale.set(0)
        self.window.update()
        scale.set(20)
        self.window.update()
