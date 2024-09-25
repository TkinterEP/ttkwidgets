# Copyright (c) FaraazKurawle 2024
# For license see LICENSE

from ttkwidgets.editable_treeview import EditableTreeview
from tests import BaseWidgetTest

class TestEditableTreeview(BaseWidgetTest):
    def test_editabletreeview_init(self):
        columns = ("attribute", "value")
        data = {f"Demo {i}": f"Demo {i}" for i in range(1, 101)}

        widget = EditableTreeview(self.window, columns=columns, show=" tree", bind_key="<Double-Button-1>", data=data)
        widget.pack(expand=1, fill="both", padx=20, pady=20)