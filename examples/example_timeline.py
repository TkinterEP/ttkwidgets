# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE

import tkinter as tk
from ttkwidgets import TimeLine

window = tk.Tk()
timeline = TimeLine(
    window,
    categories={str(key): {"text": "Category {}".format(key)} for key in range(0, 5)},
    height=100
)
menu = tk.Menu(window, tearoff=False)
menu.add_command(label="Something")
timeline.tag_configure("1", right_callback=lambda *args: print(args), menu=menu, foreground="green",
                       active_background="yellow", hover_border=2, move_callback=lambda *args: print(args))
timeline.create_marker("1", 1.0, 2.0, background="white", text="Hello World", tags=("1",), iid="1")
timeline.create_marker("2", 2.0, 3.0, background="green", text="Hello Tkinter", foreground="white", iid="2",
                       change_category=True)
timeline.create_marker("3", 1.0, 2.0, text="Hello Python")
timeline.create_marker("4", 4.0, 5.0, text="Hello User")
timeline.generate_timeline_contents()
timeline.grid()
window.after(5000, lambda: timeline.update_marker("1", background="red"))
window.after(5000, lambda: print(timeline.time))
window.mainloop()