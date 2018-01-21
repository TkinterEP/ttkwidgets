# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import TimeLine
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestTimeLine(BaseWidgetTest):
    def test_initialization(self):
        TimeLine(self.window)

    def test_kwargs(self):
        alternates = {
            "background": "black",
            "marker_foreground": "white",
            "menu": tk.Menu(),
            "categories": ("category_a", "category_b"),
        }
        for key, value in alternates.items():
            TimeLine(self.window, **{key: value}).configure({key: value})

    def test_kwargs_errors(self):
        timeline = TimeLine(self.window)
        for option in timeline.options:
            self.assertRaises((TypeError, ValueError), lambda: timeline.config(
                # menu is the only kwarg that has an allowed None value
                **{option: None if option != "menu" else tk.Frame()}))

    def test_categories(self):
        TimeLine(self.window, categories=("category",))
        TimeLine(self.window, categories={"category": {"text": "Category"}})
        self.assertRaises(TypeError, lambda: TimeLine(self.window, categories=["category",]))

    def test_marker_creation(self):
        timeline = TimeLine(self.window, categories={"category": {"foreground": "cyan", "text": "Category"}})
        iid = timeline.create_marker("category", 1.0, 2.0)
        self.assertTrue(iid in timeline.markers)

    def test_timeline_content_generation(self):
        TimeLine(self.window, categories=("category",)).generate_timeline_contents()

    def test_markers_property(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0)
        markers = timeline.markers
        self.assertIsInstance(markers, dict)
        self.assertTrue(iid in markers)
        self.assertIsInstance(markers[iid], dict)
        for option in timeline.marker_options:
            self.assertTrue(option in markers[iid])

    def test_timeline_contents(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0, text="Test")
        timeline.generate_timeline_contents()
        ids = timeline._timeline.find_all()
        rectangle = timeline.markers[iid]["rectangle_id"]
        text = timeline.markers[iid]["text_id"]
        self.assertTrue(rectangle in ids)
        self.assertTrue(text in ids)

    def test_timeline_zoom_in(self):
        timeline = TimeLine(self.window, categories=("category",))
        zoom_factor = timeline.zoom_factor
        amount_ticks = len(timeline._ticks)
        amount_items = len(timeline._canvas_ticks.find_all())
        timeline._button_zoom_in.invoke()
        self.assertGreater(timeline.zoom_factor, zoom_factor)
        self.assertGreater(len(timeline._ticks), amount_ticks)
        self.assertGreater(len(timeline._canvas_ticks.find_all()), amount_items)

    def test_timeline_zoom_reset(self):
        timeline = TimeLine(self.window, zoom_factors=(1.0, 2.0, 5.0, 10.0), zoom_default=5.0)
        zoom_factor = timeline.zoom_factor
        for i in range(4):
            timeline.zoom_in()
        timeline.zoom_reset()
        self.assertEqual(timeline.zoom_factor, zoom_factor)
        self.assertEqual(timeline.zoom_factor, 5.0)

    def test_timeline_zoom(self):
        timeline = TimeLine(self.window)
        factor = timeline.zoom_factor
        timeline.zoom_in()
        timeline.zoom_out()
        self.assertEqual(factor, timeline.zoom_factor)

    def test_timeline_click(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0)
        # calculate the coordinates of the marker
        marker = timeline.markers[iid]
        rectangle, text = marker["rectangle_id"], marker["text_id"]
        xr, yr, _, _ = timeline._timeline.bbox(rectangle)
        xw, yw = timeline._timeline.winfo_x(), timeline._timeline.winfo_y()
        event = MockEvent(xr+xw, yr+yw)
        timeline.left_click(event)
        timeline.right_click(event)

    def test_direct_configure(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0)
        timeline.itemconfigure(iid, {"fill": "black"}, {})

    def test_out_of_bounds(self):
        timeline = TimeLine(self.window, categories=("category",), start=0.0, finish=1.0)
        self.assertRaises(ValueError, lambda: timeline.create_marker("category", 2.0, 3.0))
        self.assertRaises(ValueError, lambda: timeline.create_marker("category", -1, -2))

    def test_text_shortening(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0, text="This is a very long sentence.")
        text_id = timeline.markers[iid]["text_id"]
        text = timeline._timeline.itemcget(text_id, "text")
        self.assertTrue("..." in text)

    def test_marker_time_window(self):
        timeline = TimeLine(self.window)
        x, y = timeline._canvas_ticks.winfo_x(), timeline._canvas_ticks.winfo_y()
        x += 20
        y += 10
        timeline.time_marker_move(MockEvent(x, y))
        self.assertIsInstance(timeline._time_window, tk.Toplevel)
        timeline.time_marker_release(MockEvent(x, y))

    def test_update_marker(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0)
        self.assertTrue(iid in timeline.markers)
        timeline.update_marker(iid, text="New Text")
        self.assertTrue(iid in timeline.markers)
        text_id = timeline.markers[iid]["text_id"]
        text = timeline._timeline.itemcget(text_id, "text")
        self.assertEqual(text, "New Text")

    def test_delete_marker(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0)
        rectangle_id = timeline.markers[iid]["rectangle_id"]
        timeline.delete_marker(iid)
        self.assertTrue(iid not in timeline.markers)
        self.assertTrue(rectangle_id not in timeline._timeline.find_all())

    def test_marker_tags(self):
        timeline = TimeLine(self.window, categories=("category",))
        self.assertRaises(ValueError, lambda: timeline.create_marker("category", 1.0, 2.0, tags=("tag",)))
        timeline.tag_configure("tag", background="cyan")
        iid = timeline.create_marker("category", 1.0, 2.0, tags=("tag",))
        self.assertTrue("tag" in timeline.marker_tags(iid))
        rectangle_id = timeline.markers[iid]["rectangle_id"]
        color = timeline._timeline.itemcget(rectangle_id, "fill")
        self.assertEqual(color, "cyan")

    def test_update_state(self):
        timeline = TimeLine(self.window, categories=("category",))
        iid = timeline.create_marker("category", 1.0, 2.0, hover_background="yellow")
        timeline.update_state(iid, "hover")
        rectangle_id = timeline.markers[iid]["rectangle_id"]
        color = timeline._timeline.itemcget(rectangle_id, "fill")
        self.assertEqual(color, "yellow")

    def test_unit_formatting(self):
        for unit in ["m", "h"]:
            self.assertEqual(TimeLine.get_time_string(1.0, unit), "01:00")
            self.assertEqual(TimeLine.get_time_string(1.5, unit), "01:30")
            self.assertEqual(TimeLine.get_time_string(3.25, unit), "03:15")

    def test_set_time(self):
        timeline = TimeLine(self.window)
        timeline.set_time(2.0)
        self.assertEqual(timeline.time, 2.0)


class MockEvent(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
