# Copyright (c) 2020 Fredy Ramirez <https://formateli.com>
# For license see LICENSE
"""
run.py
Show all examples located in this example folder.
Main window show a button for each example.
"""
import os
import subprocess
import tkinter as tk
from tkinter import ttk

_DIR = os.path.dirname(os.path.realpath(__file__))
_DIR = os.path.normpath(os.path.join(_DIR, '..'))

EXAMPLE_ENV = os.environ.copy()
if not 'PYTHONPATH' in EXAMPLE_ENV:
    EXAMPLE_ENV["PYTHONPATH"] = _DIR
else:
    EXAMPLE_ENV["PYTHONPATH"] = _DIR + os.pathsep + EXAMPLE_ENV["PYTHONPATH"]


class _SampleButton:
    def __init__(self, root, text, col, row):
        self.btn = ttk.Button(root, text=text, command=self.run_example)
        self.btn.grid(row=row, column=col, sticky="nsew") 

    def run_example(self, event=None):
        subprocess.Popen(['python', 'example_' + self.btn['text'] + '.py'], env=EXAMPLE_ENV)


def _get_samples():
    result = []
    dir_ = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(dir_)
    for f in files:
        if f == 'run.py':
            continue
        fp = os.path.join(dir_, f)
        if os.path.isfile(f) and f.endswith('.py'):
            f = f[8:]           # remove example_
            f = f[0:len(f)-3]   # remove .py
            result.append([f, fp])
    return result


def _add_samples(window):
    samples = _get_samples()
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
    root.title('ttkwidgets Examples')
    root.geometry('800x500')
    _add_samples(root)
    root.mainloop()
