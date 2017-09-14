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
from pynput.mouse import Controller, Button


class TestItemsCanvas(BaseWidgetTest):
    def test_itemscanvas_init(self):
        canvas = ItemsCanvas(self.window)
        canvas.pack()
        self.window.update()

    def test_items_canvas_get_options(self):
        canvas = ItemsCanvas()
        keys = ["canvaswidth", "canvasheight", "function_new", "callback_add", "callback_del", "callback_move", "width"]
        for key in keys:
            canvas.cget(key)
            self.assertTrue(key in canvas.keys())

    def test_itemscanvas_getsetitem(self):
        canvas = ItemsCanvas()
        value = canvas["canvaswidth"]
        self.assertIsInstance(value, int)
        canvas["canvaswidth"] = 20

    def test_itemscanvas_config(self):
        canvas = ItemsCanvas()
        canvas.config(canvaswidth=1024, canvasheight=1024)

    def test_itemscanvas_items(self):
        canvas = ItemsCanvas(callback_del=lambda *args: args)
        canvas.add_item(text="Item", backgroundcolor="red", textcolor="green", highlightcolor="#ffffff",
                        font=("default", 15, "italic"))
        canvas.current = 1
        canvas.del_item()
        self.window.update()

    def test_itemscanvas_events(self):
        canvas = ItemsCanvas(callback_add=lambda *args: args,
                             callback_move=lambda *args: args,
                             function_new=lambda *args: args)
        canvas.add_item(text="Item")
        canvas.current = 1
        canvas.left_motion(self.TkinterEvent())
        canvas.current = 1
        canvas.canvas.itemconfigure(1, tags=("item", "current"))
        canvas.left_motion(self.TkinterEvent())
        # canvas.right_press(self.TkinterEvent())
        canvas.current = 1
        # canvas.right_press(self.TkinterEvent())
        canvas.frame_menu.invoke(1)
        canvas.left_press(self.TkinterEvent())
        canvas.current = 1
        canvas.left_press(self.TkinterEvent())
        canvas.current = 1
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
        self.assertRaises(ValueError, canvas.set_background, path=1)
        self.assertRaises(ValueError, canvas.set_background, path="/path/not/existing")
        self.assertRaises(ValueError, canvas.set_background, image=1)

    def test_itemscanvas_drag(self):
        canvas = ItemsCanvas(self.window)
        canvas.pack()
        canvas.add_item("item", font=("default", 16))
        self.window.wm_geometry("+0+0")
        self.window.update()
        mouse_controller = Controller()
        mouse_controller.position = (30, 40)
        self.window.update()
        mouse_controller.press(Button.left)
        self.window.update()
        mouse_controller.move(100, 100)
        self.window.update()
        mouse_controller.release(Button.left)
        self.window.update()

    def test_itemscanvas_select(self):
        canvas = ItemsCanvas()
        canvas.pack()
        canvas.add_item("item", font=("default", 16))
        self.window.wm_geometry("+0+0")
        self.window.update()
        mouse_controller = Controller()
        mouse_controller.position = (30, 40)
        self.window.update()
        mouse_controller.press(Button.left)
        self.window.update()
        mouse_controller.release(Button.left)
        self.window.update()

    def test_itemscanvas_menu(self):
        canvas = ItemsCanvas()
        canvas.pack()
        self.window.wm_geometry("+0+0")
        self.window.update()
        mouse_controller = Controller()
        mouse_controller.position = (0, 0)
        mouse_controller.move(30, 40)
        self.window.update()
        mouse_controller.press(Button.right)
        self.window.update()
        mouse_controller.release(Button.right)
        self.window.update()

    class TkinterEvent(object):
        x_root = 0
        y_root = 0
        x = 0
        y = 0
        widget = tk.Canvas()
