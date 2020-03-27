# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import Calendar
import tkinter as tk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        self.calendar = Calendar(self.main, year=2015, month=3, selectforeground='white',
                            selectbackground='red')
        self.calendar.pack()

        tk.Button(self.main, text='Select', command=self.validate).pack()
        self.label = tk.Label(self.main, text='Selected date:')
        self.label.pack()

    def validate(self):
        sel = self.calendar.selection
        if sel is not None:
            self.label.configure(text='Selected date: %s' % sel.strftime('%x'))


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
