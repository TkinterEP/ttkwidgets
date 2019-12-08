# -*- coding: utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: This repository

Treeview with checkboxes at each item and a noticeable disabled style
"""

try:
    import ttk
except ImportError:
    from tkinter import ttk

import os
from PIL import Image, ImageTk
from ttkwidgets.utilities import get_assets_directory

IM_CHECKED = os.path.join(get_assets_directory(), "checked.png")      # These three checkbox icons were isolated from
IM_UNCHECKED = os.path.join(get_assets_directory(), "unchecked.png")  # Checkbox States.svg (https://commons.wikimedia.org/wiki/File:Checkbox_States.svg?uselang=en)
IM_TRISTATE = os.path.join(get_assets_directory(), "tristate.png")    # by Marekich [CC BY-SA 3.0  (https://creativecommons.org/licenses/by-sa/3.0)]


class CheckboxTreeview(ttk.Treeview):
    """
    :class:`ttk.Treeview` widget with checkboxes left of each item.
    
    .. note::
        The checkboxes are done via the image attribute of the item, 
        so to keep the checkbox, you cannot add an image to the item.
    """

    def __init__(self, master=None, **kw):
        """
        Create a CheckboxTreeview.

        :param master: master widget
        :type master: widget
        :param kw: options to be passed on to the :class:`ttk.Treeview` initializer
        """
        ttk.Treeview.__init__(self, master, style='Checkbox.Treeview', **kw)
        # style (make a noticeable disabled style)
        style = ttk.Style(self)
        style.map("Checkbox.Treeview",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')])
        # checkboxes are implemented with pictures
        self.im_checked = ImageTk.PhotoImage(Image.open(IM_CHECKED), master=self)
        self.im_unchecked = ImageTk.PhotoImage(Image.open(IM_UNCHECKED), master=self)
        self.im_tristate = ImageTk.PhotoImage(Image.open(IM_TRISTATE), master=self)
        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("tristate", image=self.im_tristate)
        self.tag_configure("checked", image=self.im_checked)
        # check / uncheck boxes on click
        self.bind("<Button-1>", self._box_click, True)

    def expand_all(self):
        """Expand all items."""

        def aux(item):
            self.item(item, open=True)
            children = self.get_children(item)
            for c in children:
                aux(c)

        children = self.get_children("")
        for c in children:
            aux(c)

    def collapse_all(self):
        """Collapse all items."""

        def aux(item):
            self.item(item, open=False)
            children = self.get_children(item)
            for c in children:
                aux(c)

        children = self.get_children("")
        for c in children:
            aux(c)

    def state(self, statespec=None):
        """
        Modify or inquire widget state.
        
        :param statespec: Widget state is returned if `statespec` is None, 
                          otherwise it is set according to the statespec 
                          flags and then a new state spec is returned 
                          indicating which flags were changed.
        :type statespec: None or sequence[str]
        """
        if statespec:
            if "disabled" in statespec:
                self.bind('<Button-1>', lambda e: 'break')
            elif "!disabled" in statespec:
                self.unbind("<Button-1>")
                self.bind("<Button-1>", self._box_click, True)
            return ttk.Treeview.state(self, statespec)
        else:
            return ttk.Treeview.state(self)

    def change_state(self, item, state):
        """
        Replace the current state of the item.

        i.e. replace the current state tag but keeps the other tags.
        
        :param item: item id
        :type item: str
        :param state: "checked", "unchecked" or "tristate": new state of the item 
        :type state: str
        """
        tags = self.item(item, "tags")
        states = ("checked", "unchecked", "tristate")
        new_tags = [t for t in tags if t not in states]
        new_tags.append(state)
        self.item(item, tags=tuple(new_tags))

    def tag_add(self, item, tag):
        """
        Add tag to the tags of item.
        
        :param item: item identifier
        :type item: str
        :param tag: tag name
        :type tag: str
        """
        tags = self.item(item, "tags")
        self.item(item, tags=tags + (tag,))

    def tag_del(self, item, tag):
        """
        Remove tag from the tags of item.
        
        :param item: item identifier
        :type item: str
        :param tag: tag name
        :type tag: str
        """
        tags = list(self.item(item, "tags"))
        if tag in tags:
            tags.remove(tag)
            self.item(item, tags=tuple(tags))

    def insert(self, parent, index, iid=None, **kw):
        """
        Creates a new item and return the item identifier of the newly created item.
        
        :param parent: identifier of the parent item
        :type parent: str
        :param index: where in the list of parent's children to insert the new item
        :type index: int or "end"
        :param iid: item identifier, iid must not already exist in the tree. If iid is None a new unique identifier is generated.
        :type iid: None or str
        :param kw: other options to be passed on to the :meth:`ttk.Treeview.insert` method
        
        :return: the item identifier of the newly created item
        :rtype: str

        .. note:: Same method as for the standard :class:`ttk.Treeview` but 
                  add the tag for the box state accordingly to the parent 
                  state if no tag among 
                  ('checked', 'unchecked', 'tristate') is given.
        """
        if self.tag_has("checked", parent):
            tag = "checked"
        else:
            tag = 'unchecked'
        if "tags" not in kw:
            kw["tags"] = (tag,)
        elif not ("unchecked" in kw["tags"] or "checked" in kw["tags"] or
                  "tristate" in kw["tags"]):
            kw["tags"] += (tag,)

        return ttk.Treeview.insert(self, parent, index, iid, **kw)

    def get_checked(self):
        """Return the list of checked items that do not have any child."""
        checked = []

        def get_checked_children(item):
            if not self.tag_has("unchecked", item):
                ch = self.get_children(item)
                if not ch and self.tag_has("checked", item):
                    checked.append(item)
                else:
                    for c in ch:
                        get_checked_children(c)

        ch = self.get_children("")
        for c in ch:
            get_checked_children(c)
        return checked

    def _check_descendant(self, item):
        """Check the boxes of item's descendants."""
        children = self.get_children(item)
        for iid in children:
            self.change_state(iid, "checked")
            self._check_descendant(iid)

    def _check_ancestor(self, item):
        """
        Check the box of item and change the state of the boxes of item's
        ancestors accordingly.
        """
        self.change_state(item, "checked")
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["checked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is not checked and item's box is checked
                self._tristate_parent(parent)
            else:
                # all boxes of the children are checked
                self._check_ancestor(parent)

    def _tristate_parent(self, item):
        """
        Put the box of item in tristate and change the state of the boxes of
        item's ancestors accordingly.
        """
        self.change_state(item, "tristate")
        parent = self.parent(item)
        if parent:
            self._tristate_parent(parent)

    def _uncheck_descendant(self, item):
        """Uncheck the boxes of item's descendant."""
        children = self.get_children(item)
        for iid in children:
            self.change_state(iid, "unchecked")
            self._uncheck_descendant(iid)

    def _uncheck_ancestor(self, item):
        """
        Uncheck the box of item and change the state of the boxes of item's
        ancestors accordingly.
        """
        self.change_state(item, "unchecked")
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["unchecked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is checked and item's box is unchecked
                self._tristate_parent(parent)
            else:
                # no box is checked
                self._uncheck_ancestor(parent)

    def _box_click(self, event):
        """Check or uncheck box when clicked."""
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)
            if self.tag_has("unchecked", item) or self.tag_has("tristate", item):
                self._check_ancestor(item)
                self._check_descendant(item)
            else:
                self._uncheck_descendant(item)
                self._uncheck_ancestor(item)
