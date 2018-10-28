"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
import os
from PIL import Image, ImageTk


class ItemsCanvas(ttk.Frame):
    """
    A :class:`ttk.Frame` containing a Canvas upon which text items can be placed with a coloured background. 
    
    The items can be moved around and deleted. A background can also be set.
    """

    def __init__(self, *args, **kwargs):
        """
        Create an ItemsCanvas.
        
        :param canvaswidth: width of the canvas in pixels
        :type canvaswidth: int
        :param canvasheight: height of the canvas in pixels
        :type canvascanvasheightwidth: int
        :param callback_add: callback for when an item is created, \*(int item, int rectangle)
        :type callback_add: function
        :param callback_del: callback for when an item is deleted, \*(int item, int rectangle)
        :type callback_del: function
        :param callback_move: callback for when an item is moved, \*(int item, int rectangle, int x, int y)
        :type callback_move: function
        :param function_new: user defined function for when an item is created, \*(self.add_item)
        :type function_new: function
        """
        # Setup Frame
        self.current = None
        self.current_coords = 0, 0
        self.items = {}
        self.item_colors = {}
        # kwarg processing
        self._canvaswidth = kwargs.pop("canvaswidth", 512)
        self._canvasheight = kwargs.pop("canvasheight", 512)
        self._function_new = kwargs.pop("function_new", None)
        self._callback_add = kwargs.pop("callback_add", None)
        self._callback_del = kwargs.pop("callback_del", None)
        self._callback_move = kwargs.pop("callback_move", None)

        ttk.Frame.__init__(self, *args, **kwargs)
        # Setup Canvas
        self._max_x = self._canvaswidth - 10
        self._max_y = self._canvasheight - 10
        self.canvas = tk.Canvas(self, width=self._canvaswidth, height=self._canvasheight)
        self._image = None
        self._background = None
        # Setup event bindings
        self.canvas.tag_bind("item", "<ButtonPress-1>", self.left_press)
        self.canvas.tag_bind("item", "<ButtonRelease-1>", self.left_release)
        self.canvas.tag_bind("item", "<B1-Motion>", self.left_motion)
        self.canvas.tag_bind("item", "<ButtonPress-3>", self.right_press)
        self.canvas.bind("<ButtonPress-3>", self.right_press)
        # Setup item menu
        self.item_menu = tk.Menu(self, tearoff=0)
        self.item_menu.add_command(label="Delete", command=self.del_item)
        # Setup frame menu
        self.frame_menu = tk.Menu(self, tearoff=0)
        self.frame_menu.add_command(label="New", command=self._new_item)
        # Call grid_widgets last
        self.grid_widgets()

    def left_press(self, event):
        """
        Callback for the press of the left mouse button.

        Selects a new item and sets its highlightcolor.
        
        :param event: Tkinter event
        """
        self.current_coords = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.set_current()
        if self.current:
            self.canvas.itemconfigure(self.current, fill=self.item_colors[self.current][1])
            self.current = None
            return
        results = self.canvas.find_withtag(tk.CURRENT)
        if len(results) is 0:
            return
        self.current = results[0]
        self.canvas.itemconfigure(self.current, fill=self.item_colors[self.current][2])

    def left_release(self, event):
        """
        Callback for the release of the left button.

        :param event: Tkinter event
        """
        self.config(cursor="")
        if len(self.canvas.find_withtag("current")) != 0 and self.current is not None:
            self.canvas.itemconfigure(tk.CURRENT, fill=self.item_colors[self.current][1])

    def left_motion(self, event):
        """
        Callback for the B1-Motion event, or the dragging of an item.

        Moves the item to the desired location, but limits its movement to a
        place on the actual Canvas. The item cannot be moved outside of the Canvas.

        :param event: Tkinter event
        """
        self.set_current()
        results = self.canvas.find_withtag(tk.CURRENT)
        if len(results) is 0:
            return
        item = results[0]
        rectangle = self.items[item]
        self.config(cursor="exchange")
        self.canvas.itemconfigure(item, fill="blue")
        xc, yc = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        dx, dy = xc - self.current_coords[0], yc - self.current_coords[1]
        self.current_coords = xc, yc
        self.canvas.move(item, dx, dy)
        # check whether the new position of the item respects the boundaries
        x, y = self.canvas.coords(item)
        x, y = max(min(x, self._max_x), 0), max(min(y, self._max_y), 0)
        self.canvas.coords(item, x, y)
        self.canvas.coords(rectangle, self.canvas.bbox(item))

    def right_press(self, event):
        """
        Callback for the right mouse button event to pop up the correct menu.
        
        :param event: Tkinter event
        """
        self.set_current()
        current = self.canvas.find_withtag("current")
        if current and current[0] in self.canvas.find_withtag("item"):
            # Display item_menu
            self.current = current[0]
            self.item_menu.tk_popup(event.x_root, event.y_root)
        else:
            # Display frame_menu
            self.frame_menu.tk_popup(event.x_root, event.y_root)

    def grid_widgets(self):
        """Put the widgets in the correct position."""
        self.canvas.grid(sticky="nswe")

    def add_item(self, text, font=("default", 12, "bold"), backgroundcolor="yellow", textcolor="black",
                 highlightcolor="blue"):
        """
        Add a new item on the Canvas.
        
        :param text: text to display
        :type text: str
        :param font: font of the text
        :type font: tuple or :class:`~tkinter.font.Font`
        :param backgroundcolor: background color
        :type  backgroundcolor: str
        :param textcolor: text color
        :type  textcolor: str
        :param highlightcolor: the color of the text when the item is selected
        :type  highlightcolor: str
        """
        item = self.canvas.create_text(0, 0, anchor=tk.NW, text=text, font=font, fill=textcolor, tag="item")
        rectangle = self.canvas.create_rectangle(self.canvas.bbox(item), fill=backgroundcolor)
        self.canvas.tag_lower(rectangle, item)
        self.items[item] = rectangle
        if callable(self._callback_add):
            self._callback_add(item, rectangle)
        self.item_colors[item] = (backgroundcolor, textcolor, highlightcolor)

    def del_item(self):
        """Delete the current item on the Canvas."""
        item = self.current
        rectangle = self.items[item]
        self.canvas.delete(item, rectangle)
        if callable(self._callback_del):
            self._callback_del(item, rectangle)

    def _new_item(self):
        """Function that calls the user defined function to add a new item."""
        if callable(self._function_new):
            self._function_new(self.add_item)

    def set_background(self, image=None, path=None, resize=True):
        """
        Set the background image of the Canvas.
        
        :param image: background image
        :type image: PhotoImage
        :param path: background image path
        :type path: str
        :param resize: whether to resize the image to the Canvas size
        :type resize: bool
        """
        if not image and not path:
            raise ValueError("You must either pass a PhotoImage object or a path object")
        if image and path:
            raise ValueError("You must pass either a PhotoImage or str path, not both")
        if image is not None and not isinstance(image, tk.PhotoImage) and not isinstance(image, ImageTk.PhotoImage):
            raise ValueError("The image passed is not a PhotoImage object")
        if path is not None and not isinstance(path, str):
            raise ValueError("The image path passed is not of str type: {0}".format(path))
        if path and not os.path.exists(path):
            raise ValueError("The image path passed is not valid: {0}".format(path))
        if image is not None:
            self._image = image
        elif path is not None:
            img = Image.open(path)
            if resize:
                img = img.resize((self._canvaswidth, self._canvasheight), Image.ANTIALIAS)
            self._image = ImageTk.PhotoImage(img)
        self._background = self.canvas.create_image(0, 0, image=self._image, anchor=tk.NW, tag="background")
        self.canvas.tag_lower("background")

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method :meth:`~ItemsCanvas.keys`.
        """
        if key is "canvaswidth":
            return self._canvaswidth
        elif key is "canvasheight":
            return self._canvasheight
        elif key is "function_new":
            return self._function_new
        elif key is "callback_add":
            return self._callback_add
        elif key is "callback_del":
            return self._callback_del
        elif key is "callback_move":
            return self._callback_move
        else:
            ttk.Frame.cget(self, key)

    def config(self, **kwargs):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method :meth:`~ItemsCanvas.keys`.
        See :meth:`~ItemsCanvas.__init__` for a description of the widget specific option.
        """
        self._canvaswidth = kwargs.pop("canvaswidth", self._canvaswidth)
        self._canvasheight = kwargs.pop("canvasheight", self._canvasheight)
        self.canvas.config(width=self._canvaswidth, height=self._canvasheight)
        self._function_new = kwargs.pop("function_new", self._function_new)
        self._callback_add = kwargs.pop("callback_add", self._callback_add)
        self._callback_del = kwargs.pop("callback_del", self._callback_del)
        self._callback_move = kwargs.pop("callback_move", self._callback_move)
        ttk.Frame.config(self, **kwargs)

    configure = config

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, key, value):
        self.config(**{key: value})

    def keys(self):
        keys = ttk.Frame.keys(self)
        keys.extend([
            "canvaswidth",
            "canvasheight",
            "function_new",
            "callback_add",
            "callback_del",
            "callback_move"
        ])
        return keys

    def set_current(self):
        results = self.canvas.find_withtag(tk.CURRENT)
        if len(results) == 0:
            self.current = None
        else:
            self.current = results[0]
