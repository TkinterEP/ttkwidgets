# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import ItemsCanvas
from tests import BaseWidgetTest
from ttkwidgets.utilities import get_assets_directory
import os
from PIL import Image, ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestItemsCanvas(BaseWidgetTest):
    def test_itemscanvas_init(self):
        canvas = ItemsCanvas(self.window)
        canvas.pack()
        self.window.update()

    def test_itemscanvas_cget(self):
        canvas = ItemsCanvas()
        canvas.cget("canvaswidth")
        canvas.cget("canvasheight")
        canvas.cget("function_new")
        canvas.cget("callback_add")
        canvas.cget("callback_del")
        canvas.cget("callback_move")
        canvas.cget("width")

    def test_itemscanvas_getsetitem(self):
        canvas = ItemsCanvas()
        value = canvas["canvaswidth"]
        self.assertIsInstance(value, int)
        canvas["canvaswidth"] = 20

    def test_itemscanvas_config(self):
        canvas = ItemsCanvas()
        canvas.config(canvaswidth=1024, canvasheight=1024)

    def test_itemscanvas_items(self):
        canvas = ItemsCanvas()
        canvas.add_item(text="Item", backgroundcolor="red", textcolor="green", highlightcolor="#ffffff",
                        font=("default", 15, "italic"))
        self.window.update()

    def test_itemscanvas_events(self):
        canvas = ItemsCanvas()
        canvas.current = 1
        canvas.left_motion(self.TkinterEvent())
        canvas.right_press(self.TkinterEvent())
        canvas.left_press(self.TkinterEvent())
        canvas.left_release(self.TkinterEvent())

    def test_itemscanvas_background(self):
        canvas = ItemsCanvas()
        path = os.path.join(get_assets_directory(), "open.png")
        img = ImageTk.PhotoImage(Image.open(path))
        canvas.set_background(image=img)
        self.window.update()
        canvas.set_background(path=path)
        self.window.update()
        self.assertRaises(ValueError, lambda: canvas.set_background(image=img, path=path))
        self.assertRaises(ValueError, canvas.set_background)

    class TkinterEvent(object):
        x_root = 0
        y_root = 0
        x = 0
        y = 0
        widget = tk.Canvas()
