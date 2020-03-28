# Copyright (c) 2020 Fredy Ramirez <https://formateli.com>
# For license see LICENSE

import sys, os
import tkinter as tk
from tkinter import ttk
from importlib import import_module

_DIR = os.path.dirname(os.path.realpath(__file__))
_DIR = os.path.normpath(os.path.join(_DIR, '..', 'ttkwidgets'))
if os.path.isdir(_DIR):
    sys.path.insert(0, os.path.dirname(_DIR))


class _SampleButton():
    def __init__(self, root, text, col, row):
        self.root = root
        self.btn = ttk.Button(root, text=text, command=self.run_example)
        self.btn.grid(row=row, column=col, sticky="nsew") 

    def run_example(self, event=None):
        try:
            module = import_module('examples.example_' + self.btn['text'])
            ex_class = getattr(module, 'Example')
            self.root.wait_window(
                ex_class(self.root, is_top_level=True).main)
        except Exception as e:
            print(e)


def _get_samples():
    result = []
    dir_ = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(dir_)
    for f in files:
        if f == 'run.py':
            continue
        fp = os.path.join(dir_, f)
        if os.path.isfile(f) and f.endswith('.py'):
            f = f[8:] # remove example_
            f = f[0:len(f)-3] # remove .py
            result.append([f, fp])
    return result


def _add_samples(window):
    samples = _get_samples()
    total_samples = len(samples)
    max_col_count = 5
    row = -1
    col = -1
    row_checked = False
    for s in samples:
        if col == -1 or (row + 1) > max_col_count:
            col += 1
            window.grid_columnconfigure(col, weight=1)

        if row == -1 or (row + 1) > max_col_count:
            if (row + 1) > max_col_count:
                row_checked = True
            row = 0

        if not row_checked:
            window.grid_rowconfigure(row, weight=1)

        _SampleButton(window, s[0], col, row)
        row += 1


if __name__ == '__main__':
    root = tk.Tk()
    root.title('ttkwidget Examples')
    root.geometry('800x500')
    _add_samples(root)
    root.mainloop()
    try:
        root.destroy()
    except:
        pass
