# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets.autocomplete import AutocompleteCombobox, AutocompleteEntry
from tests import BaseWidgetTest
import tkinter as tk


class TestEvent(object):
    def __init__(self, key="A"):
        self.keysym = key


class TestAutocompleteWidgets(BaseWidgetTest):
    def test_autocompletecombobox(self):
        box = AutocompleteCombobox(self.window, completevalues=["Apple", "Pear", "Banana"])
        box.pack()
        self.window.update()

        self.assertIn('completevalues', box.keys())
        self.assertEqual(box['completevalues'], sorted(["Apple", "Pear", "Banana"]))

        box.insert(0, "A")
        self.window.update()
        for item in ["A", "Up", "Down", "Left", "Right", "Return"]:
            box.handle_keyrelease(TestEvent(item))
        box.autocomplete(0)
        box.set_completion_list(["Apply"])
        self.assertEqual(box['completevalues'], ["Apply"])
        box['completevalues'] = ["Test"]
        self.assertEqual(box['completevalues'], ["Test"])

    def test_autocompletecombobox_unsorted(self):
        box = AutocompleteCombobox(self.window, completevalues=["Apple", "Pear", "Banana"], sort=False)
        box.pack()
        self.window.update()

        self.assertIn('completevalues', box.keys())
        self.assertEqual(box['completevalues'], ["Apple", "Pear", "Banana"])

    def test_autocompleteentry(self):
        entry = AutocompleteEntry(self.window, completevalues=["Apple", "Pear", "Banana"])
        entry.pack()
        self.window.update()

        self.assertIn('completevalues', entry.keys())
        self.assertEqual(entry['completevalues'], sorted(["Apple", "Pear", "Banana"]))

        entry.insert(0, "A")
        self.window.update()
        for item in ["A", "Up", "Down", "Left", "Right", "Return"]:
            entry.handle_keyrelease(TestEvent(item))
        entry.autocomplete(0)
        entry.set_completion_list(["Apply"])
        self.assertEqual(entry['completevalues'], ["Apply"])
        entry['completevalues'] = ["Test"]
        self.assertEqual(entry['completevalues'], ["Test"])
