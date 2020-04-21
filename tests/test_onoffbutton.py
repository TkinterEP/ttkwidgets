# Copyright (c) 2020 Fredy Ramirez <https://formateli.com>
# For license see LICENSE
from ttkwidgets import OnOffButton
from tests import BaseWidgetTest
import tkinter as tk
from tkinter import ttk


class TestOnOffButton(BaseWidgetTest):
    def test_onoffbutton_init(self):
        onoff = OnOffButton(self.window)
        onoff.pack()
        self.window.update()

    def test_onoffbutton_variable_default(self):
        onoff = OnOffButton(self.window)
        onoff.pack()
        self.window.update()
        variable = onoff.cget('variable')
        self.assertEqual(isinstance(variable, tk.IntVar), True)
        self.assertEqual(variable.get(), 0)
        variable.set(1)
        self.assertEqual(variable.get(), 1)

    def test_onoffbutton_variable_int(self):
        variable = tk.IntVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), False)
        variable.set(1)
        self.assertEqual(variable.get(), True)

    def test_onoffbutton_variable_bool(self):
        variable = tk.BooleanVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), 0)
        variable.set(1)
        self.assertEqual(variable.get(), 1)

    def test_onoffbutton_variable_string(self):
        variable = tk.StringVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), '0')
        variable.set(1)
        self.assertEqual(variable.get(), '1')
        onoff.config(onvalue='ON', offvalue='OFF')
        self.assertEqual(variable.get(), 'ON')
        onoff.invoke()
        self.assertEqual(variable.get(), 'OFF')

    def test_onoffbutton_invoke(self):
        onoff = OnOffButton(self.window, command=self._button_changed)
        onoff.pack()
        self.window.update()
        self.assertEqual(onoff.get(), 0)
        result = onoff.invoke()
        self.assertEqual(onoff, result)
        self.assertEqual(onoff.get(), 1)

    def test_onoffbutton_style(self):
        style = ttk.Style()
        onoff = OnOffButton(self.window)
        onoff.pack()
        self.window.update()
        st = onoff.cget('style')
        self.assertEqual(st, 'OnOffButton')
        opts = {
            'background': style.lookup('TFrame', 'background'),
            'switchcolor': 'white',
            'oncolor': 'green',
            'offcolor': 'red',
            'disabledcolor': 'gray',
            'switchdisabledcolor': '#d9d9d9',
        }
        for key, value in opts.items():
            self.assertEqual(style.lookup(st, key), value)

        # Changing 'OnOffButton' style before init
        style.configure('OnOffButton', background='red', oncolor='yellow')
        onoff2 = OnOffButton(self.window)
        onoff2.pack()
        self.window.update()
        opts = {
            'background': 'red',
            'switchcolor': 'white',
            'oncolor': 'yellow',
            'offcolor': 'red',
            'disabledcolor': 'gray',
            'switchdisabledcolor': '#d9d9d9',
        }
        for key, value in opts.items():
            self.assertEqual(style.lookup(st, key), value)

        # New custom style passing at init
        style.configure('OnOffButtonTest', background='orange', oncolor='brown')
        onoff3 = OnOffButton(self.window, style='OnOffButtonTest')
        onoff3.pack()
        self.window.update()
        st = onoff3.cget('style')
        self.assertEqual(st, 'OnOffButtonTest')
        opts = {
            'background': 'orange',
            'switchcolor': 'white',
            'oncolor': 'brown',
            'offcolor': 'red',
            'disabledcolor': 'gray',
            'switchdisabledcolor': '#d9d9d9',
        }
        for key, value in opts.items():
            self.assertEqual(style.lookup(st, key), value)

        # Passing style to widget config
        style.configure('OnOffButtonTest2', background='purple', oncolor='blue')
        onoff4 = OnOffButton(self.window)
        onoff4.pack()
        self.window.update()
        onoff4.config(style='OnOffButtonTest2')
        st = onoff4.cget('style')
        self.assertEqual(st, 'OnOffButtonTest2')
        opts = {
            'background': 'purple',
            'switchcolor': 'white',
            'oncolor': 'blue',
            'offcolor': 'red',
            'disabledcolor': 'gray',
            'switchdisabledcolor': '#d9d9d9',
        }
        for key, value in opts.items():
            self.assertEqual(style.lookup(st, key), value)

    def test_onoffbutton_kwargs(self):
        self.assertRaises(TypeError, lambda: OnOffButton(self.window, size='a'))

    def _button_changed(self, button):
        return button
