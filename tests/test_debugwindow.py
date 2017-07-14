# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import DebugWindow
from tests import BaseWidgetTest
import mock
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import os
import sys


def is_python_3():
    return sys.version_info[0] is 3


class TestDebugWindow(BaseWidgetTest):
    def test_debugwindow_init(self):
        debug = DebugWindow(self.window)
        self.window.update()

    def test_debugwindow_print(self):
        debug = DebugWindow(self.window)
        print("Something!")
        self.window.update()
        self.assertTrue("Something!" in debug.text.get("1.0", tk.END))

    def test_debugwindow_save(self):
        debug = DebugWindow(self.window)
        print("Something!")
        self.window.update()
        module = "tkinter.filedialog.asksaveasfilename" if is_python_3() else "tkFileDialog.asksaveasfilename"
        with mock.patch(module, return_value="somefile.txt"):
            debug.save()
        self.assertTrue(os.path.exists("somefile.txt"))
        with open("somefile.txt", "r") as f:
            self.assertTrue("Something!" in f.read())
        os.remove("somefile.txt")
