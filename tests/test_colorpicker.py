# Copyright (c) Juliette Monsel 2017
# For license see LICENSE
from ttkwidgets import colorpicker as tkc
from tests import BaseWidgetTest
import unittest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    

class TestFunctions(unittest.TestCase):
    def test_round2(self):
        self.assertEqual(tkc.round2(1.1), 1)
        self.assertIsInstance(tkc.round2(1.1), int)

    def test_rgb_to_hsv(self):
        self.assertEqual(tkc.rgb_to_hsv(255, 0, 0), (0, 100, 100))

    def test_hsv_to_rgb(self):
        self.assertEqual(tkc.hsv_to_rgb(0, 100, 100), (255, 0, 0))

    def test_rgb_to_html(self):
        self.assertEqual(tkc.rgb_to_html(255, 255, 255), "#FFFFFF")

    def test_html_to_rgb(self):
        self.assertEqual(tkc.html_to_rgb("#FFFFFF"), (255, 255, 255))

    def test_hue2col(self):
        self.assertEqual(tkc.hue2col(0), (255, 0, 0))

    def test_col2hue(self):
        self.assertEqual(tkc.col2hue(255, 0, 0), 0)


class TestSpinbox(BaseWidgetTest):
    def test_spinbox_init(self):
        spinbox = tkc.Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()

    def test_spinbox_bindings(self):
        spinbox = tkc.Spinbox(self.window, from_=0, to=10)
        spinbox.pack()
        self.window.update()
        spinbox.event_generate('<FocusIn>')
        self.window.update()
        spinbox.event_generate('<FocusOut>')
        self.window.update()


class TestColorSquare(BaseWidgetTest):
    def test_colorsquare_init(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()

    def test_colorsquare_bindings(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()
        cs.event_generate('<1>', x=10, y=50)
        self.window.update()
        cs.event_generate('<B1-Motion>', x=20, y=50)
        self.window.update()
        cs.event_generate('<Configure>')
        self.window.update()

    def test_colorsquare_functions(self):
        cs = tkc.ColorSquare(self.window, hue=60, height=200, width=200)
        cs.pack()
        self.window.update()
        cs._fill()
        self.window.update()
        cs._draw((60, 100, 100))
        self.window.update()
        self.assertEqual(cs.get_hue(), 60)
        self.window.update()
        cs.set_hue(40)
        self.assertEqual(cs.get_hue(), 40)
        self.window.update()
        cs.set_rgb((255, 0, 0))
        self.assertEqual(cs.get_hue(), 0)
        self.window.update()
        cs.set_hsv((0, 100, 100))
        self.assertEqual(cs.get_hue(), 0)
        self.window.update()
        self.assertEqual(cs.get(), ((255, 0, 0), (0, 100, 100), '#FF0000'))
        self.window.update()


class TestGradientBar(BaseWidgetTest):
    def test_gradientbar_init(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()

    def test_gradientbar_bindings(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb.event_generate('<1>', x=10, y=50)
        self.window.update()
        gb.event_generate('<B1-Motion>', x=20, y=50)
        self.window.update()
        gb.event_generate('<Configure>')
        self.window.update()

    def test_gradientbar_functions(self):
        gb = tkc.GradientBar(self.window, hue=20, height=12, width=200)
        gb.pack()
        self.window.update()
        gb._draw_gradient(60)
        self.window.update()
        self.assertEqual(gb.get(), 60)
        self.window.update()
        gb.set(40)
        self.window.update()
        self.assertEqual(gb.get(), 40)


class TestColorPicker(BaseWidgetTest):
    def test_colorpicker_init(self):
        tkc.ColorPicker(self.window, color="sky blue", title='Test')
        self.window.update()

    def test_colorpicker_bindings(self):
        cp = tkc.ColorPicker(self.window, color="sky blue", title='Test')
        self.window.update()
        cp.bar.event_generate("<ButtonRelease-1>", x=10, y=1)
        self.window.update()
        cp.bar.event_generate("<Button-1>", x=10, y=1)
        self.window.update()
        cp.square.event_generate("<ButtonRelease-1>", x=10, y=1)
        self.window.update()
        cp.square.event_generate("<Button-1>", x=10, y=1)
        self.window.update()
        cp.html.event_generate("<FocusOut>")
        self.window.update()
        cp.html.event_generate("<Return>")
        self.window.update()

    def test_colorpicker_functions(self):
        cp = tkc.ColorPicker(self.window, color="sky blue", title='Test')
        self.window.update()
        cp._update_color_rgb()
        self.window.update()
        cp._update_color_hsv()
        self.window.update()
        cp.get_color()
        self.window.update()
        cp.ok()
        self.window.update()

    def test_colorpicker_staticmethods(self):
        cp = tkc.ColorPicker(self.window, color="sky blue", title='Test')
        strvar = tkc.tk.StringVar(cp, -2)
        self.window.update()
        self.assertEqual(cp.get_hue_value(strvar), 0)
        self.assertEqual(cp.get_sv_value(strvar), 0)
        self.assertEqual(cp.get_color_value(strvar), 0)
        self.window.update()
        strvar.set(50)
        self.assertEqual(cp.get_hue_value(strvar), 50)
        self.assertEqual(cp.get_sv_value(strvar), 50)
        self.assertEqual(cp.get_color_value(strvar), 50)
        self.window.update()
        strvar.set(390)
        self.assertEqual(cp.get_hue_value(strvar), 360)
        self.assertEqual(strvar.get(), '360')
        self.assertEqual(cp.get_color_value(strvar), 255)
        self.assertEqual(strvar.get(), '255')
        self.assertEqual(cp.get_sv_value(strvar), 100)
        self.assertEqual(strvar.get(), '100')
        self.window.update()
