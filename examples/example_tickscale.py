# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import TickScale
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


root = tk.Tk()
style = ttk.Style(root)
style.configure('my.Vertical.TScale', sliderlength=10, background='white',
                foreground='red')
style.configure('my.Horizontal.TScale', sliderlength=50,
                font='TkDefaultFont 20 italic')
s1 = TickScale(root, orient='vertical', style='my.Vertical.TScale',
               tickinterval=0.2, from_=-1, to=1, showvalue=True, digits=2,
               length=400, labelpos='e')
s2 = TickScale(root, orient='horizontal', style='my.Horizontal.TScale',
               from_=0, to=10, tickinterval=2, resolution=1,
               showvalue=True, length=300)
s3 = TickScale(root, orient='horizontal', style='my.Horizontal.TScale',
               from_=0.25, to=1, tickinterval=0.1, resolution=0.1,
               showvalue=True, length=300)

s1.pack(fill='y')
s2.pack(fill='x')
s3.pack(fill='x')

root.mainloop()
