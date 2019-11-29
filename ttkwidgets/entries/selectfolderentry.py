import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

from ttkwidgets.utilities import get_bitmap


class SelectFolderEntry(ttk.Frame):
    def __init__(self, master=None, title="Select a directory", path=None, **kwargs):
        super().__init__(master)
        self.ety = ttk.Entry(self, **kwargs)
        self.button_img = get_bitmap("folder")
        button = ttk.Button(self, bitmap=self.button_img, command=self.on_btn_click)

        self.ety.bind("<Double-Button-1>", self.on_btn_click)
        self.path = path
        self.title = title
        if path is not None:
            self.ety.delete(0, tk.END)
            self.ety.insert(tk.END, self.path)

        self.ety.grid(row=0, column=0)
        button.grid(row=0, column=1)

    def on_btn_click(self, *args):
        self.path = filedialog.askdirectory(title=self.title)
        self.ety.delete(0, tk.END)
        self.ety.insert(tk.END, self.path)
