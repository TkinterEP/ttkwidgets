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
from ttkwidgets.utilities import open_icon
from collections import OrderedDict
from math import floor


class TimeLine(ttk.Frame):
    """
    A Frame containing a Canvas and various buttons to manage a timeline that can be marked with certain events,
    allowing the binding of commands to hovering over certain elements and creating texts inside the elements.

    Each marker is pretty much a coloured rectangle with some optional text, that can be assigned tags. Tags may specify
    the colors of the marker, but tags can also be assigned callbacks that can be called with the identifier of the tag
    as well as a Tkinter event instance that was generated upon clicking. For example, the markers may be moved, or the
    user may want to add a menu that shows upon right-clicking. See the create_marker function for more details on the
    markers.

    The markers are put into a Canvas, which contains rows for each category. The categories are indicated by Labels and
    separated by black separating lines. Underneath the rows of categories, there is a second Canvas containing markers
    for the ticks of the time unit. Some time units get special treatment, such as "h" and "m", displayed in an
    appropriate H:M and M:S format respectively.

    The height of the row for each category is automatically adjusted to the height of its respective Label to give
    a uniform appearance. All markers are redrawn if the generate_canvas_contents is called, and therefore it should
    be called after any size change. Depending on the number of markers to draw, it may take a long time.

    The TimeLine can be scrolled in two ways: horizontally (with _scrollbar_timeline) and vertically (with
    _scrollbar_timeline_v), which both use a class function as a proxy to allow for other functions to be called upon
    scrolling. The horizontal scrollbar makes a small pop-up window appear to indicate the time the cursor is currently
    pointing at on the timeline.

    The markers can be retrieved from the class using the markers property, and they can be saved and then the markers
    can be recreated by calling create_marker again for each marker. This functionality is not built into the class,
    if the user wants to do something like this, he or she should write the code required, as it can be done in
    different ways.

    Some of the code has been inspired by the ItemsCanvas, as that is also a Canvas that supports the manipulation of
    items, but as this works in a fundamentally different way, the classes do not share any common parent class.

    This widget is *absolutely not* thread-safe, and it was not designed as such. It may work in some situations, but
    nothing is guaranteed when using this widget from multiple threads, even with Tkinter compiled with thread-safe
    flags or when using mtTkinter for Python 2.

    Some themes may conflict with this widget, for example because it makes the default font bigger for the category
    Labels. This should be fixed by the user by modifying the TimeLine.T(Widget) style.
    """

    def __init__(self, master=None, **kwargs):
        """
        Create a TimeLine widget

        Keyword Arguments:
            TimeLine options:
            * int width: width of the timeline in pixels                                    400
            * int height: height of the timeline in pixels                                  200
            * float start: value to start at                                                0.0
            * float finish: value to finish at                                              10.0
            * float resolution: amount of time per pixel                                    0.01
            * float tick_resolution: amount of time between ticks                           1.0
            * str unit: unit of time, some units have predefined properties, such           "s"
                as minutes ("m") and hours ("h"), which make the tick markers have
                an appropriate format
            * bool zoom_enabled: whether to allow zooming with the buttons                  True
            * dict categories: a dictionary with the names of the categories as             {}
                the keys and keyword argument dictionaries as the values
            * str background: Tkinter-compatible background color for the Canvas            "white"
            * str style: Style for the Frame widget                                         "TimeLine.TFrame"
            * tuple int zoom_factors: tuple of zoom levels, for example (1, 2, 5)           (1, 2, 5)
                means zoom levels of 1x, 2x and 5x are supported
            Marker options:
            * tuple marker_font: font tuple to specify the default font for the             ("default", 10)
                markers
            * str marker_background: Tkinter-compatible default background color            "lightblue"
                for the markers
            * str marker_foreground: Tkinter-compatible default foreground color            "black"
                for the markers

        The style of the buttons can be modified by using the "TimeLine.TButton" style.
        The style of the surrounding Frame can be modified by using the "TimeLine.TFrame" style, or by specifying
            another style in the keyword arguments.
        The style of the category Labels can be modified by using the "TimeLine.TLabel" style.
        """
        # Keyword argument processing
        self._width = kwargs.pop("width", 400)
        self._height = kwargs.pop("height", 200)
        self._start = kwargs.pop("start", 0.0)
        self._finish = kwargs.pop("finish", 10.0)
        self._resolution = kwargs.pop("resolution", 0.01)
        self._tick_resolution = kwargs.pop("tick_resolution", 1.0)
        self._unit = kwargs.pop("unit", "s")
        self._zoom_enabled = kwargs.pop("zoom_enabled", True)
        self._zoom_factors = kwargs.pop("zoom_factors", (1, 2, 5))
        self._categories = kwargs.pop("categories", {})
        self._background = kwargs.pop("background", "gray90")
        self._style = kwargs.get("style", "TimeLine.TFrame")
        kwargs["style"] = self._style
        self._marker_font = kwargs.pop("marker_font", ("default", 10))
        self._marker_background = kwargs.pop("marker_background", "lightblue")
        self._marker_foreground = kwargs.pop("marker_foreground", "black")
        # Check the arguments
        self.check_kwargs()
        # Set up the style
        self.style = ttk.Style()
        self.style.configure(self._style, background=self._background)
        # Initialize the Frame
        ttk.Frame.__init__(self, master, **kwargs)

        # Open icons
        self._image_zoom_in = open_icon("zoom_in.png")
        self._image_zoom_out = open_icon("zoom_out.png")
        self._image_zoom_reset = open_icon("zoom_reset.png")

        # Create necessary attributes
        self._zoom_factor = self._zoom_factors[0]
        self._markers = {category: {} for category in self._categories.keys()}
        self._canvas_markers = {}  # Canvas ID: (category, marker_iid)
        self._markers_canvas = {}  # marker_iid: (canvas_rectangle_id, canvas_text_id)
        self._iid = 0
        self._tags = {}
        self._rows = {}

        # Create the child widgets

        # Frames
        self._canvas_categories = tk.Canvas(self, background=self._background, height=self._height,
                                            borderwidth=0)
        self._canvas_ticks = tk.Canvas(self, background=self._background, width=self._width, height=30,
                                       borderwidth=0)
        self._frame_zoom = ttk.Frame(self, style=self._style)
        self._frame_categories = ttk.Frame(self._canvas_categories, style=self._style)
        # Zoom buttons
        self._button_zoom_in = ttk.Button(self._frame_zoom, image=self._image_zoom_in, command=self.zoom_in,
                                          state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)
        self._button_zoom_out = ttk.Button(self._frame_zoom, image=self._image_zoom_out, command=self.zoom_out,
                                           state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)
        self._button_zoom_reset = ttk.Button(self._frame_zoom, image=self._image_zoom_reset, command=self.zoom_reset,
                                             state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)
        # Category Labels
        self._category_labels = OrderedDict()
        canvas_width = 0
        for category, kwargs in (sorted(self._categories.items())
                                 if not isinstance(self._categories, OrderedDict)
                                 else self._categories):
            kwargs["background"] = kwargs.get("background", self._background)
            kwargs["justify"] = kwargs.get("justify", tk.LEFT)
            label = ttk.Label(self._frame_categories, **kwargs)
            width = label.winfo_reqwidth()
            canvas_width = width if width > canvas_width else canvas_width
            self._category_labels[category] = label
        self._canvas_categories.create_window(0, 0, window=self._frame_categories, anchor=tk.NW)
        self._canvas_categories.config(width=canvas_width, height=self._height)
        # Canvas widgets
        self._canvas_scroll = tk.Canvas(self, background=self._background, width=self._width, height=self._height)
        self._timeline = tk.Canvas(self._canvas_scroll, background=self._background, borderwidth=0)
        self._timeline_id = self._canvas_scroll.create_window(0, 0, window=self._timeline, anchor=tk.NW)
        self._scrollbar_timeline = ttk.Scrollbar(self, command=self.set_scroll, orient=tk.HORIZONTAL)
        self._scrollbar_vertical = ttk.Scrollbar(self, command=self.set_scroll_v, orient=tk.VERTICAL)
        self._canvas_scroll.config(xscrollcommand=self._scrollbar_timeline.set,
                                   yscrollcommand=self._scrollbar_vertical.set)
        self._canvas_categories.config(yscrollcommand=self._scrollbar_vertical.set)
        # Event bindings
        self._timeline.bind("<Configure>", self.__configure_timeline)

        self.generate_timeline_contents()
        self.grid_widgets()

    def grid_widgets(self):
        """
        Put all the child widgets of this super-widget in place
        """
        # Categories
        for index, label in enumerate(self._category_labels.values()):
            label.grid(column=0, row=index, padx=5, sticky="nw")
        # Canvas widgets
        self._canvas_scroll.grid(column=1, row=0, padx=(0, 5), pady=5, sticky="nswe")
        self._canvas_ticks.grid(column=1, row=1, padx=(0, 5), pady=(0, 5), sticky="nswe")
        self._scrollbar_timeline.grid(column=1, row=2, padx=(0, 5), pady=(0, 5), sticky="we")
        # Zoom widgets
        self._button_zoom_in.grid(row=0, column=0, pady=5, sticky="nswe")
        self._button_zoom_out.grid(row=1, column=0, pady=(0, 5), sticky="nswe")
        self._button_zoom_reset.grid(row=2, column=0, pady=(0, 5), sticky="nswe")
        # Frames
        self._canvas_categories.grid(column=0, row=0, padx=5, pady=5, sticky="nswe")
        self._scrollbar_vertical.grid(column=2, row=0, pady=5, padx=(0, 5), sticky="ns")
        self._frame_zoom.grid(column=3, row=0, rowspan=2, padx=(0, 5), pady=5, sticky="nswe")

    # Canvas related functions

    @property
    def pixel_width(self):
        """
        The width of the whole TimeLine in pixels (so not just the visible part)
        """
        return self.zoom_factor * ((self._finish - self._start) / self._resolution)

    def generate_timeline_contents(self):
        """
        Generate all the contents of the Canvas, including time tick markers and all markers in the categories
        """
        # Configure the canvas
        self.clear_timeline()
        self.create_scroll_regions()
        self.create_scroll_region()
        self._timeline.config(width=self.pixel_width)
        # Generate the Y-coordinates for each of the rows and create the lines indicating the rows
        self.create_separating_lines()
        # Create the markers on the timeline
        self.create_markers(self.markers)
        # Create the ticks in the _canvas_ticks
        self.create_ticks()

    def create_scroll_region(self):
        """
        Set the correct scroll regions for the categories Canvas
        """
        canvas_width = 0
        canvas_height = 0
        for label in self._category_labels.values():
            width = label.winfo_reqwidth()
            canvas_height += label.winfo_reqheight()
            canvas_width = width if width > canvas_width else canvas_width
        self._canvas_categories.config(scrollregion="0 0 {0} {1}".format(canvas_width, canvas_height))

    def get_time_position(self, time):
        """
        Get the location as a pixel coordinate (only the x-coordinate) of a certain time value
        """
        if time < self._start or time > self._finish:
            raise ValueError("time argument out of bounds")
        return (time - self._start) / (self._resolution / self._zoom_factor)

    def clear_timeline(self):
        """
        Delete all items in the Canvas, does not modify the categories
        """
        self._timeline.delete(tk.ALL)
        self._canvas_ticks.delete(tk.ALL)

    def create_ticks(self):
        """
        Create the tick markers in the ticks canvas
        """
        self._canvas_ticks.create_line((0, 10, self.pixel_width, 10), fill="black")
        ticks = list(TimeLine.range(self._start, self._finish, self._tick_resolution / self._zoom_factor))
        for tick in ticks:
            string = TimeLine.get_time_string(tick, self._unit)
            x = self.get_time_position(tick)
            self._canvas_ticks.create_text((x, 20), text=string, fill="black", font=("default", 10))
            self._canvas_ticks.create_line((x, 5, x, 15), fill="black")
        self._canvas_ticks.config(scrollregion="0 0 {0} {1}".format(self.pixel_width, 30))

    def create_separating_lines(self):
        """
        Create the lines separating the different category rows in the TimeLine's Canvas
        """
        total = 0
        for category, label in self._category_labels.items():
            height = label.winfo_reqheight()
            self._rows[category] = (total, total + height)
            total += height
            self._timeline.create_line((0, total, self.pixel_width, total))
        pixel_height = total
        self._timeline.config(height=pixel_height)

    def create_markers(self, markers):
        """
        Create all the markers in a given category dictionary, as in the markers property
        """
        for category, category_markers in markers.items():
            for marker in category_markers.values():
                self.create_marker(category, marker["start"], marker["finish"], **marker)
        return

    def create_marker(self, category_v, start_v, finish_v, **kwargs):
        """
        Create a new marker in the TimeLine with the specified properties

        For the *args, _v appendixes are used in order not to conflict with a marker dictionary as found in
        self._markers

        :param category_v: Category identifier (not text!)
        :param start_v: Start time for the marker
        :param finish_v: Finish time for the marker
        :return: rectangle id, text id (the latter is None when text is None)
        :raise ValueError: One of the specified arguments is invalid

        Keyword Arguments:
            * str text: a text label to show in the marker, may not be displayed fully if the zoom level does not allow
                it. Updates when resizing.
            * str background: Tkinter-compatible background color for the marker
            * str foreground: Tkinter-compatible text color for the marker
            * str outline: Tkinter-compatible outline color for the marker
            * tuple font: Tkinter-compatible font tuple to set for the text of the marker
            * str iid: unique marker identifier used by the internal code
            * tuple tags: set of tags to apply to this marker, allowing callbacks to be set and other properties
        """
        if category_v not in self._categories:
            raise ValueError("category argument not a valid category: {}".format(category_v))
        if start_v < self._start or finish_v > self._finish:
            raise ValueError("time out of bounds")
        iid = kwargs.pop("iid", self._iid)
        background = kwargs.get("background", self._marker_background)
        foreground = kwargs.get("foreground", self._marker_foreground)
        outline = kwargs.get("outline", "black")
        font = kwargs.get("font", self._marker_font)
        tags = kwargs.get("tags", ())
        # Calculate pixel positions
        start_pixel = start_v / self._resolution * self._zoom_factor
        finish_pixel = finish_v / self._resolution * self._zoom_factor
        y_start_pixel, y_finish_pixel = self._rows[category_v]
        # Create the rectangle
        rectangle = self._timeline.create_rectangle(
            (start_pixel, y_start_pixel, finish_pixel, y_finish_pixel), fill=background, outline=outline
        )
        # Create the text
        text = kwargs.get("text", None)
        if text is not None:
            text_id = self._timeline.create_text((0, 0), text=text, fill=foreground, font=font)
            x = start_pixel - (start_pixel - finish_pixel) / 2
            y = y_start_pixel - (y_start_pixel - y_finish_pixel) / 2
            self._timeline.coords(text_id, (x, y))
        else:
            text_id = None
        # Save the marker
        self._markers[category_v][iid] = {
            "text": text,
            "foreground": foreground,
            "background": background,
            "outline": outline,
            "font": font,
            "iid": iid,
            "tags": tags,
            "rectangle_id": rectangle,
            "text_id": text_id,
            "category": category_v,
            "start": start_v,
            "finish": finish_v
        }

        self._iid += 1

    def tag_configure(self):
        pass

    def set_zoom_factor(self):
        pass

    def set_scroll(self, *args):
        """
        Proxy for the xview function of the TimeLine Canvas, displays the value of the scroll in time units.
        """
        self._canvas_scroll.xview(*args)
        self._canvas_ticks.xview(*args)

    def __configure_timeline(self, *args):
        """
        Function from ScrolledFrame, adapted for the _timeline
        """
        # Resize the canvas scrollregion to fit the entire frame
        (size_x, size_y) = (self._timeline.winfo_reqwidth(), self._timeline.winfo_reqheight())
        self._canvas_scroll.config(scrollregion="0 0 {0} {1}".format(size_x, size_y))

    # Zoom button functions

    def zoom_in(self):
        """
        Callback for the _button_zoom_in, to update the current zoom factor and then redraw the Canvas
        """
        index = self._zoom_factors.index(self._zoom_factor)
        if index + 1 == len(self._zoom_factors):
            # Already zoomed in all the way
            return
        self._zoom_factor = self._zoom_factors[index + 1]
        self.generate_timeline_contents()

    def zoom_out(self):
        """
        Callback for the _button_zoom_out, to update the current zoom factor and then redraw the Canvas
        """
        index = self._zoom_factors.index(self._zoom_factor)
        if index == 0:
            # Already zoomed out all the way
            return
        self._zoom_factor = self._zoom_factors[index - 1]
        self.generate_timeline_contents()

    def zoom_reset(self):
        """
        Callback for the _button_zoom_reset, to reset the zoom level to its initial value, and then redraw the Canvas
        """
        self._zoom_factor = self._zoom_factors[0]
        self.generate_timeline_contents()

    def set_scroll_v(self, *args):
        """
        Proxy for the two yview functions that should be called upon scrolling vertically
        """
        self._canvas_categories.yview(*args)
        self._canvas_scroll.yview(*args)

    @property
    def markers(self):
        """
        Return a dictionary with categories as keys
        """
        return self._markers

    @property
    def zoom_factor(self):
        """
        Return the current zoom factor
        """
        return self._zoom_factor

    def check_kwargs(self):
        """
        Checks the type and values of the keyword arguments that have been set to attributes in __init__.
        :return: None
        :raise: ValueError or TypeError if an argument does not satisfy the conditions
        """
        # width, height
        if not isinstance(self._width, int) or not isinstance(self._height, int):
            raise TypeError("width and/or height arguments not of int type")
        if not self._width > 0 or not self._height > 0:
            raise ValueError("width and/or height arguments not larger than zero")
        # start, finish
        if not isinstance(self._start, float) or not isinstance(self._finish, float):
            raise TypeError("start and/or finish arguments not of float type")
        # resolutions
        if not isinstance(self._resolution, float) or not isinstance(self._tick_resolution, float):
            raise TypeError("resolution and/or tick_resolution arguments not of float type")
        if not self._resolution > 0 or not self._tick_resolution > 0:
            raise ValueError("resolution and/or tick_resolution arguments not larger than zero")
        # unit
        if not isinstance(self._unit, str):
            raise TypeError("unit argument not of str type")
        # zoom
        if not isinstance(self._zoom_enabled, bool):
            raise TypeError("zoom_enabled argument not of bool type")
        if not isinstance(self._zoom_factors, tuple):
            raise TypeError("zoom_factors argument not of tuple type")
        if not len(self._zoom_factors) > 0:
            raise ValueError("zoom_factors argument is empty tuple")
        if sum(1 for factor in self._zoom_factors if isinstance(factor, (int, float))) != len(self._zoom_factors):
            raise ValueError("one or more values in zoom_factors argument not of int type")
        # categories
        if not isinstance(self._categories, dict):
            raise TypeError("categories argument not of dict type")
        if (sum(1 for cat, val in self._categories.items() if isinstance(cat, str) and isinstance(val, dict)) !=
                len(self._categories)):
            raise ValueError("one or more keys not str type or values not dict type in categories argument")
        # background
        if not isinstance(self._background, str):
            raise TypeError("background argument not of str type")
        # marker options
        if not isinstance(self._marker_font, tuple) or len(self._marker_font) == 0:
            raise ValueError("marker_font argument not a valid font tuple")
        if not isinstance(self._marker_background, str) or not isinstance(self._marker_foreground, str):
            raise TypeError("marker_background and/or marker_foreground argument(s) not of str type")
        return

    @staticmethod
    def get_time_string(time, unit):
        """
        Return a properly formatted string for a given time value and unit.
        """
        supported_units = ["h", "m"]
        if unit not in supported_units:
            return "{}".format(time)
        hours, minutes = str(time).split(".")
        hours = int(hours)
        minutes = int(round(float(minutes) * 60))
        return "{:02d}:{:02d}".format(hours, minutes)

    @staticmethod
    def range(start, finish, step):
        """
        Like built-in range(), but with float support
        """
        value = start
        while value <= finish:
            yield value
            value += step

