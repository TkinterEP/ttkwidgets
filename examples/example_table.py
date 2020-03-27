# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import Table
import tkinter as tk
from tkinter import ttk


class Example():
    def __init__(self, root, is_top_level=False):
        if is_top_level:
            self.main = tk.Toplevel(root)
            self.main.transient(root)
            self.main.grab_set()
        else:
            self.main = root

        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(0, weight=1)

        style = ttk.Style(self.main)
        style.theme_use('alt')
        self.sortable = tk.BooleanVar(self.main, False)
        self.drag_row = tk.BooleanVar(self.main, False)
        self.drag_col = tk.BooleanVar(self.main, False)

        columns = ["A", "B", "C", "D", "E", "F", "G"]
        self.table = Table(self.main,
                columns=columns, sortable=self.sortable.get(),
                drag_cols=self.drag_col.get(),
                drag_rows=self.drag_row.get(), height=6)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, stretch=False)

        # sort column A content as int instead of strings
        self.table.column('A', type=int)

        for i in range(12):
            self.table.insert('', 'end', iid=i,
                         values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))

        # add scrollbars
        sx = tk.Scrollbar(self.main, orient='horizontal', command=self.table.xview)
        sy = tk.Scrollbar(self.main, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

        self.table.grid(sticky='ewns')
        sx.grid(row=1, column=0, sticky='ew')
        sy.grid(row=0, column=1, sticky='ns')
        self.main.update_idletasks()

        frame = tk.Frame(self.main)
        tk.Checkbutton(frame, text='sortable',
                variable=self.sortable,
                command=self.toggle_sort).pack(side='left')
        tk.Checkbutton(frame, text='drag columns',
                variable=self.drag_col,
                command=self.toggle_drag_col).pack(side='left')
        tk.Checkbutton(frame, text='drag rows',
                variable=self.drag_row,
                command=self.toggle_drag_row).pack(side='left')
        frame.grid()
        self.main.geometry('400x200')

    # toggle table properties
    def toggle_sort(self):
        self.table.config(sortable=self.sortable.get())

    def toggle_drag_col(self):
        self.table.config(drag_cols=self.drag_col.get())

    def toggle_drag_row(self):
        self.table.config(drag_rows=self.drag_row.get())


if __name__ == '__main__':
    root = tk.Tk()
    Example(root)
    root.mainloop()
