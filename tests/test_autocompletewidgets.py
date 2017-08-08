# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.autocomplete import AutocompleteCombobox, AutocompleteEntry
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestEvent(object):
    def __init__(self, key="A"):
        self.keysym = key


class TestAutocompleteWidgets(BaseWidgetTest):
    def test_autocompletecombobox(self):
        box = AutocompleteCombobox(self.window, completevalues=["Apple", "Pear", "Banana"])
        box.pack()
        self.window.update()
        box.insert(0, "A")
        self.window.update()
        for item in ["A", "Up", "Down", "Left", "Right", "Return"]:
            box.handle_keyrelease(TestEvent(item))
        box.autocomplete(0)
        box.set_completion_list(["Apply"])

    def test_autocompleteentry(self):
        entry = AutocompleteEntry(self.window, completevalues=["Apple", "Pear", "Banana"])
        entry.pack()
        self.window.update()
        entry.insert(0, "A")
        self.window.update()
        for item in ["A", "Up", "Down", "Left", "Right", "Return"]:
            entry.handle_keyrelease(TestEvent(item))
        entry.autocomplete(0)
        entry.set_completion_list(["Apply"])
