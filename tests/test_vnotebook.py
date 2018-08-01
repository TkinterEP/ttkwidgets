"""
Author: RedFantom
License: GNU GPLv3, as in LICENSE.md
Copyright (C) 2018 RedFantom
"""
from unittest import TestCase
# Basic UI imports
import tkinter as tk
from tkinter import ttk
# Module to test
from ttkwidgets.frames import VNotebook


class TestVNotebook(TestCase):
    def setUp(self):
        self.window = tk.Tk()

    def tearDown(self):
        self.window.destroy()

    def test_init(self):
        VNotebook(self.window).grid()
        self.window.update()

    def add_test_frame(self, notebook, **kwargs):
        notebook.grid()
        frame = ttk.Frame(notebook)
        ttk.Scale(frame).grid()
        frame.grid()
        return notebook.add(frame, text="Test", **kwargs)

    def test_add(self):
        notebook = VNotebook(self.window)
        self.add_test_frame(notebook)
        self.window.update()

    def test_compound(self):
        for compound in (tk.BOTTOM, tk.TOP, tk.RIGHT, tk.LEFT):
            VNotebook(self.window, compound=compound).grid()
            self.window.update()

    def test_index(self):
        notebook = VNotebook(self.window)
        self.add_test_frame(notebook)
        frame = ttk.Frame(notebook)
        notebook.insert(0, frame)
        self.assertEqual(notebook.tabs[0], notebook.get_id_for_tab(frame))
        self.assertEqual(0, notebook.index(frame))

    def test_enable_traversal(self):
        notebook = VNotebook(self.window)
        self.add_test_frame(notebook)
        self.add_test_frame(notebook)
        notebook.enable_traversal()
        active = notebook.active
        notebook._switch_tab(None)
        self.assertNotEqual(active, notebook.active)

    def test_tab_config(self):
        notebook = VNotebook(self.window)
        id = self.add_test_frame(notebook)
        notebook.tab_configure(id, text="Hello")
        self.assertEqual(notebook.tab_cget(id, "text"), "Hello")

    def test_activate(self):
        notebook = VNotebook(self.window)
        self.add_test_frame(notebook)
        self.add_test_frame(notebook)
        self.assertEqual(notebook.tabs[0], notebook.active)
        notebook.activate_index(1)
        self.assertEqual(notebook.tabs[1], notebook.active)
