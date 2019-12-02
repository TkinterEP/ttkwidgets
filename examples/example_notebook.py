import tkinter as tk
import tkinter.ttk as ttk
from ttkwidgets import Notebook


class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.nb = Notebook(self)
        self.frames = [tk.Frame(self) for i in range(10)]
        for i, w in enumerate(self.frames):
            tk.Canvas(w, width=300, height=300).grid(sticky="nswe")
            self.nb.add(w, text="Frame " + str(i))
            w.grid()
        self.nb.grid()


root = tk.Tk()
root.title("Notebook Example")
gui = MainWindow(root)
gui.grid()
root.mainloop()