# Copyright (c) FaraazKurawle 2024
# For license see LICENSE

from ttkwidgets.numberedtext import NumberedText
from tests import BaseWidgetTest

class TestNumberedText(BaseWidgetTest):
    def test_numberedtext_init(self):
        widget = NumberedText(self.window)
        widget.pack()
        self.window.update()

    def test_numberedtext_buttons_functions(self):
        widget = NumberedText(self.window)
        widget.pack()
        # No buttons

    def test_numberedtextr_kw(self):
        widget = NumberedText(self.window, bg="red")
        widget.pack()