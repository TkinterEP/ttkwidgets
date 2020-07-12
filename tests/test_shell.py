# Copyright (c) Dogeek 2020
# For license see LICENSE
from ttkwidgets import Shell
from tests import BaseWidgetTest


class TestShell(BaseWidgetTest):
    def test_shell_init(self):
        shell = Shell(self.window)
        shell.pack()
        self.window.update()
        shell.destroy()

    def test_shell_forcefocus(self):
        shell = Shell(self.window, force_focus=True)
        shell.after(1000, lambda: self.assertIsNotNone(shell.focus_get()))
