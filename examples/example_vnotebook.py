from ttkwidgets import VNotebook
import tkinter.ttk as ttk
import tkinter as tk


def callback():
    notebook.hide(id_)


root = tk.Tk()
notebook = VNotebook(root, compound=tk.RIGHT)
notebook.add(ttk.Scale(notebook), text="Scale")
notebook.add(ttk.Button(notebook, text="Destroy", command=root.destroy), text="Button")
frame = ttk.Frame(notebook)
id_ = notebook.add(frame, text="Hidden")
ttk.Button(frame, command=callback, text="Hide").grid()
notebook.enable_traversal()
notebook.grid(row=1)
root.mainloop()
