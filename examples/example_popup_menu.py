import tkinter as tk
import ttkwidgets


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.some_var = False
        
        self.menu = ttkwidgets.PopupMenu(self, callbacks=[self.on_context_menu_open])
        self.menu.add_command(label="Foo", command=self.dummy)
        self.menu.add_command(label="Bar", command=self.dummy)
        self.menu.add_command(label="Baz", command=self.dummy)

    def on_context_menu_open(self, event):
        print("Context menu opened!")
        self.some_var = True

    def dummy(self):
        print("Dummy call.")
        self.some_var = False


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x300")
    gui = MainWindow(root)
    gui.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
