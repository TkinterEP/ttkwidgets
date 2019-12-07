# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets import Notebook
from tests import BaseWidgetTest


class TestNotebook(BaseWidgetTest):
    def test_notebook_init(self):
        nb = Notebook(self.window)
        nb.grid()
        self.window.update()
