"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
import tkinter as tk
from tkinter import ttk
from ttkwidgets import tooltips  # Import once, use everywhere


window = tk.Tk()
button = ttk.Button(window, text="Destroy", command=window.destroy, tooltip="This button destroys the window.")
button.pack()
x = lambda: button.configure(tooltip="This button no longer destroys the window", command=lambda: print("Behaviour changed!"))
window.after(5000, x)
window.mainloop()
