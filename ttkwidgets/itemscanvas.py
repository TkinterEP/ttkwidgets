"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk


class ItemsCanvas(ttk.Frame):
    def __init__(self, *args, **kwargs):
        # Setup Frame
        self.current = None
        self.items = {}
        width = kwargs.pop("canvaswidth", 512)
        height = kwargs.pop("canvasheight", 512)
        ttk.Frame.__init__(self, *args, **kwargs)
        self._canvaswidth = width
        self._canvasheight = height
        # Setup Canvas
        self._max_x = self._canvaswidth - 10
        self._max_y = self._canvasheight - 10
        self.canvas = tk.Canvas(self, width=width, height=height)
        self._image = None
        self._background = None
        # Setup event bindings
        self.canvas.tag_bind("item", "<ButtonPress-1>", self.left_press)
        self.canvas.tag_bind("item", "<ButtonRelease-1>", self.left_release)
        self.canvas.tag_bind("item", "<B1-Motion>", self.left_motion)
        self.canvas.tag_bind("item", "<ButtonPress-3>", self.right_press)
        self.canvas.bind("<ButtonPress-3>", self.frame_right_press)
        # Setup item menu
        self.item_menu = tk.Menu(self, tearoff=0)
        self.item_menu.add_command(label="Edit", command=self.edit_item)
        self.item_menu.add_command(label="Delete", command=self.del_item)
        # Setup frame menu
        self.frame_menu = tk.Menu(self, tearoff=0)
        self.frame_menu.add_command(label="New", command=self.new_item)
        # Call grid_widgets last
        self.grid_widgets()

    def frame_right_press(self, event):
        self.frame_menu.post(event.x_root, event.y_root)

    def left_press(self, event):
        if self.current:
            self.canvas.itemconfigure(self.current, fill="black")
            self.current = None
            return
        results = self.canvas.find_withtag(tk.CURRENT)
        if len(results) is 0:
            return
        self.current = results[0]
        self.canvas.itemconfigure(self.current, fill="blue")

    def left_release(self, event):
        self.config(cursor="")
        if not self.current:
            self.canvas.itemconfigure(tk.CURRENT, fill="black")

    def left_motion(self, event):
        self.current = None
        item = self.canvas.find_withtag(tk.CURRENT)[0]
        rectangle = self.items[item]
        self.config(cursor="exchange")
        self.canvas.itemconfigure(item, fill="blue")
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        x = self._max_x if x > self._max_x else x
        y = self._max_y if y > self._max_y else y
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.canvas.coords(item, x, y)
        self.canvas.coords(rectangle, self.canvas.bbox(item))

    def right_press(self, event):
        if not self.current:
            return
        self.item_menu.post(event.x_root, event.y_root)

    def grid_widgets(self):
        self.canvas.grid(sticky="nswe")

    def add_item(self, text, font=("default", 12, "bold"), color="yellow"):
        item = self.canvas.create_text(0, 0, anchor=tk.NW, text=text, font=font, fill="black", tag="item")
        rectangle = self.canvas.create_rectangle(self.canvas.bbox(item), fill=color)
        self.canvas.tag_lower(rectangle, item)
        self.items[item] = rectangle

    def new_item(self):
        pass

    def del_item(self):
        item = self.current
        rectangle = self.items[item]
        self.canvas.delete(item, rectangle)

    def edit_item(self):
        pass

    def set_background(self, image=None, path=None, resize=True):
        if not image and not path:
            raise ValueError("You must either pass a PhotoImage object or a path object")
        if image and path:
            raise ValueError("You must pass either a PhotoImage or str path, not both")
        if image is not None and not isinstance(image, tk.PhotoImage) and not isinstance(image, ImageTk.PhotoImage):
            raise ValueError("The image passed is not a PhotoImage object")
        if path is not None and not isinstance(path, str):
            raise ValueError("The image path passed is not of str type: {0}".format(path))
        if not os.path.exists(path):
            raise ValueError("The iamge path passed is not valid: {0}".format(path))
        if image is not None:
            self._image = image
        elif path is not None:
            img = Image.open(path)
            if resize:
                img = img.resize(self._canvaswidth, self._canvasheight, Image.ANTIALIAS)
            self._image = ImageTk.PhotoImage(img)
        self._background = self.canvas.create_image(0, 0, image=self._image, anchor=tk.NW, tag="background")
        self.canvas.tag_lower("background")
