# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE

import tkinter as tk
from ttkwidgets import TimeLine


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        timeline = TimeLine(
            self.main,
            categories={str(key): {"text": "Category {}".format(key)} for key in range(0, 5)},
            height=100, extend=True
        )
        menu = tk.Menu(self.main, tearoff=False)
        menu.add_command(label="Some Action",
                command=lambda: print("Command Executed"))
        timeline.tag_configure("1", right_callback=lambda *args: print(args),
                menu=menu, foreground="green", active_background="yellow",
                hover_border=2, move_callback=lambda *args: print(args))
        timeline.create_marker("1", 1.0, 2.0, background="white",
                text="Change Color", tags=("1",), iid="1")
        timeline.create_marker("2", 2.0, 3.0, background="green",
                text="Change Category", foreground="white", iid="2",
                change_category=True)
        timeline.create_marker("3", 1.0, 2.0, text="Show Menu", tags=("1",))
        timeline.create_marker("4", 4.0, 5.0, text="Do nothing", move=False)
        timeline.draw_timeline()
        timeline.grid()
        self.main.after(2500, lambda: timeline.configure(marker_background="cyan"))
        self.main.after(5000, lambda: timeline.update_marker("1", background="red"))
        self.main.after(5000, lambda: print(timeline.time))


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
