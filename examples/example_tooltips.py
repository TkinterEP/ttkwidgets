"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
import tkinter as tk
from tkinter import ttk
# Import once, use everywhere
from ttkwidgets import tooltips


window = tk.Tk()
button = ttk.Button(window, text="Destroy", command=window.destroy, tooltip="This button destroys the window.")
button.pack()
x = lambda: button.configure(tooltip="This button no longer destroys the window", command=lambda: print("Behaviour changed!"))
window.after(5000, x)
window.mainloop()
