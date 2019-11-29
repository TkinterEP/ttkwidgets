import tkinter as tk
import tkinter.ttk as ttk
from ttkwidgets import PlaceholderEntry


class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.entry = PlaceholderEntry(self, placeholder="It's a placeholder")
        self.entry.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Placeholder Entry Example")
    gui = MainWindow(root)
    gui.pack()
    root.mainloop()
