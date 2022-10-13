# Copyright (c) Dogeek 2020
# For license see LICENSE
from ttkwidgets.utilities import isint, isfloat
from tests import BaseWidgetTest
import tkinter as tk


class TestUtilities(BaseWidgetTest):
    def test_isint(self):
        intvar = tk.IntVar()
        self.assertTrue(isint(intvar))
        stringvar = tk.StringVar()
        stringvar.set('123')
        self.assertTrue(isint(stringvar))
        self.assertTrue(isint('123'))
        self.assertTrue(isint(123))
        self.assertFalse(isint(123.0))
        self.assertFalse(isint('123.4'))

    def test_isfloat(self):
        intvar = tk.IntVar()
        self.assertFalse(isfloat(intvar))
        stringvar = tk.StringVar()
        stringvar.set('123')
        self.assertFalse(isfloat(stringvar))
        stringvar.set('123.0')
        self.assertTrue(isfloat(stringvar))
        self.assertFalse(isfloat('123'))
        self.assertFalse(isfloat(123))
        self.assertTrue(isfloat(123.0))
        self.assertTrue(isfloat('123.4'))


if __name__ == '__main__':
    import unittest
    unittest.main()
