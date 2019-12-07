# -*- coding: utf-8 -*-
"""
Author: Dogeek
Copyright (c) 2019 Dogeek
"""
from ttkwidgets import Notebook
from tests import BaseWidgetTest


class TestNotebook(BaseWidgetTest):
    def test_notebook_init(self):
        nb = Notebook(self.window)
        nb.grid()
        self.window.update()
