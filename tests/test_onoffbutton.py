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
        variable = onoff._variable
        self.assertEqual(isinstance(variable, tk.StringVar), True)
        self.assertEqual(variable.get(), 'off')
        variable.set('on')
        self.assertEqual(variable.get(), 'on')

    def test_onoffbutton_variable_int(self):
        variable = tk.IntVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), 0)
        variable.set(1)
        self.assertEqual(variable.get(), 1)

    def test_onoffbutton_variable_bool(self):
        variable = tk.BooleanVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), False)
        variable.set(True)
        self.assertEqual(variable.get(), True)

    def test_onoffbutton_variable_string(self):
        variable = tk.StringVar()
        onoff = OnOffButton(self.window, variable=variable)
        onoff.pack()
        self.window.update()
        self.assertEqual(variable.get(), 'off')
        variable.set('on')
        self.assertEqual(variable.get(), 'on')

    def test_onoffbutton_invoke(self):
        onoff = OnOffButton(self.window, command=self._button_changed)
        onoff.pack()
        self.window.update()
        self.assertEqual(onoff.get(), 'off')
        result = onoff.invoke()
        self.assertEqual('Invoked', result)
        self.assertEqual(onoff.get(), 'on')

    def test_onoffbutton_style(self):
        style = ttk.Style()
        onoff = OnOffButton(self.window)
        onoff.pack()
        self.window.update()
        self.assertEqual(onoff.cget('class'), 'OnOffButton')
        st = onoff.cget('style')
        self.assertEqual(st, 'OnOffButton')

        # New custom style passing at init
        style.configure('OnOffButtonTest.OnOffButton',
                        background='orange', oncolor='brown')
        onoff2 = OnOffButton(self.window,
                             style='OnOffButtonTest.OnOffButton')
        onoff2.pack()
        self.window.update()
        self.assertEqual(onoff2.cget('class'), 'OnOffButton')
        st = onoff2.cget('style')
        self.assertEqual(st, 'OnOffButtonTest.OnOffButton')

        # Passing style to widget config
        style.configure('OnOffButtonTest2.OnOffButton',
                        background='purple', oncolor='blue')
        onoff3 = OnOffButton(self.window)
        onoff3.pack()
        self.window.update()
        onoff3.config(style='OnOffButtonTest2.OnOffButton')
        st = onoff3.cget('style')
        self.assertEqual(st, 'OnOffButtonTest2.OnOffButton')

    def _button_changed(self):
        return 'Invoked'
