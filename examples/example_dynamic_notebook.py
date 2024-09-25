from ttkwidgets.dynamic_notebook import DynamicNotebook
import tkinter as tk

def demo():
    root = tk.Tk()
    wksp =DynamicNotebook(root)
    wksp.pack(fill="both", expand=1)
    root.mainloop()

if __name__ == "__main__":
    demo()