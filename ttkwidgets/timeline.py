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
from ttkwidgets import AutoHideScrollbar


class TimeLine(ttk.Frame):
    """
    A Frame containing a Canvas and various buttons to manage a timeline
    that can be marked with certain events, allowing the binding of
    commands to hovering over certain elements and creating texts inside
    the elements.

    Each marker is pretty much a coloured rectangle with some optional
    text, that can be assigned tags. Tags may specify the colors of the
    marker, but tags can also be assigned callbacks that can be called
    with the identifier of the tag as well as a Tkinter event instance
    that was generated upon clicking. For example, the markers may be
    moved, or the user may want to add a menu that shows upon
    right-clicking. See the :meth:`create_marker` function for more details on
    the markers.

    The markers are put into a Canvas, which contains rows for each
    category. The categories are indicated by Labels and separated by
    black separating lines. Underneath the rows of categories, there is
    a second Canvas containing markers for the ticks of the time unit.
    Some time units get special treatment, such as "h" and "m",
    displayed in an appropriate H:M and M:S format respectively.

    The height of the row for each category is automatically adjusted to
    the height of its respective Label to give a uniform appearance.
    All markers are redrawn if :meth:`draw_timeline` is called,
    and therefore it should be called after any size change. Depending
    on the number of markers to draw, it may take a long time.

    The TimeLine can be scrolled in two ways: horizontally (with
    :obj:`_scrollbar_timeline`) and vertically (with :obj:`_scrollbar_timeline_v`),
    which both use a class function as a proxy to allow for other
    functions to be called upon scrolling. The horizontal scrollbar
    makes a small pop-up window appear to indicate the time the cursor
    is currently pointing at on the timeline.

    The markers can be retrieved from the class using the markers
    property, and they can be saved and then the markers can be
    recreated by calling :meth:`create_marker` again for each marker. This
    functionality is not built into the class, if the user wants to do
    something like this, he or she should write the code required, as it
    can be done in different ways.

    Some of the code has been inspired by the :class:`ItemsCanvas`, as that is
    also a Canvas that supports the manipulation of items, but as this
    works in a fundamentally different way, the classes do not share any
    common parent class.

    .. warning::
         This widget is *absolutely not* thread-safe, and it was not designed
         as such. It may work in some situations, but nothing is guaranteed
         when using this widget from multiple threads, even with Tkinter
         compiled with thread-safe flags or when using mtTkinter for
         Python 2.

    .. note::
         Some themes may conflict with this widget, for example because it
         makes the default font bigger for the category Labels. This should
         be fixed by the user by modifying the "TimeLine.T(Widget)" style.
    """

    def __init__(self, master=None, **kwargs):
        """
        Create a TimeLine widget

        The style of the buttons can be modified by using the
        "TimeLine.TButton" style.
        The style of the surrounding Frame can be modified by using the
        "TimeLine.TFrame" style, or by specifying another style in the
        keyword arguments.
        The style of the category Labels can be modified by using the
        "TimeLine.TLabel" style.

        **Base TimeLine Widget Options**

        :param width: Width of the timeline in pixels
        :type width: int
        :param height: Height of the timeline in pixels
        :type height: int
        :param extend: Whether to extend when an item is moved out of
            range
        :type extend: bool
        :param start: Value to start the timeline at
        :type start: float
        :param finish: Value to end the timeline at
        :type finish: float
        :param resolution: Amount of time per pixel [s/pixel]
        :type resolution: int
        :param tick_resolution: Amount of time between ticks on the
            timeline
        :type tick_resolution: int
        :param unit: Unit of time. Some units have predefined
            properties, such as minutes ('m') and hours ('h'), which
            make the tick markers have an appropriate format.
        :type unit: str
        :param zoom_enabled: Whether to allow zooming on the timeline
            using the zoom buttons
        :type zoom_enabled: bool
        :param categories: A dictionary with the names of the categories
            as the keys and the keyword argument dictionaries as values.
            Use an :obj:`OrderedDict` in order to preserve category
            order.
        :type categories: dict[Any, dict]
        :param background: Background color for the Canvas widget
        :type background: str
        :param style: Style to apply to the Frame widget
        :type style: str
        :param zoom_factors: Tuple of allowed zoom levels. For example:
            (1.0, 2.0, 5.0). The order of zoom levels is preserved.
        :type zoom_factors: tuple[float]
        :param zoom_default: Default zoom level to apply to the timeline
        :type zoom_default: float
        :param snap_margin: Amount of pixels between start and/or finish
            of a marker and a tick on the timeline before the marker is
            snapped into place
        :type snap_margin: int
        :param menu: Menu to show when a right-click is performed
            somewhere on the TimeLine without a marker being active
        :type menu: tk.Menu
        :param autohidescrollbars: whether to use :class:`~ttkwidgets.AutoHideScrollbar`
            or :class:`ttk.Scrollbar` for the scrollbars
        :type autohidescrollbars: bool

        **Marker Default Options**

        :param marker_font: Font tuple to specify the default font for
            the markers
        :type marker_font: tuple
        :param marker_background: Default background color for markers
        :type marker_background: str
        :param marker_foreground: Default foreground color for markers
        :type marker_foreground: str
        :param marker_outline: Default outline color for the markers
        :type marker_outline: str
        :param marker_border: Border width in pixels
        :type marker_border: int
        :param marker_move: Whether markers are allowed to move by
            default
        :type marker_move: bool
        :param marker_change_category: Whether markers are allowed to
            change category by being dragged vertically
        :type marker_change_category: bool
        :param marker_allow_overlap: Whether the markers are allowed to
            overlap. This setting is only enforced on the marker being
            moved. This means that when inserting markers, no errors
            will be raised, even with overlaps, and when an
            overlap-allowing marker is moved over an overlap-disallowing
            marker and overlap will still occur.
        :type marker_allow_overlap: bool
        :param marker_snap_to_ticks: Whether the markers should snap to
            the ticks when moved close to ticks automatically
        """
        self.check_kwargs(kwargs)
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
        self._zoom_default = kwargs.pop("zoom_default", 0)
        self._categories = kwargs.pop("categories", {})
        self._background = kwargs.pop("background", "gray90")
        self._style = kwargs.get("style", "TimeLine.TFrame")
        self._extend = kwargs.pop("extend", False)
        self._snap_margin = kwargs.pop("snap_margin", 10)
        self._menu = kwargs.pop("menu", None)
        self._autohidescrollbars = kwargs.pop("autohidescrollbars", False)
        kwargs["style"] = self._style
        self._marker_font = kwargs.pop("marker_font", ("default", 10))
        self._marker_background = kwargs.pop("marker_background", "lightblue")
        self._marker_foreground = kwargs.pop("marker_foreground", "black")
        self._marker_outline = kwargs.pop("marker_outline", "black")
        self._marker_border = kwargs.pop("marker_border", 0)
        self._marker_move = kwargs.pop("marker_move", True)
        self._marker_change_category = kwargs.pop("marker_change_category", False)
        self._marker_allow_overlap = kwargs.pop("marker_allow_overlap", False)
        self._marker_snap_to_ticks = kwargs.pop("marker_snap_to_ticks", True)
        # Set up the style
        self.style = ttk.Style()
        self.style.configure(self._style, background=self._background)
        # Initialize the Frame
        ttk.Frame.__init__(self, master, **kwargs)

        # Open icons
        self._image_zoom_in = open_icon("zoom_in.png")
        self._image_zoom_out = open_icon("zoom_out.png")
        self._image_zoom_reset = open_icon("zoom_reset.png")
        self._time_marker = open_icon("marker.png")
        self._time_marker_image = None
        self._time_marker_line = None

        # Create necessary attributes
        self._zoom_factor = self._zoom_factors[0]
        self._markers = {}
        self._canvas_markers = {}  # Canvas ID: (category, marker_iid)
        self._iid = 0
        self._tags = {}
        self._rows = {}
        self._after_id = None
        self._active = None
        self._ticks = ()

        # Time pop-up frame
        self._time_label = None
        self._time_window = None
        self._time_visible = False

        # Create the child widgets

        # Frames
        self._canvas_categories = tk.Canvas(
            self, background=self._background, height=self._height, borderwidth=0)
        self._canvas_ticks = tk.Canvas(
            self, background=self._background, width=self._width, height=30, borderwidth=0)
        self._frame_zoom = ttk.Frame(self, style=self._style)
        self._frame_categories = ttk.Frame(self._canvas_categories, style=self._style)

        # Zoom buttons
        self._button_zoom_in = ttk.Button(
            self._frame_zoom, image=self._image_zoom_in, command=self.zoom_in,
            state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)
        self._button_zoom_out = ttk.Button(
            self._frame_zoom, image=self._image_zoom_out, command=self.zoom_out,
            state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)
        self._button_zoom_reset = ttk.Button(
            self._frame_zoom, image=self._image_zoom_reset, command=self.zoom_reset,
            state=tk.NORMAL if self._zoom_enabled else tk.DISABLED)

        # Category Labels
        self._category_labels = OrderedDict()
        self.draw_categories()

        # Canvas widgets
        self._canvas_scroll = tk.Canvas(self, background=self._background, width=self._width, height=self._height)
        self._timeline = tk.Canvas(self._canvas_scroll, background=self._background, borderwidth=0)
        self._timeline_id = self._canvas_scroll.create_window(0, 0, window=self._timeline, anchor=tk.NW)
        if self._autohidescrollbars:
            self._scrollbar_timeline = AutoHideScrollbar(self, command=self._set_scroll, orient=tk.HORIZONTAL)
            self._scrollbar_vertical = AutoHideScrollbar(self, command=self._set_scroll_v, orient=tk.VERTICAL)
        else:
            self._scrollbar_timeline = ttk.Scrollbar(self, command=self._set_scroll, orient=tk.HORIZONTAL)
            self._scrollbar_vertical = ttk.Scrollbar(self, command=self._set_scroll_v, orient=tk.VERTICAL)
        self._canvas_scroll.config(xscrollcommand=self._scrollbar_timeline.set,
                                   yscrollcommand=self._scrollbar_vertical.set)
        self._canvas_categories.config(yscrollcommand=self._scrollbar_vertical.set)

        self._setup_bindings()
        self.zoom_reset()
        self.draw_timeline()
        self.grid_widgets()

    def grid_widgets(self):
        """
        Configure all widgets using the grid geometry manager

        Automatically called by the :meth:`__init__` method.
        Does not have to be called by the user except in extraordinary
        cases.
        """
        # Categories
        for index, label in enumerate(self._category_labels.values()):
            label.grid(column=0, row=index, padx=5, sticky="nw", pady=(1, 0) if index == 0 else 0)
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

    def _setup_bindings(self):
        """
        Setup the event bindings for the widgets:
        Configure for _timeline
        Horizontal and Vertical scrolling for all widgets
        """
        self._timeline.bind("<Configure>", self.__configure_timeline)
        for widget in [self, self._canvas_scroll, self._timeline, self._canvas_categories]:
            widget.bind("<MouseWheel>", self._mouse_scroll_v)
            widget.bind("<Shift-MouseWheel>", self._mouse_scroll_h)
        # Callback bindings
        self._timeline.bind("<ButtonPress-1>", self._left_click)
        self._timeline.bind("<B1-Motion>", self._left_motion)
        self._timeline.bind("<ButtonPress-3>", self._right_click)
        self._timeline.tag_bind("marker", "<Enter>", self._enter_handler)
        self._timeline.tag_bind("marker", "<Leave>", self._leave_handler)
        self._canvas_ticks.bind("<B1-Motion>", self._time_marker_move)
        self._canvas_ticks.bind("<ButtonRelease-1>", self._time_marker_release)

    def draw_timeline(self):
        """Draw the contents of the whole TimeLine Canvas"""
        # Configure the canvas
        self.clear_timeline()
        self.create_scroll_region()
        self._timeline.config(width=self.pixel_width)
        self._canvas_scroll.config(width=self._width, height=self._height)
        # Generate the Y-coordinates for each of the rows and create the lines indicating the rows
        self.draw_separators()
        # Create the markers on the timeline
        self.draw_markers()
        # Create the ticks in the _canvas_ticks
        self.draw_ticks()
        self.draw_time_marker()

    def draw_time_marker(self):
        """Draw the time marker on the TimeLine Canvas"""
        self._time_marker_image = self._canvas_ticks.create_image((2, 16), image=self._time_marker)
        self._time_marker_line = self._timeline.create_line(
            (2, 0, 2, self._timeline.winfo_height()), fill="#016dc9", width=2)
        self._timeline.lift(self._time_marker_line)
        self._timeline.tag_lower("marker")

    def draw_categories(self):
        """Draw the category labels on the Canvas"""
        for label in self._category_labels.values():
            label.destroy()
        self._category_labels.clear()
        canvas_width = 0
        for category in (sorted(self._categories.keys() if isinstance(self._categories, dict) else self._categories)
                         if not isinstance(self._categories, OrderedDict)
                         else self._categories):
            kwargs = self._categories[category] if isinstance(self._categories, dict) else {"text": category}
            kwargs["background"] = kwargs.get("background", self._background)
            kwargs["justify"] = kwargs.get("justify", tk.LEFT)
            label = ttk.Label(self._frame_categories, **kwargs)
            width = label.winfo_reqwidth()
            canvas_width = width if width > canvas_width else canvas_width
            self._category_labels[category] = label
        self._canvas_categories.create_window(0, 0, window=self._frame_categories, anchor=tk.NW)
        self._canvas_categories.config(width=canvas_width + 5, height=self._height)

    def create_scroll_region(self):
        """Setup the scroll region on the Canvas"""
        canvas_width = 0
        canvas_height = 0
        for label in self._category_labels.values():
            width = label.winfo_reqwidth()
            canvas_height += label.winfo_reqheight()
            canvas_width = width if width > canvas_width else canvas_width
        self._canvas_categories.config(scrollregion="0 0 {0} {1}".format(canvas_width, canvas_height))

    def clear_timeline(self):
        """
        Clear the contents of the TimeLine Canvas

        Does not modify the actual markers dictionary and thus after
        redrawing all markers are visible again.
        """
        self._timeline.delete(tk.ALL)
        self._canvas_ticks.delete(tk.ALL)

    def draw_ticks(self):
        """Draw the time tick markers on the TimeLine Canvas"""
        self._canvas_ticks.create_line((0, 10, self.pixel_width, 10), fill="black")
        self._ticks = list(TimeLine.range(self._start, self._finish, self._tick_resolution / self._zoom_factor))
        for tick in self._ticks:
            string = TimeLine.get_time_string(tick, self._unit)
            x = self.get_time_position(tick)
            x_tick = x + 1 if x == 0 else (x - 1 if x == self.pixel_width else x)
            x_text = x + 15 if x - 15 <= 0 else (x - 15 if x + 15 >= self.pixel_width else x)
            self._canvas_ticks.create_text((x_text, 20), text=string, fill="black", font=("default", 10))
            self._canvas_ticks.create_line((x_tick, 5, x_tick, 15), fill="black")
        self._canvas_ticks.config(scrollregion="0 0 {0} {1}".format(self.pixel_width, 30))

    def draw_separators(self):
        """Draw the lines separating the categories on the Canvas"""
        total = 1
        self._timeline.create_line((0, 1, self.pixel_width, 1))
        for index, (category, label) in enumerate(self._category_labels.items()):
            height = label.winfo_reqheight()
            self._rows[category] = (total, total + height)
            total += height
            self._timeline.create_line((0, total, self.pixel_width, total))
        pixel_height = total
        self._timeline.config(height=pixel_height)

    def draw_markers(self):
        """Draw all created markers on the TimeLine Canvas"""
        self._canvas_markers.clear()
        for marker in self._markers.values():
            self.create_marker(marker["category"], marker["start"], marker["finish"], marker)

    def __configure_timeline(self, *args):
        """Function from ScrolledFrame, adapted for the _timeline"""
        # Resize the canvas scrollregion to fit the entire frame
        (size_x, size_y) = (self._timeline.winfo_reqwidth(), self._timeline.winfo_reqheight())
        self._canvas_scroll.config(scrollregion="0 0 {0} {1}".format(size_x, size_y - 5))

    def create_marker(self, category, start, finish, marker=None, **kwargs):
        """
        Create a new marker in the TimeLine with the specified options

        :param category: Category identifier, key as given in categories
            dictionary upon initialization
        :type category: Any
        :param start: Start time for the marker
        :type start: float
        :param finish: Finish time for the marker
        :type finish: float
        :param marker: marker dictionary (replaces kwargs)
        :type marker: dict[str, Any]

        **Marker Options**
        
        Options can be given either in the marker dictionary argument,
        or as keyword arguments. Given keyword arguments take precedence
        over tag options, which take precedence over default options.

        :param text: Text to show in the marker. Text may not be
            displayed fully if the zoom level does not allow the marker
            to be wide enough. Updates when resizing the marker.
        :type text: str
        :param background: Background color for the marker
        :type background: str
        :param foreground: Foreground (text) color for the marker
        :type foreground: str
        :param outline: Outline color for the marker
        :type outline: str
        :param border: The width of the border (for which outline is the
            color)
        :type border: int
        :param font: Font tuple to set for the marker
        :type font: tuple
        :param iid: Unique marker identifier to use. A marker is
            generated if not given, and its value is returned. Use this
            option if keeping track of markers in a different manner
            than with auto-generated iid's is necessary.
        :type iid: str
        :param tags: Set of tags to apply to this marker, allowing
            callbacks to be set and other options to be configured. The
            option precedence is from the first to the last item, so
            the options of the last item overwrite those of the one
            before, and those of the one before that, and so on.
        :type tags: tuple[str]
        :param move: Whether the marker is allowed to be moved
        :type move: bool

        Additionally, all the options with the ``marker_`` prefix from
        :meth:`__init__`, but without the prefix, are supported. Active state
        options are also available, with the ``active_`` prefix for
        ``background``, ``foreground``, ``outline``, ``border``. These
        options are also available for the hover state with the
        ``hover_`` prefix.

        :return: identifier of the created marker
        :rtype: str
        :raise ValueError: One of the specified arguments is invalid
        """
        kwargs = kwargs if marker is None else marker
        if category not in self._categories:
            raise ValueError("category argument not a valid category: {}".format(category))
        if start < self._start or finish > self._finish:
            raise ValueError("time out of bounds")
        self.check_marker_kwargs(kwargs)
        # Update the options based on the tags. The last tag always takes precedence over the ones before it, and the
        # marker specific options take precedence over tag options
        tags = kwargs.get("tags", ())
        options = kwargs.copy()
        # Check the tags
        for tag in tags:
            # Update the options
            kwargs.update(self._tags[tag])
        # Update with the specific marker options
        kwargs.update(options)
        # Process the other options
        iid = kwargs.pop("iid", str(self._iid))
        background = kwargs.get("background", "default")
        foreground = kwargs.get("foreground", "default")
        outline = kwargs.get("outline", "default")
        font = kwargs.get("font", "default")
        border = kwargs.get("border", "default")
        move = kwargs.get("move", "default")
        change_category = kwargs.get("change_category", "default")
        allow_overlap = kwargs.get("allow_overlap", "default")
        snap_to_ticks = kwargs.get("snap_to_ticks", "default")
        # Calculate pixel positions
        x1 = start / self._resolution * self._zoom_factor
        x2 = finish / self._resolution * self._zoom_factor
        y1, y2 = self._rows[category]
        # Create the rectangle
        rectangle_id = self._timeline.create_rectangle(
            (x1, y1, x2, y2),
            fill=background if background != "default" else self._marker_background,
            outline=outline if outline != "default" else self._marker_outline,
            tags=("marker",),
            width=border if border != "default" else self._marker_border
        )
        # Create the text
        text = kwargs.get("text", None)
        text_id = self._draw_text((x1, y1, x2, y2), text, foreground, font) if text is not None else None
        # Save the marker
        locals_ = locals()
        self._markers[iid] = {
            key: (
                locals_[key.replace("hover_", "").replace("active_", "")] if key in (
                    prefix + color for prefix in ["", "hover_", "active_"]
                    for color in ["background", "foreground", "outline", "border"]
                ) and key not in kwargs else (locals_[key] if key in locals_ else kwargs[key])
            ) for key in self.marker_options
        }
        # Save the marker's Canvas IDs
        self._canvas_markers[rectangle_id] = iid
        self._canvas_markers[text_id] = iid
        self._timeline.tag_lower("marker")
        # Attempt to prevent duplicate iids
        while str(self._iid) in self.markers:
            self._iid += 1
        return iid

    def _draw_text(self, coords, text, foreground, font):
        """Draw the text and shorten it if required"""
        if text is None:
            return None
        x1_r, _, x2_r, _ = coords
        while True:
            text_id = self._timeline.create_text(
                (0, 0), text=text,
                fill=foreground if foreground != "default" else self._marker_foreground,
                font=font if font != "default" else self._marker_font,
                tags=("marker",)
            )
            x1_t, _, x2_t, _ = self._timeline.bbox(text_id)
            if (x2_t - x1_t) < (x2_r - x1_r):
                break
            self._timeline.delete(text_id)
            text = text[:-4] + "..."
        x, y = TimeLine.calculate_text_coords(coords)
        self._timeline.coords(text_id, (x, y))
        return text_id

    def update_marker(self, iid, **kwargs):
        """
        Change the options for a certain marker and redraw the marker

        :param iid: identifier of the marker to change
        :type iid: str
        :param kwargs: Dictionary of options to update
        :type kwargs: dict
        :raises: ValueError
        """
        if iid not in self._markers:
            raise ValueError("Unknown iid passed as argument: {}".format(iid))
        self.check_kwargs(kwargs)
        marker = self._markers[iid]
        marker.update(kwargs)
        self.delete_marker(iid)
        return self.create_marker(marker["category"], marker["start"], marker["finish"], marker)

    def delete_marker(self, iid):
        """
        Delete a marker from the TimeLine

        :param iid: marker identifier
        :type iid: str
        """
        if iid == tk.ALL:
            for iid in self.markers.keys():
                self.delete_marker(iid)
            return
        options = self._markers[iid]
        rectangle_id, text_id = options["rectangle_id"], options["text_id"]
        del self._canvas_markers[rectangle_id]
        del self._canvas_markers[text_id]
        del self._markers[iid]
        self._timeline.delete(rectangle_id, text_id)

    def zoom_in(self):
        """Increase zoom factor and redraw TimeLine"""
        index = self._zoom_factors.index(self._zoom_factor)
        if index + 1 == len(self._zoom_factors):
            # Already zoomed in all the way
            return
        self._zoom_factor = self._zoom_factors[index + 1]
        if self._zoom_factors.index(self.zoom_factor) + 1 == len(self._zoom_factors):
            self._button_zoom_in.config(state=tk.DISABLED)
        self._button_zoom_out.config(state=tk.NORMAL)
        self.draw_timeline()

    def zoom_out(self):
        """Decrease zoom factor and redraw TimeLine"""
        index = self._zoom_factors.index(self._zoom_factor)
        if index == 0:
            # Already zoomed out all the way
            return
        self._zoom_factor = self._zoom_factors[index - 1]
        if self._zoom_factors.index(self._zoom_factor) == 0:
            self._button_zoom_out.config(state=tk.DISABLED)
        self._button_zoom_in.config(state=tk.NORMAL)
        self.draw_timeline()

    def zoom_reset(self):
        """Reset the zoom factor to default and redraw TimeLine"""
        self._zoom_factor = self._zoom_factors[0] if self._zoom_default == 0 else self._zoom_default
        if self._zoom_factors.index(self._zoom_factor) == 0:
            self._button_zoom_out.config(state=tk.DISABLED)
            self._button_zoom_in.config(state=tk.NORMAL)
        elif self._zoom_factors.index(self.zoom_factor) + 1 == len(self._zoom_factors):
            self._button_zoom_out.config(state=tk.NORMAL)
            self._button_zoom_in.config(state=tk.DISABLED)
        self.draw_timeline()

    def set_zoom_factor(self, factor):
        """
        Manually set a custom zoom factor

        :param factor: Custom zoom factor
        :type factor: float
        """
        self._zoom_factor = factor
        self.draw_timeline()

    def set_time(self, time):
        """
        Set the time marker to a specific time

        :param time: Time to set for the time marker on the TimeLine
        :type time: float
        """
        x = self.get_time_position(time)
        _, y = self._canvas_ticks.coords(self._time_marker_image)
        self._canvas_ticks.coords(self._time_marker_image, x, y)
        self._timeline.coords(self._time_marker_line, x, 0, x, self._timeline.winfo_height())

    def _time_marker_move(self, event):
        """Callback for <B1-Motion> Event: Move the selected marker"""
        limit = self.pixel_width
        x = self._canvas_ticks.canvasx(event.x)
        x = min(max(x, 0), limit)
        _, y = self._canvas_ticks.coords(self._time_marker_image)
        self._canvas_ticks.coords(self._time_marker_image, x, y)
        self._timeline.coords(self._time_marker_line, x, 0, x, self._timeline.winfo_height())
        self._time_show()

    def _time_marker_release(self, event):
        """Callback for <B1-Release> Event: Hide time marker window"""
        if not self._time_visible:
            return
        self._time_label.destroy()
        self._time_window.destroy()
        self._time_label = None
        self._time_window = None
        self._time_visible = False

    def _time_show(self):
        """Show the time marker window"""
        if not self._time_visible:
            self._time_visible = True
            self._time_window = tk.Toplevel(self)
            self._time_window.attributes("-topmost", True)
            self._time_window.overrideredirect(True)
            self._time_label = ttk.Label(self._time_window)
            self._time_label.grid()
            self._time_window.lift()
        x, y = self.master.winfo_pointerxy()
        geometry = "{0}x{1}+{2}+{3}".format(
            self._time_label.winfo_width(),
            self._time_label.winfo_height(),
            x - 15,
            self._canvas_ticks.winfo_rooty() - 10)
        self._time_window.wm_geometry(geometry)
        self._time_label.config(text=TimeLine.get_time_string(self.time, self._unit))

    def tag_configure(self, tag_name, **kwargs):
        """
        Create a marker tag

        :param tag_name: Identifier for the tag

        :param move_callback: Callback to be called upon moving a
            marker. Arguments to callback:
            ``(iid: str, (old_start: float, old_finish: float),
            (new_start: float, new_finish: float))``
        :type move_callback: callable
        :param left_callback: Callback to be called upon left clicking
            a marker. Arguments to callback:
            ``(iid: str, x_coord: int, y_coord: int)``
        :type left_callback: callable
        :param right_callback: Callback to be called upon right clicking
            a marker. Arguments to callback:
            ``(iid: str, x_coord: int, y_coord: int)``
        :type right_callback: callable
        :param menu: A Menu widget to show upon right click. Can be
            used with the right_callback option simultaneously.
        :type menu: tk.Menu

        In addition, supports all options supported by markers. Note
        that tag options are applied to markers upon marker creation,
        and thus is a tag is updated, the markers are not automatically
        updated as well.
        """
        callbacks = [
            kwargs.get("move_callback", None),
            kwargs.get("left_callback", None),
            kwargs.get("right_callback", None)
        ]
        for callback in callbacks:
            if callback is not None and not callable(callback):
                raise ValueError("One or more callbacks is not a callable object")
        self._tags[tag_name] = kwargs

    def marker_tags(self, iid):
        """Generator for all the tags of a certain marker"""
        tags = self._markers[iid]["tags"]
        for tag in tags:
            yield tag

    def _set_scroll_v(self, *args):
        """Scroll both categories Canvas and scrolling container"""
        self._canvas_categories.yview(*args)
        self._canvas_scroll.yview(*args)

    def _mouse_scroll_h(self, event):
        """Callback <Shift-MouseWheel> event for horizontal scrolling"""
        args = (int(-1 * (event.delta / 120)), "units")
        self._canvas_scroll.xview_scroll(*args)
        self._canvas_ticks.xview_scroll(*args)

    def _mouse_scroll_v(self, event):
        """Callback for <MouseWheel> event for vertical scrolling"""
        args = (int(-1 * (event.delta / 120)), "units")
        self._canvas_scroll.yview_scroll(*args)
        self._canvas_categories.yview_scroll(*args)

    def _set_scroll(self, *args):
        """Set horizontal scroll of scroll container and ticks Canvas"""
        self._canvas_scroll.xview(*args)
        self._canvas_ticks.xview(*args)

    def get_time_position(self, time):
        """
        Get x-coordinate for given time

        :param time: Time to determine x-coordinate on Canvas for
        :type time: float
        :return: X-coordinate for the given time
        :rtype: int
        :raises: ValueError
        """
        if time < self._start or time > self._finish:
            raise ValueError("time argument out of bounds")
        return (time - self._start) / (self._resolution / self._zoom_factor)

    def get_position_time(self, position):
        """
        Get time for x-coordinate

        :param position: X-coordinate position to determine time for
        :type position: int
        :return: Time for the given x-coordinate
        :rtype: float
        """
        return self._start + position * (self._resolution / self._zoom_factor)

    @staticmethod
    def get_time_string(time, unit):
        """
        Create a properly formatted string given a time and unit

        :param time: Time to format
        :type time: float
        :param unit: Unit to apply format of. Only supports hours ('h')
            and minutes ('m').
        :type unit: str
        :return: A string in format '{whole}:{part}'
        :rtype: str
        """
        supported_units = ["h", "m"]
        if unit not in supported_units:
            return "{}".format(round(time, 2))
        hours, minutes = str(time).split(".")
        hours = int(hours)
        minutes = int(round(float("0.{}".format(minutes)) * 60))
        return "{:02d}:{:02d}".format(hours, minutes)

    def _right_click(self, event):
        """Function bound to right click event for marker canvas"""
        iid = self.current_iid
        if iid is None:
            if self._menu is not None:
                self._menu.post(event.x, event.y)
            return
        args = (iid, (event.x_root, event.y_root))
        self.call_callbacks(iid, "right_callback", args)
        tags = list(self.marker_tags(iid))
        if len(tags) == 0:
            return
        menu = self._tags[tags[-1]].get("menu", None)
        if menu is None or not isinstance(menu, tk.Menu):
            return
        menu.post(event.x_root, event.y_root)

    def _left_click(self, event):
        """Function bound to left click event for marker canvas"""
        self.update_active()
        iid = self.current_iid
        if iid is None:
            return
        args = (iid, event.x_root, event.y_root)
        self.call_callbacks(iid, "left_callback", args)

    def _left_motion(self, event):
        """Function bound to move event for marker canvas"""
        iid = self.current_iid
        if iid is None:
            return
        marker = self._markers[iid]
        if marker["move"] is False:
            return
        delta = marker["finish"] - marker["start"]
        # Limit x to 0
        x = max(self._timeline.canvasx(event.x), 0)
        # Check if the timeline needs to be extended
        limit = self.get_time_position(self._finish - delta)
        if self._extend is False:
            x = min(x, limit)
        elif x > limit:  # self._extend is True
            self.configure(finish=(self.get_position_time(x) + (marker["finish"] - marker["start"])) * 1.1)
        # Get the new start value
        start = self.get_position_time(x)
        finish = start + (marker["finish"] - marker["start"])
        rectangle_id, text_id = marker["rectangle_id"], marker["text_id"]
        if rectangle_id not in self._timeline.find_all():
            return
        x1, y1, x2, y2 = self._timeline.coords(rectangle_id)
        # Overlap protection
        allow_overlap = marker["allow_overlap"]
        allow_overlap = self._marker_allow_overlap if allow_overlap == "default" else allow_overlap
        if allow_overlap is False:
            for marker_dict in self.markers.values():
                if marker_dict["allow_overlap"] is True:
                    continue
                if marker["iid"] != marker_dict["iid"] and marker["category"] == marker_dict["category"]:
                    if marker_dict["start"] < start < marker_dict["finish"]:
                        start = marker_dict["finish"] if start < marker_dict["finish"] else marker_dict["start"]
                        finish = start + (marker["finish"] - marker["start"])
                        x = self.get_time_position(start)
                        break
                    if marker_dict["start"] < finish < marker_dict["finish"]:
                        finish = marker_dict["finish"] if finish > marker_dict["finish"] else marker_dict["start"]
                        start = finish - (marker_dict["finish"] - marker_dict["start"])
                        x = self.get_time_position(start)
                        break
        # Vertical movement
        if marker["change_category"] is True or \
                (marker["change_category"] == "default" and self._marker_change_category):
            y = max(self._timeline.canvasy(event.y), 0)
            category = min(self._rows.keys(), key=lambda category: abs(self._rows[category][0] - y))
            marker["category"] = category
            y1, y2 = self._rows[category]
        # Snapping to ticks
        if marker["snap_to_ticks"] is True or (marker["snap_to_ticks"] == "default" and self._marker_snap_to_ticks):
            # Start is prioritized over finish
            for tick in self._ticks:
                tick = self.get_time_position(tick)
                # Start
                if abs(x - tick) < self._snap_margin:
                    x = tick
                    break
                # Finish
                x_finish = x + delta
                if abs(x_finish - tick) < self._snap_margin:
                    delta = self.get_time_position(marker["finish"] - marker["start"])
                    x = tick - delta
                    break
        rectangle_coords = (x, y1, x2 + (x - x1), y2)
        self._timeline.coords(rectangle_id, *rectangle_coords)
        if text_id is not None:
            text_x, text_y = TimeLine.calculate_text_coords(rectangle_coords)
            self._timeline.coords(text_id, text_x, text_y)
        if self._after_id is not None:
            self.after_cancel(self._after_id)
        args = (iid, (marker["start"], marker["finish"]), (start, finish))
        self._after_id = self.after(10, self._after_handler(iid, "move_callback", args))
        marker["start"] = start
        marker["finish"] = finish

    def _enter_handler(self, event):
        """Callback for :obj:`<Enter>` event on marker, to set hover options"""
        iid = self.current_iid
        if iid is None or iid == self.active:
            return
        self.update_state(iid, "hover")

    def _leave_handler(self, event):
        """Callback for :obj:`<Leave>` event on marker, to set normal options"""
        iid = self.current_iid
        if iid is None or self.active == iid:
            return
        self.update_state(iid, "normal")

    def update_state(self, iid, state):
        """
        Set a custom state of the marker

        :param iid: identifier of the marker to set the state of
        :type iid: str
        :param state: supports "active", "hover", "normal"
        :type state: str
        """
        if state not in ["normal", "hover", "active"]:
            raise ValueError("Invalid state: {}".format(state))
        marker = self._markers[iid]
        rectangle_id, text_id = marker["rectangle_id"], marker["text_id"]
        state = "" if state == "normal" else state + "_"
        colors = {}
        for color_type in ["background", "foreground", "outline", "border"]:
            value = marker[state + color_type]
            attribute = "_marker_{}".format(color_type)
            colors[color_type] = getattr(self, attribute) if value == "default" else value
        self._timeline.itemconfigure(rectangle_id, fill=colors["background"], width=colors["border"],
                                     outline=colors["outline"])
        self._timeline.itemconfigure(text_id, fill=colors["foreground"])

    def update_active(self):
        """Update the active marker on the marker Canvas"""
        if self.active is not None:
            self.update_state(self.active, "normal")
        if self.current_iid == self.active:
            self._active = None
            return
        self._active = self.current_iid
        if self.active is not None:
            self.update_state(self.active, "active")

    def _after_handler(self, iid, callback, args):
        """Proxy to called by after() in mainloop"""
        self._after_id = None
        self.update_state(iid, "normal")
        self.call_callbacks(iid, callback, args)

    def call_callbacks(self, iid, type, args):
        """
        Call the available callbacks for a certain marker

        :param iid: marker identifier
        :type iid: str
        :param type: type of callback (key in tag dictionary)
        :type type: str
        :param args: arguments for the callback
        :type args: tuple
        :return: amount of callbacks called
        :rtype: int
        """
        amount = 0
        for tag in self.marker_tags(iid):
            callback = self._tags[tag].get(type, None)
            if callback is not None:
                amount += 1
                callback(*args)
        return amount

    @property
    def time(self):
        """
        Current value the time marker is pointing to

        :rtype: float
        """
        x, _, = self._canvas_ticks.coords(self._time_marker_image)
        return self.get_position_time(x)

    @property
    def active(self):
        """
        Currently selected marker

        :rtype: str
        """
        return self._active

    @property
    def current(self):
        """
        Currently active item on the _timeline Canvas

        :rtype: str
        """
        results = self._timeline.find_withtag(tk.CURRENT)
        return results[0] if len(results) != 0 else None

    @property
    def current_iid(self):
        """
        Currently active item's iid

        :rtype: str
        """
        current = self.current
        if current is None or current not in self._canvas_markers:
            return None
        return self._canvas_markers[current]

    @property
    def markers(self):
        """
        Return a dictionary with categories as keys

        :rtype: dict[str, dict[str, Any]]
        """
        return self._markers

    @property
    def zoom_factor(self):
        """
        Return the current zoom factor

        :rtype: float
        """
        return self._zoom_factor

    @property
    def pixel_width(self):
        """
        Width of the whole TimeLine in pixels

        :rtype: int
        """
        return self.zoom_factor * ((self._finish - self._start) / self._resolution)

    @property
    def options(self):
        """List of available options to :meth:`__init__`"""
        return [
            # TimeLine options
            "width", "height", "extend", "start", "finish", "resolution", "tick_resolution", "unit", "zoom_enabled",
            "categories", "background", "style", "zoom_factors", "zoom_default", "extend", "menu", "autohidescrollbars", "snap_margin",
            # Marker options
            "marker_font", "marker_background", "marker_foreground", "marker_outline", "marker_border", "marker_move",
            "marker_change_category", "marker_allow_overlap", "marker_snap_to_ticks"
        ]

    @property
    def marker_options(self):
        """List of available options to create_marker"""
        return ["category", "start", "finish", "text", "font", "iid", "tags", "move", "rectangle_id", "text_id",
                "allow_overlap", "change_category", "snap_to_ticks"] + \
               [prefix + item for prefix in ["hover_", "active_", ""]
                for item in ["background", "foreground", "outline", "border"]]

    def configure(self, cnf={}, **kwargs):
        """Update options of the TimeLine widget"""
        kwargs.update(cnf)
        TimeLine.check_kwargs(kwargs)
        scrollbars = 'autohidescrollbars' in kwargs
        for option in self.options:
            attribute = "_" + option
            setattr(self, attribute, kwargs.pop(option, getattr(self, attribute)))
        if scrollbars:
            self._scrollbar_timeline.destroy()
            self._scrollbar_vertical.destroy()
            if self._autohidescrollbars:
                self._scrollbar_timeline = AutoHideScrollbar(self, command=self._set_scroll, orient=tk.HORIZONTAL)
                self._scrollbar_vertical = AutoHideScrollbar(self, command=self._set_scroll_v, orient=tk.VERTICAL)
            else:
                self._scrollbar_timeline = ttk.Scrollbar(self, command=self._set_scroll, orient=tk.HORIZONTAL)
                self._scrollbar_vertical = ttk.Scrollbar(self, command=self._set_scroll_v, orient=tk.VERTICAL)
            self._canvas_scroll.config(xscrollcommand=self._scrollbar_timeline.set,
                                       yscrollcommand=self._scrollbar_vertical.set)
            self._canvas_categories.config(yscrollcommand=self._scrollbar_vertical.set)
            self._scrollbar_timeline.grid(column=1, row=2, padx=(0, 5), pady=(0, 5), sticky="we")
            self._scrollbar_vertical.grid(column=2, row=0, pady=5, padx=(0, 5), sticky="ns")
        ttk.Frame.configure(self, **kwargs)
        self.draw_timeline()

    config = configure

    def cget(self, item):
        """Return the value of an option"""
        return getattr(self, "_" + item) if item in self.options else ttk.Frame.cget(self, item)

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, key, value):
        return self.configure(key=value)

    def itemconfigure(self, iid, rectangle_options, text_options):
        """
        Configure options of items drawn on the Canvas

        Low-level access to the individual elements of markers and other
        items drawn on the timeline Canvas. All modifications are
        overwritten when the TimeLine is redrawn.
        """
        rectangle_id, text_id = self._markers[iid]["rectangle_id"], self._markers[iid]["text_id"]
        if len(rectangle_options) != 0:
            self._timeline.itemconfigure(rectangle_id, **rectangle_options)
        if len(text_options) != 0:
            self._timeline.itemconfigure(text_id, **text_options)

    @staticmethod
    def calculate_text_coords(rectangle_coords):
        """Calculate Canvas text coordinates based on rectangle coords"""
        return (int(rectangle_coords[0] + (rectangle_coords[2] - rectangle_coords[0]) / 2),
                int(rectangle_coords[1] + (rectangle_coords[3] - rectangle_coords[1]) / 2))

    @staticmethod
    def range(start, finish, step):
        """Like built-in :func:`~builtins.range`, but with float support"""
        value = start
        while value <= finish:
            yield value
            value += step

    @staticmethod
    def check_kwargs(kwargs):
        """
        Check the type and values of keyword arguments to :meth:`__init__`

        :param kwargs: Dictionary of keyword arguments
        :type kwargs: dict[str, Any]
        :raises: TypeError, ValueError
        """
        # width, height
        width = kwargs.get("width", 400)
        height = kwargs.get("height", 200)
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and/or height arguments not of int type")
        if not width > 0 or not height > 0:
            raise ValueError("width and/or height arguments not larger than zero")
        # start, finish
        start = kwargs.get("start", 0.0)
        finish = kwargs.get("finish", 10.0)
        if not isinstance(start, float) or not isinstance(finish, float):
            raise TypeError("start and/or finish arguments not of float type")
        # resolutions
        resolution = kwargs.get("resolution", 0.01)
        tick_resolution = kwargs.get("tick_resolution", 1.0)
        if not isinstance(resolution, float) or not isinstance(tick_resolution, float):
            raise TypeError("resolution and/or tick_resolution arguments not of float type")
        if not resolution > 0 or not tick_resolution > 0:
            raise ValueError("resolution and/or tick_resolution arguments not larger than zero")
        # unit
        unit = kwargs.get("unit", "")
        if not isinstance(unit, str):
            raise TypeError("unit argument not of str type")
        # zoom
        zoom_enabled = kwargs.get("zoom_enabled", True)
        zoom_factors = kwargs.get("zoom_factors", (1, 2, 5))
        zoom_default = kwargs.get("zoom_default", 0)
        if not isinstance(zoom_enabled, bool):
            raise TypeError("zoom_enabled argument not of bool type")
        if not isinstance(zoom_factors, tuple):
            raise TypeError("zoom_factors argument not of tuple type")
        if not len(zoom_factors) > 0:
            raise ValueError("zoom_factors argument is empty tuple")
        if sum(1 for factor in zoom_factors if isinstance(factor, (int, float))) != len(zoom_factors):
            raise ValueError("one or more values in zoom_factors argument not of int or float type")
        if not isinstance(zoom_default, (int, float)):
            raise TypeError("zoom_default argument is not int or float type")
        if not zoom_default >= 0:
            raise ValueError("zoom_default argument does not have a valid value")
        # categories
        categories = kwargs.get("categories", {})
        if not isinstance(categories, (dict, tuple)):
            raise TypeError("categories argument not of dict or tuple type")
        # background
        background = kwargs.get("background", "gray90")
        if not isinstance(background, str):
            raise TypeError("background argument not of str type")
        # style
        style = kwargs.get("style", "TimeLine.TFrame")
        if not isinstance(style, str):
            raise TypeError("style argument is not of str type")
        # extend
        extend = kwargs.get("extend", False)
        if not isinstance(extend, bool):
            raise TypeError("extend argument is not of bool type")
        snap_margin = kwargs.get("snap_margin", 10)
        if not isinstance(snap_margin, int):
            raise TypeError("snap_margin argument is not of int type")
        menu = kwargs.get("menu", None)
        if menu is not None and not isinstance(menu, tk.Menu):
            raise TypeError("menu argument is not a tk.Menu widget")
        autohidescrollbars = kwargs.get("autohidescrollbars", False)
        if not isinstance(autohidescrollbars, bool):
            raise TypeError("autohidescrollbars argument is not of bool type")
        # marker options
        marker_font = kwargs.get("marker_font", ("default", 10))
        marker_background = kwargs.get("marker_background", "lightblue")
        marker_foreground = kwargs.get("marker_foreground", "black")
        marker_outline = kwargs.get("marker_outline", "black")
        marker_border = kwargs.get("marker_border", 0)
        marker_move = kwargs.get("marker_move", True)
        marker_change_category = kwargs.get("marker_change_category", False)
        marker_allow_overlap = kwargs.get("marker_allow_overlap", False)
        marker_snap_to_ticks = kwargs.get("marker_snap_to_ticks", True)
        if not isinstance(marker_font, tuple) or len(marker_font) == 0:
            raise ValueError("marker_font argument not a valid font tuple")
        if not isinstance(marker_background, str) or not isinstance(marker_foreground, str):
            raise TypeError("marker_background and/or marker_foreground argument(s) not of str type")
        if not isinstance(marker_outline, str):
            raise TypeError("marker_outline argument not of str type")
        if not isinstance(marker_border, int):
            raise TypeError("marker_border argument is not of int type")
        if not marker_border >= 0:
            raise ValueError("marker_border argument is smaller than zero")
        if not isinstance(marker_move, bool):
            raise TypeError("marker_move argument is not of bool type")
        if not isinstance(marker_change_category, bool):
            raise TypeError("marker_change_category argument is not of bool type")
        if not isinstance(marker_allow_overlap, bool):
            raise TypeError("marker_allow_overlap argument is not of bool type")
        if not isinstance(marker_snap_to_ticks, bool):
            raise TypeError("marker_snap_to_ticks argument is not of bool type")
        return

    def check_marker_kwargs(self, kwargs):
        """
        Check the types of the keyword arguments for marker creation

        :param kwargs: dictionary of options for marker creation
        :type kwargs: dict
        :raises: TypeError, ValueError
        """
        text = kwargs.get("text", "")
        if not isinstance(text, str) and text is not None:
            raise TypeError("text argument is not of str type")
        for color in (item for item in (prefix + color for prefix in ["active_", "hover_", ""]
                                        for color in ["background", "foreground", "outline"])):
            value = kwargs.get(color, "")
            if value == "default":
                continue
            if not isinstance(value, str):
                raise TypeError("{} argument not of str type".format(color))
        font = kwargs.get("font", ("default", 10))
        if (not isinstance(font, tuple) or not len(font) > 0 or not isinstance(font[0], str)) and font != "default":
            raise ValueError("font argument is not a valid font tuple")
        for border in (prefix + "border" for prefix in ["active_", "hover_", ""]):
            border_v = kwargs.get(border, 0)
            if border_v == "default":
                continue
            if not isinstance(border_v, int) or border_v < 0:
                raise ValueError("{} argument is not of int type or smaller than zero".format(border))
        iid = kwargs.get("iid", "-1")
        if not isinstance(iid, str):
            raise TypeError("iid argument not of str type")
        if iid == "":
            raise ValueError("iid argument empty string")
        for boolean_arg in ["move", "category_change", "allow_overlap", "snap_to_ticks"]:
            value = kwargs.get(boolean_arg, False)
            if value == "default":
                continue
            if not isinstance(value, bool):
                raise TypeError("{} argument is not of bool type".format(boolean_arg))
        tags = kwargs.get("tags", ())
        if not isinstance(tags, tuple):
            raise TypeError("tags argument is not of tuple type")
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError("one or more values in tags argument is not of str type")
            if tag not in self._tags:
                raise ValueError("unknown tag in tags argument")
