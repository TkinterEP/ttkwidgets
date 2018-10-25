# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets.color import askcolor
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from PIL import Image, ImageTk


def pick(alpha=False):
    global im  # to avoid garbage collection of image
    res = askcolor('sky blue', parent=window, title='Pick a color', alpha=alpha)
    canvas.delete('image')
    if res[1] is not None:
        im = ImageTk.PhotoImage(Image.new('RGBA', (100, 100), res[1]), master=window)
        canvas.create_image(60, 60, image=im, tags='image', anchor='center')
    print(res)


window = tk.Tk()
canvas = tk.Canvas(window, width=120, height=120)
canvas.create_text(60, 60, text='Background', anchor='center')
canvas.pack()
ttk.Button(window, text="Pick a color (No alpha channel)", command=pick).pack(fill='x')
ttk.Button(window, text="Pick a color (With alpha channel)", command=lambda: pick(True)).pack(fill='x')
window.mainloop()
