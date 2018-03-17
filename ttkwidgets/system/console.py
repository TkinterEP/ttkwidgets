"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
    import tkFileDialog as fd
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.filedialog as fd
import sys
from threading import Lock
import rlcompleter
import traceback


class Console(ttk.Frame):
    """
    Interactive Console supporting Python console as well as System
    Console. Based on pytkcon by samyzaf (GitHub).
    """
    SYSTEM = "system"
    PYTHON = "python"

    COLORS_PASTELS = {
        "background": "#3f3f3f",
        "foreground": "#dcdccc",
        "prompt": "#72d5a3",
        "path": "#94bff3",
        "error": "#dca3a3",
    }

    _MODIFIERS = {
        "Shift": 0x00001,
        "Control": 0x00004,
        "Alt": 0x20000,
        "Caps_Lock": 0x00002,
        "Right_Down": 0x00400,
        "Middile_Down": 0x00200
    }

    _WELCOME_PYTHON = "Python {}.{}.{}".format(*sys.version_info)
    _WELCOME_SYSTEM = ""

    def __init__(self, master: tk.Widget, **kwargs):
        """
        :param master: master widget

        :param kind: Kind of Console, either SYSTEM or PYTHON
        :param color: Whether colors are enabled
        :param colors: Color scheme dictionary
        :param width: Amount of characters in a line
        :param height: Amount of lines
        :param font: Font for the Text

        :param kwargs: passed on to ttk.Frame.__init__
        """
        self._kind = kwargs.pop("kind", Console.SYSTEM)
        self._color = kwargs.pop("color", True)
        self._colors = kwargs.pop("colors", Console.COLORS_PASTELS)
        self._width = kwargs.pop("width", 80)
        self._height = kwargs.pop("height", 24)
        self._font = kwargs.pop("font", ("Consolas", 9, "normal"))

        ttk.Frame.__init__(self, master, **kwargs)

        # Attributes
        self._history = list()
        self._complete = rlcompleter.Completer(globals()).complete
        self._write_lock = Lock()

        # Child widgets
        self._scroll = ttk.Scrollbar(self)
        self._text = tk.Text(self, yscrollcommand=self._scroll.set)
        self._scroll.config(command=self._text.yview)

    def setup_bindings(self):
        """Setup the bindings for the Text widget"""
        self._text.bind("<Return>", self.handle_return)
        self._text.bind("<Shift-KeyRelease-Return>", self.handle_return)
        self._text.bind("<KeyRelease-Up>", self.handle_up)
        self._text.bind("<BackSpace>", self.handle_backspace)
        self._text.bind("<Delete>", self.handle_delete)
        self._text.bind("<Tab>", self.handle_tab)
        self._text.bind("<Key>", self.handle_key)
        self._text.bind("<Control-l>", self.handle_control)
        self._text.bind("<Enter>", self.focus)

    def setup_text(self):
        """Setup Text widgets with tags and font"""
        self._text.tag_config("prompt", foreground=self._colors["prompt"], font=self._font[0:2] + ("bold",))
        self._text.tag_config("err", foreground=self._colors["error"])
        self._text.tag_config("out", foreground=self._colors["foreground"])
        self._text.tag_config("path", foreground=self._colors["path"])
        self._text.config(background=self._colors["background"])

    def exec(self, cmd: str=None):
        """Configure Text widget for executing command"""
        self._text.tag_add("cmd", "limit", "%s-1c" % tk.INSERT)
        if cmd is None:
            cmd = self._text.get("limit", tk.END).lstrip()
            self._history.append(cmd)
        self.eval(cmd)

    def eval(self, cmd: str):
        """Execute a given command in the Python interpreter"""
        try:
            compile(cmd, "<stdin>", "eval")
        except SyntaxError:
            try:
                exec(cmd, globals())
            except Exception:
                self.write_exception()
            return
        try:
            result = eval(cmd, globals())
            if result is not None:
                self.write(tk.END, result, tags=("out",))
        except Exception:
            self.write_exception()

    def login(self):
        """Change username/host prompt for SYSTEM Console"""
        if self._kind != Console.SYSTEM:
            return
        pass

    def prompt(self):
        """Write the prompt to the Text widget"""
        pass

    def write(self, *args, **kwargs):
        """Write a string to the output buffer"""
        self._write_lock.acquire()
        self._text.insert(*args, **kwargs)
        self._write_lock.release()

    def write_exception(self):
        """Write an Exception to the output"""
        self.write(tk.END, traceback.format_exc(), tags=("err",))

    def write_end(self, string:str, tags:tuple):
        """Write a given string to the end of the last line"""
        l1, c1 = Console.index_to_tuple(self._text, "%s-1c" % tk.END)
        l2, c2 = Console.index_to_tuple(self._text, 'limit')
        if l1 == l2:
            self.write('limit-3c', string, tags)
        else:
            self.write(tk.END, string, tags)
        self._text.see(tk.END)

    def write_line(self, text: str, tags: tuple):
        """Write a given line to the end of the Text widget"""
        text = text.strip() + "\n"
        self.write_end(text, tags)

    def clear(self):
        """Clear everything from the Text widget"""
        self._text.delete(1.0, tk.END)
        self.prompt()

    def handle_return(self):
        """Handle <Return> event"""
        pass

    def handle_up(self):
        """Handle <Up> (arrow) event"""
        pass

    def handle_backspace(self):
        """Handle <BackSpace> event"""
        pass

    def handle_delete(self):
        """Handle <Delete> event"""
        pass

    def handle_tab(self):
        """Handle <Tab> event"""
        pass

    def handle_key(self):
        """Handle <Key> (keypress) event"""
        pass

    def handle_control(self):
        """Handle <Control-l> (CTRL-L) event"""
        pass

    @staticmethod
    def append_event_modifiers(event):
        """Process an event for modifier keys"""
        return [mod for mod, value in Console._MODIFIERS if event.state & value]

    @staticmethod
    def index_to_tuple(text: tk.Text, index):
        """Return a tuple of line, column for index"""
        return tuple(map(int, text.index(index).split(".")))

    @staticmethod
    def tuple_to_index(tup: tuple):
        """Return a Text index for a given (line, column) tuple"""
        return str(tup[0]) + "." + str(tup[1])

    @staticmethod
    def get_last_line(text: tk.Text):
        """Return the last Console line of a given Text widget"""
        line, column = Console.index_to_tuple(text, tk.END)
        line -= 1
        start = Console.index_to_tuple(text, (line, 0))
        return text.get(start, str(line) + ".end")

    @staticmethod
    def format_list(l: list, wrap:int=60):
        """Format a list into a str"""
        text, line = str(), str()
        n = max(max([len(w) for w in l]), 18) + 2
        for elem in sorted(map(str, l)):
            if len(line) > wrap:
                text += line + "\n"
                line = str()
            else:
                line += ("%-" + str(n) + "s") % elem
        if len(line):
            text += line
        return text


class Buffer(object):
    """Write stdout or stderr also to tk.Text widget"""
    def __init__(self, text: Console, output: (sys.__stdout__, sys.__stderr__)):
        """
        :param text: Text widget to write data to
        :param output: Also write given data to this output buffer
        """
        self._text = text
        self._out = output

    def write(self, string):
        """Write a given string to buffers"""
        self._out.write(string)
        l1, _ = Console.index_to_tuple(self._text._text, "%s-1c" % tk.END)
        l2, _ = Console.index_to_tuple(self._text._text, 'limit')
        if l1 == l2:
            self._text.write('limit-3c', string)
        else:
            self._text.write('end', string)
        self._text._text.see('end')

    def writelines(self, lines: list):
        """Write a list of lines to output buffers"""
        self._out.writelines(lines)
        for line in lines:
            self._text.write(line)

    def flush(self):
        """Flush output buffers"""
        self._out.flush()
        self._text.update_idletasks()
