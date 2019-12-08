# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets import Notebook
from tests import BaseWidgetTest
import tkinter as tk


class TestNotebook(BaseWidgetTest):
    def test_notebook_init(self):
        nb = Notebook(self.window)
        nb.grid()
        self.window.update()
    
    def test_notebook_prev(self):
        nb = Notebook(self.window)
        f1 = tk.Frame(self.window, width=300, height=300, bg='red')
        f2 = tk.Frame(self.window, width=300, height=300, bg='green')
        f3 = tk.Frame(self.window, width=300, height=300, bg='blue')
        nb.add(f1, text='f1')
        nb.add(f2, text='f2')
        nb.add(f3, text='f3')
        nb.grid()
        self.window.update()
        nb.select(1)
        nb.select_prev()
        self.assertEqual(nb.current_tab, 0)
    
    def test_notebook_next(self):
        nb = Notebook(self.window)
        f1 = tk.Frame(self.window, width=300, height=300, bg='red')
        f2 = tk.Frame(self.window, width=300, height=300, bg='green')
        f3 = tk.Frame(self.window, width=300, height=300, bg='blue')
        nb.add(f1, text='f1')
        nb.add(f2, text='f2')
        nb.add(f3, text='f3')
        nb.grid()
        self.window.update()
        nb.select(1)
        nb.select_next()
        self.assertEqual(nb.current_tab, 2)
