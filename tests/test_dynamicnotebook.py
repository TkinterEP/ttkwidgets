# Copyright (c) FaraazKurawle 2024
# For license see LICENSE

from ttkwidgets.dynamic_notebook import DynamicNotebook
from tests import BaseWidgetTest

class TestDynamicNotebook(BaseWidgetTest):
    def test_dynamicnotebook_init(self):
        widget = DynamicNotebook(self.window)
        widget.pack()
        self.window.update()

    def test_dynamicnotebook_buttons_functions(self):
        widget = DynamicNotebook(self.window)
        widget.pack()
        widget.add_frame_button_func()
        widget.remove_frame()

    def test_dynamicnotebook_kw(self):
        widget = DynamicNotebook(self.window)
        widget.pack()