# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2018
# For license see LICENSE

from ttkwidgets import Table
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sortable = tk.BooleanVar(root, False)
drag_row = tk.BooleanVar(root, False)
drag_col = tk.BooleanVar(root, False)

columns = ["A", "B", "C", "D", "E", "F", "G"]
table = Table(root, columns=columns, sortable=sortable.get(), drag_cols=drag_col.get(),
              drag_rows=drag_row.get(), height=6)
for col in columns:
    table.heading(col, text=col)

# sort column A content as int instead of strings
table.column('A', type=int)

for i in range(10):
    table.insert('', 'end', iid=i,
                 values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))

# add scrollbars
sx = tk.Scrollbar(root, orient='horizontal', command=table.xview)
sy = tk.Scrollbar(root, orient='vertical', command=table.yview)
table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

table.grid(sticky='ewns')
sx.grid(row=1, column=0, sticky='ew')
sy.grid(row=0, column=1, sticky='ns')


# toggle table properties
def toggle_sort():
    table.config(sortable=sortable.get())


def toggle_drag_col():
    table.config(drag_cols=drag_col.get())


def toggle_drag_row():
    table.config(drag_rows=drag_row.get())


frame = tk.Frame(root)
tk.Checkbutton(frame, text='sortable', variable=sortable, command=toggle_sort).pack(side='left')
tk.Checkbutton(frame, text='drag columns', variable=drag_col, command=toggle_drag_col).pack(side='left')
tk.Checkbutton(frame, text='drag rows', variable=drag_row, command=toggle_drag_row).pack(side='left')
frame.grid()

root.mainloop()
