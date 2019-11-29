# -*- coding: utf-8 -*-
"""
Author : Dogeek
(C) 2019
"""

import os
from ttkwidgets import DirTree
from tests import BaseWidgetTest


class TestDirTree(BaseWidgetTest):
    def test_dirtree_init(self):
        tree = DirTree(self.window)
        tree.pack()
        self.window.update()

    def test_dirtree_path(self):
        tree = DirTree(self.window)
        tree.pack()
        self.window.update()
        self.assertTrue(tree.path == os.getcwd())
        self.window.update()
