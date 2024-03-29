# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import CheckboxTreeview
from tests import BaseWidgetTest


class TestCheckboxTreeview(BaseWidgetTest):
    def test_checkboxtreeview_init(self):
        tree = CheckboxTreeview(self.window)
        tree.pack()
        self.window.update()

    def test_checkboxtreeview_events(self):
        tree = CheckboxTreeview(self.window)
        tree.pack()
        self.window.update()
        tree.event_generate("<1>", x=10, y=10)
        self.window.update()

    def test_checkboxtreeview_methods(self):
        tree = CheckboxTreeview(self.window)
        tree.pack()
        self.window.update()
        tree.insert("", "end", "1", text="1")
        tree.insert("1", "end", "11", text="11")
        tree.insert("11", "end", "111", text="111")
        tree.insert("11", "end", "112", text="112")
        self.window.update()
        tree.state()
        self.window.update()
        tree.state(['disabled'])
        self.window.update()
        tree.state(['!disabled'])
        self.window.update()
        tree.collapse_all()
        self.window.update()
        tree.expand_all()
        self.window.update()
        tree.tag_add("1", "item")
        self.assertTrue(tree.tag_has("item", "1"))
        self.window.update()
        tree.change_state("1", "checked")
        self.assertTrue(tree.tag_has("checked", "1"))
        self.assertFalse(tree.tag_has("unchecked", "1"))
        self.assertFalse(tree.tag_has("tristate", "1"))
        self.assertTrue(tree.tag_has("item", "1"))
        self.window.update()
        tree.tag_del("1", "item")
        self.assertFalse(tree.tag_has("item", "1"))
        self.window.update()
        tree._check_descendant("1")
        self.assertTrue(tree.tag_has("checked", "11"))
        self.assertTrue(tree.tag_has("checked", "111"))
        self.assertTrue(tree.tag_has("checked", "112"))
        self.window.update()
        tree._uncheck_descendant("1")
        self.assertTrue(tree.tag_has("unchecked", "11"))
        self.assertTrue(tree.tag_has("unchecked", "111"))
        self.assertTrue(tree.tag_has("unchecked", "112"))
        self.window.update()
        tree.check_all()
        self.assertTrue(tree.tag_has("checked", "11"))
        self.assertTrue(tree.tag_has("checked", "111"))
        self.assertTrue(tree.tag_has("checked", "112"))
        self.window.update()
        tree.uncheck_all()
        self.assertTrue(tree.tag_has("unchecked", "11"))
        self.assertTrue(tree.tag_has("unchecked", "111"))
        self.assertTrue(tree.tag_has("unchecked", "112"))
        self.window.update()
        tree._check_ancestor("111")
        self.assertTrue(tree.tag_has("tristate", "11"))
        self.window.update()
        tree._check_ancestor("112")
        self.assertTrue(tree.tag_has("checked", "11"))
        self.window.update()
        tree._uncheck_ancestor("111")
        self.assertTrue(tree.tag_has("tristate", "11"))
        self.window.update()
        tree._uncheck_ancestor("112")
        self.assertTrue(tree.tag_has("unchecked", "11"))
        self.window.update()
        tree._tristate_parent("111")
        self.assertTrue(tree.tag_has("tristate", "11"))
        self.assertTrue(tree.tag_has("tristate", "1"))
        self.window.update()
        tree.change_state("1", "checked")
        tree._check_descendant("1")
        self.assertEqual(tree.get_checked(), ["111", "112"])
        self.window.update()
