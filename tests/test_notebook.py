# -*- coding: utf-8 -*-
"""
Author : Dogeek
(C) 2019
"""

import os
from ttkwidgets import Notebook
from tests import BaseWidgetTest


class TestDirTree(BaseWidgetTest):
    def test_notebook_init(self):
        nb = Notebook(self.window)
        nb.grid()
        self.window.update()
