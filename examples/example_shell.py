import os
import tkinter as tk

from ttkwidgets import Shell


def onreturn(buffer):
    import shlex
    lexed = shlex.split(buffer, posix=True)
    shell.print(lexed)

def contractuser(path):
    expand = os.path.expanduser('~')
    return path.replace(expand, '~')

root = tk.Tk()
root.title(os.getcwd())
shell = Shell(root, prefix=contractuser(os.getcwd()) + ' ')
shell.add_command('onreturn', onreturn)
shell.pack()
root.mainloop()