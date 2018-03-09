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


class Console(ttk.Frame):
    """
    Interactive Console supporting Python console as well as System
    Console. Loosely based on pytkcon by samyzaf (GitHub).
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

    def __init__(self, master: tk.Widget, kind=SYSTEM, color=True,
                 colors=COLORS_PASTELS, **kwargs):
        """
        :param master: master widget
        :param kind: kind of Console, either SYSTEM or PYTHON
        :param color: Whether colors are enabled
        :param colors: Color scheme dictionary
        :param kwargs: passed on to ttk.Frame.__init__
        """
        ttk.Frame.__init__(self, master, **kwargs)





