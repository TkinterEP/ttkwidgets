# -*- coding: utf-8 -*-

# Copyright (c) RedFantom 2017
# For license see LICENSE


from ttkwidgets.frames import Balloon
import tkinter as tk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        button = tk.Button(self.main, text="Button", command=self.main.destroy)
        button.pack()
        balloon = Balloon(button)


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
