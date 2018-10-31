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
from contextlib import contextmanager
import sys
from threading import Lock
import rlcompleter
import traceback
from ttkwidgets import AutoHideScrollbar
import subprocess as sp


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
        "Middle_Down": 0x00200
    }

    _WELCOME_PYTHON = "Python {}.{}.{}".format(*sys.version_info)
    _WELCOME_SYSTEM = ""

    def __init__(self, master, **kwargs):
        # type: ((tk.Tk, tk.Widget, tk.BaseWidget)) -> None
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
        self._scroll = AutoHideScrollbar(self)
        self._text = tk.Text(self, yscrollcommand=self._scroll.set)
        self._scroll.config(command=self._text.yview)

        self.setup_console()

        self.grid_widgets()

    def setup_console(self):
        """Configure Console properties, input and output"""
        if self._kind == Console.SYSTEM and sys.platform == "linux":
            from subprocess import Popen, PIPE
            p = Popen(["bash"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            self.__stdout = p.stdout
            self.__stderr = p.stderr
            self.__stdin = p.stdin
        elif self._kind == Console.PYTHON:
            pass
        else:
            raise ValueError("Invalid type of Console requested")

    def grid_widgets(self):
        """Configure child widgets in grid geometry manager"""
        self._text.grid(row=1, column=1, padx=5, pady=5)
        self._scroll.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="ns")

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


class PythonInterface(object):
    """Create an stdout, stderr and stdin interface to Python"""

    class _Python(object):
        """Provide access to the Python interpreter"""

        def __init__(self, stdout, stderr):
            """Initialize with given output buffers"""
            # type: PythonInterface.Buffer, PythonInterface.Buffer -> None
            self._stdout = stdout
            self._stderr = stderr

        def write(self, string):
            # type: (bytes) -> int
            """Write a string of UTF-8 encoded bytes to eval"""
            string = string.decode()
            try:
                with PythonInterface.grab_stdout() as stdout:
                    exec(string)
                self._stdout.write(stdout)
            except BaseException:
                # Handle error with stderr
                self._stderr.write(traceback.format_exc().encode())
                return 0
            return len(string)

    def __init__(self):
        """Initialize input and output buffers"""
        self.stdout = PythonInterface.Buffer()
        self.stderr = PythonInterface.Buffer()
        self.stdin = PythonInterface._Python(self.stdout, self.stderr)

    @staticmethod
    @contextmanager
    def grab_stdout():
        """Context manager that temporarily redirects stdout"""
        # type: () -> bytes
        b = PythonInterface.Buffer()
        stdout = sys.__stdout__
        sys.__stdout__ = b
        yield
        s = b.read(-1)
        sys.__stdout__ = stdout
        return s

    class Buffer(object):
        """Redirect for any buffer instance"""

        def __init__(self):
            """Instantiate buffer instance and attributes"""
            self._buffer = bytes()

        def write(self, string):
            """Write a bytes string to the buffer"""
            # type: bytes -> int
            self._buffer += string
            return len(string)

        def writelines(self, lines):
            """Write a set of bytes lines to the buffer"""
            self._buffer += b"".join(lines)
            return len(lines)

        def read(self, amount):
            """Read a specified amount of bytes from the buffer"""
            # type: int -> bytes
            if amount == -1:
                b = self._buffer
                self._buffer = bytes()
                return b
            b = self._buffer[:amount]
            self._buffer = self._buffer[amount:]
            return b

        def flush(self):
            pass


class SystemInterface(sp.Popen):
    """Provide a platform-dependent interface to the system console"""

    COMMAND = "bash" if "linux" in sys.platform else "cmd"

    def __init__(self):
        """Initialize process for system console command"""
        sp.Popen.__init__(self, [SystemInterface.COMMAND], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)


if __name__ == "__main__":
    window = tk.Tk()
    console = Console(window)
    console.pack()
    console.mainloop()
