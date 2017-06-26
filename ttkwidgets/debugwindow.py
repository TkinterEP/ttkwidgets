"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
    import tkFileDialog as fd
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.filedialog as fd
import sys


class DebugWindow(tk.Toplevel):
    """
    A Toplevel that shows sys.stdout and sys.stderr for Tkinter applications
    """
    def __init__(self, master=None, title="Debug window", stdout=True, stderr=False, width=70, **kwargs):
        self._width = width
        tk.Toplevel.__init__(self, master, **kwargs)
        self.wm_title(title)
        if stdout:
            sys.stdout = self
        if stderr:
            sys.stderr = self
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="Save file", command=self.save)
        self.filemenu.add_command(label="Exit", command=self.destroy)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.text = tk.Text(self, width=width)
        self.scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        self.text.bind("<Key>", lambda e: "break")
        self._grid_widgets()

    def save(self):
        file_name = fd.asksaveasfilename()
        if file_name is "" or file_name is None:
            return
        with open(file_name, "w") as f:
            f.write(self.text.get("1.0", tk.END))

    def _grid_widgets(self):
        self.text.grid(row=0, column=0)
        self.scroll.grid(row=0, column=1, sticky="ns")

    def write(self, line):
        while True:
            if len(line) <= self._width:
                self.text.insert(tk.END, line)
                break
            else:
                sub = line[:self._width]
                self.text.insert(tk.END, sub)
                self.text.insert(tk.END, "\n")


if __name__ == '__main__':
    DebugWindow().mainloop()
