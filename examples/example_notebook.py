import tkinter as tk
import tkinter.ttk as ttk
from ttkwidgets import Notebook


class MainWindow(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'black', 'white', 'purple', 'brown']
        self.nb = Notebook(self, tabdrag=True, tabmenu=True, closebutton=True, closecommand=self.closecmd)
        self.frames = [tk.Frame(self, width=300, height=300, bg=color) for i, color in enumerate(colors)]
        for i, w in enumerate(self.frames):
            self.nb.add(w, text="Frame " + str(i))
            w.grid()
        self.nb.grid()
    
    def closecmd(self, tab_id):
        print("Close tab " + str(tab_id))
        self.nb.forget(tab_id)


root = tk.Tk()
root.title("Notebook Example")
gui = MainWindow(root)
gui.grid()
root.mainloop()
