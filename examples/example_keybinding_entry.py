import tkinter as tk
import tkinter.ttk as ttk

from ttkwidgets import KeybindingEntry


class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.ety = KeybindingEntry(self)
        self.ety.pack()
        self.ety.bind("<<KeybindingValidated>>", self._on_keybind_validate)
    
    def _on_keybind_validate(self, event):
        print(self.ety.event_format)

root = tk.Tk()
root.title("Keybinding Example")
gui = MainWindow(root)
gui.pack()
root.mainloop()
