# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.color import askcolor
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        self.canvas = tk.Canvas(self.main, width=120, height=120)
        self.canvas.create_text(60, 60, text='Background', anchor='center')
        self.canvas.pack()
        ttk.Button(self.main, text="Pick a color (No alpha channel)",
            command=self.pick).pack(fill='x')
        ttk.Button(self.main, text="Pick a color (With alpha channel)",
            command=lambda: self.pick(True)).pack(fill='x')

    def pick(self, alpha=False):
        global im # to avoid garbage collection of image
        res = askcolor('sky blue', parent=self.main, title='Pick a color', alpha=alpha)
        self.canvas.delete('image')
        if res[1] is not None:
            im = ImageTk.PhotoImage(Image.new('RGBA', (100, 100), res[1]), master=self.main)
            self.canvas.create_image(60, 60, image=im, tags='image', anchor='center')
        print(res)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
