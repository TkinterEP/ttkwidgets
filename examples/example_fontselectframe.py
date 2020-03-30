# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.font import FontSelectFrame
import tkinter as tk
from tkinter import ttk


class Example:
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        self.label = ttk.Label(
                self.main, text='Sample text rendered in the chosen font.')
        self.label.pack(padx=10, pady=10)
        self.font_selection = FontSelectFrame(
                self.main, callback=self.update_preview)
        self.font_selection.pack()

    def update_preview(self, font_tuple):
        print(font_tuple)
        font = self.font_selection.font[0]
        if font is not None:
            self.label.configure(font=font)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
