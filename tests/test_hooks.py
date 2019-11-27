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


def printf(*args, **kwargs):
    kwargs["flush"] = True
    print(*args, **kwargs)
    

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
            print("basic_updater is expecting {} and got {}: {}, so it is ignored".format(
                self.expected, option, value))
            return
        printf("basic_updater is expecting {} and got {}: {}".format(self.expected, option, value))
        self.assertEquals(value, self.expected[option], "Invalid value for {}: {}".format(option, value))
        self.updated = True
        self.expected.clear()

    def second_updater(self, widget, option, value):
        if option not in self.second_expected:
            return  # Not updated with desired option
        self.assertEquals(value, self.second_expected[option])
        self.second_updated = True
        self.second_expected.clear()

    def has_been_updated(self):
        updated = self.updated
        self.updated = False
        return updated

    def has_been_second_updated(self):
        updated = self.second_updated
        self.second_updated = False
        return updated

    def test_basic_hook(self):
        printf("Started test_basic_hook")
        self.expected = {"tooltip": "Hello World"}
        printf("test_basic_hook is expecting:", self.expected)
        options = {"tooltip": "Default Value"}
        hook_ttk_widgets(self.basic_updater, options)
        ttk.Button(tooltip="Hello World")
        self.assertTrue(self.has_been_updated())

        self.assertTrue(is_hooked(options))
        self.assertTrue(hasattr(ttk.Button, generate_hook_name(options)))

        printf("Finished test_basic_hook")

    def test_user_hook_and_defaults(self):
        printf("Started test_user_hook", flush=True)
        self.expected = {"not_user": "Hello World"}
        options = self.expected.copy()
        hook_ttk_widgets(self.basic_updater, self.expected.copy())

        button_init = ttk.Button.__init__

        def __init__(self_widget, *args, **kwargs):
            self.user_hook_called = True
            button_init(self_widget, *args, **kwargs)

        ttk.Button.__init__ = __init__

        printf("test_user_hook is expecting: ", self.expected)
        ttk.Button()
        self.assertTrue(self.user_hook_called)
        self.assertTrue(is_hooked(options))
        self.assertTrue(self.has_been_updated())
        printf("Finished test_user_hook")

    def test_multi_hooks(self):
        printf("Started test_multi_hooks")
        options1 = {"hook1": "Default One"}
        options2 = {"hook2": "Default Two"}
        self.expected = {"hook1": "Custom One"}
        printf("test_multi_hooks is expecting: ", self.expected)
        self.second_expected = {"hook2": "Default Two"}

        name = hook_ttk_widgets(self.basic_updater, options1)
        hook_ttk_widgets(self.second_updater, options2)
        self.assertEquals(name, generate_hook_name(options1))

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        ttk.Button(hook1="Custom One")

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        self.assertTrue(self.has_been_updated())
        self.assertTrue(self.has_been_second_updated())
        printf("Finished test_multi_hooks")

    def tearDown(self):
        self.window.destroy()

