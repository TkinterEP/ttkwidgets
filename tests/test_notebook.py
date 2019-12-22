# Copyright (c) Dogeek 2019
# For license see LICENSE
from ttkwidgets import Notebook
from tests import BaseWidgetTest
from tkinter import ttk
import tkinter as tk


class TestNotebook(BaseWidgetTest):
    def test_notebook_init(self):
        nb = Notebook(self.window)
        nb.grid()
        self.window.update()

    def test_notebook_add_tab(self):
        nb = Notebook(self.window)
        frame = ttk.Frame(self.window, width=200, height=200)
        nb.add(frame, text="Frame")
        nb.grid()
        self.window.update()

    def test_notebook_select_tab(self):
        nb = Notebook(self.window)
        frame = ttk.Frame(self.window, width=200, height=200)
        frame2 = ttk.Frame(self.window, width=200, height=200)
        nb.add(frame, text="Frame")
        nb.add(frame2, text="Frame2")
        nb.grid()
        nb.select_next()
        nb.select_next()
        nb.select_prev()
        self.window.update()

    def test_notebook_move_tab(self):
        nb = Notebook(self.window, drag_to_toplevel=False)
        for i in range(3):
            frame = ttk.Frame(self.window, width=200, height=200)
            nb.add(frame, text="Frame" + str(i))
        nb._dragged_tab = nb.tabs()[0]
        nb.swap(nb.tabs()[1])
        nb._on_click(None)
        self.assertEqual(nb._visible_tabs, [1, 0, 2])

    def test_notebook_insert(self):
        nb = Notebook(self.window, drag_to_toplevel=False)
        for i in range(3):
            frame = ttk.Frame(self.window, width=200, height=200)
            nb.add(frame, text="Frame" + str(i))
        nb.insert('.!toplevel.!frame2',
                  ttk.Frame(self.window, width=200, height=200),
                  text="Added")

        self.assertEqual(nb._visible_tabs, [3, 0, 1, 2]) # not sure

    def test_notebook_index(self):
        nb = Notebook(self.window)
        for i in range(10):
            frame = ttk.Frame(self.window, width=200, height=200)
            nb.add(frame, text="Frame" + str(i))

        with self.assertRaises(ValueError):
            nb.index('.!toplevel.!frame11')

        self.assertEqual(nb.index('.!toplevel.!frame'), 0)
        self.assertEqual(nb.index(tk.END), 9)
        nb.current_tab = 0
        self.assertEqual(nb.index(tk.CURRENT), 0)

        self.window.update()

    def test_notebook_forget_tab(self):
        nb = Notebook(self.window)
        for i in range(3):
            frame = ttk.Frame(self.window, width=200, height=200)
            nb.add(frame, text="Frame" + str(i))

        nb.forget('.!toplevel.!frame')

    def test_notebook_config_tab(self):
        nb = Notebook(self.window)
        for i in range(10):
            frame = ttk.Frame(self.window, width=200, height=200)
            nb.add(frame, text="Frame" + str(i))

        with self.assertRaises(ValueError):
            nb.tab(tk.CURRENT, state='random')

        nb.tab(tk.CURRENT, text="Changed")
        self.window.update()
