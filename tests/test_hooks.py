"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
from unittest import TestCase
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets.hook import hook_ttk_widgets, generate_hook_name, is_hooked
    

class TestHooks(TestCase):

    def setUp(self):
        self.window = tk.Tk()
        self.expected = {None: None}
        self.updated = False
        self.user_hook_called = False
        self.second_updated = False
        self.second_expected = {None: None}

    def basic_updater(self, widget, option, value):
        if option not in self.expected:
            return
        self.assertEquals(value, self.expected[option], "Invalid value for {}: {}".format(option, value))
        self.updated = True
        del self.expected[option]

    def second_updater(self, widget, option, value):
        if option not in self.second_expected:
            return  # Not updated with desired option
        self.assertEquals(value, self.second_expected[option])
        self.second_updated = True
        self.second_expected.clear()

    def has_been_updated(self):
        updated = self.updated
        self.updated = False
        return updated and len(self.expected) == 0

    def has_been_second_updated(self):
        updated = self.second_updated
        self.second_updated = False
        return updated and len(self.expected) == 0

    def test_basic_hook(self):
        self.expected = {"random_kwarg": "Hello World"}
        options = {"random_kwarg": "Default Value"}
        hook_ttk_widgets(self.basic_updater, options)
        button = ttk.Button(random_kwarg="Hello World")
        self.assertTrue(self.has_been_updated())

        self.assertTrue(is_hooked(options))
        self.assertTrue(hasattr(ttk.Button, generate_hook_name(options)))
        self.assertTrue("random_kwarg" in button.keys())

    def test_user_hook_and_defaults(self):
        self.expected = {"not_user": "Hello World"}
        options = self.expected.copy()
        hook_ttk_widgets(self.basic_updater, self.expected.copy())

        button_init = ttk.Button.__init__

        def __init__(self_widget, *args, **kwargs):
            self.user_hook_called = True
            button_init(self_widget, *args, **kwargs)

        ttk.Button.__init__ = __init__

        ttk.Button()
        self.assertTrue(self.user_hook_called)
        self.assertTrue(is_hooked(options))
        self.assertTrue(self.has_been_updated())

    def test_multi_hooks(self):
        options1 = {"hook1": "Default One"}
        options2 = {"hook2": "Default Two"}
        self.expected = {"hook1": "Custom One"}
        self.second_expected = {"hook2": "Default Two"}

        name = hook_ttk_widgets(self.basic_updater, options1)
        hook_ttk_widgets(self.second_updater, options2)
        self.assertEquals(name, generate_hook_name(options1))

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        button = ttk.Button(hook1="Custom One")

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        self.assertTrue(self.has_been_updated())
        self.assertTrue(self.has_been_second_updated())

        self.assertTrue("hook1" in button.keys() and "hook2" in button.keys())

    def test_multi_option_hooks_cget_config_keys_overwrite(self):
        options = {"hookx": "Default X", "hooky": "Default Y"}
        self.expected = {"hookx": "Default X", "hooky": "Option Y"}

        hook_ttk_widgets(self.basic_updater, options)
        self.assertTrue(is_hooked(options))
        self.assertTrue(is_hooked({"hookx": None}))
        self.assertTrue(is_hooked({"hooky": None}))

        button = ttk.Button(hooky="Option Y")

        self.assertTrue(self.has_been_updated())
        self.assertTrue("hooky" in button.keys())
        self.assertTrue("hookx" in button.keys())
        self.assertEqual("Default X", button.cget("hookx"))
        self.assertEqual("Option Y", button.cget("hooky"))

        self.expected = {"hookx": "Option X"}
        button.configure(hookx="Option X", command=self.window.destroy)
        self.assertTrue(self.has_been_updated())

        self.assertEqual("Option X", button.cget("hookx"))
        self.assertEqual("Option Y", button.cget("hooky"))
        self.assertIsNotNone(button.cget("command"))

        self.assertRaises(RuntimeError, lambda: hook_ttk_widgets(self.basic_updater, options))
        self.assertRaises(RuntimeError, lambda: hook_ttk_widgets(None, {"hookx": "New Default X"}))

        options["hookx"] = "New Default X"
        hook_ttk_widgets(None, options)
        self.expected = options.copy()
        ttk.Button()
        self.assertTrue(self.has_been_updated())

    def tearDown(self):
        self.window.destroy()

