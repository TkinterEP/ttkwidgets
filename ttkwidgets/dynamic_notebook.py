"""
Author: Faraaz Kurawle
License: GNU GPLv3
Source: This repository
"""

import tkinter as tk
import tkinter.ttk as ttk

class DynamicNotebook(ttk.Notebook):
    """
    Notebook widget with ablity to add or remove tabs in the runtime.

    :param parent: parent widget of this widget.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.root = parent
        self.frame_dict = {}
        self.intial_Frames()

        self.bind("<<NotebookTabChanged>>", self.watcher)
        

    def intial_Frames(self):
        frame1 = tk.Frame(self, bg="white")

        self.add(frame1, text="Frame 1")
        self.add(tk.Label(self), text="-")
        self.add(tk.Label(self), text="+")

        self.frame_dict.update({"Frame 1": frame1})

    def add_frame_button_func(self):
        c = self.index("current")
        self.insert_frame(c - 1)

    def insert_frame(self, index):
        tab_text = f"Frame {index+1}"
        frame = tk.Frame(self, bg="white")
        
        self.insert(index, frame, text=tab_text)

        self.frame_dict.update({tab_text: frame})
        self.select(index)

    def remove_frame(self, index):
        self.forget(index)
        self.select(index - 1)

    def get_current_frame_tcl_name(self):
        current_index = self.index("current")
        return self.root.nametowidget(self.tabs()[current_index])

    def watcher(self, e):
        tab_name = self.tab(self.select(), "text")

        if tab_name not in ("-", "+"):
            return

        if tab_name == "-":
            c = self.index("current")
            if self.index("end") > 3:
                self.remove_frame(c - 1)
            else:
                self.select(c - 1)

        elif tab_name == "+":
            c = self.index("current")
            self.insert_frame(c - 1)
      
