"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
import tkinter as tk
from tkinter import ttk
from ttkwidgets import tooltips  # Import once, use everywhere


window = tk.Tk()
ttk.Button(window, text="Destroy", command=window.destroy, tooltip="This button destroys the window.").pack()
window.mainloop()
