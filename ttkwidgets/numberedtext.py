"""
Author: Faraaz Kurawle
License: GNU GPLv3
Source: This repository
"""

from tkinter import ttk
import tkinter as tk

class NumberedText(tk.Frame):
    """
    Text Widget along with line numbers.
    
    :param master: parent of this widget.
    :type: widget

    param options: all valid tk.Text customization options.
        """
    def __init__(self, master, **options):
        super().__init__(master)

        self.options = options
        self.config(bg='red')
        style = ttk.Style(self)
        self.configure(bg="white")
        style.configure("TSeparator", relief="flat")
        
        self.uniscrollbar = tk.Scrollbar(self, relief="flat")
        self.uniscrollbar.pack(side="right", fill="y")
        
        self.scroll_text()

        self.number_widget()
        
        self.textarea.config(spacing1=0, spacing2=0, spacing3=1)
        
    def scroll_text(self):
        self.textarea = tk.Text(self, relief="flat", font="times 15", **self.options)

        self.uniscrollbar["command"] = self.scroll_both
        self.textarea["yscrollcommand"] = self.update_scroll_both

        self.textarea.pack(side="right", fill="y")
    
    def number_widget(self):
        self.linenumber = LineNumbers(self, self.textarea, relief="flat", state="disabled")

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both

        self.linenumber.pack(side="right", fill="y")
        
    def mouse_wheel(self, event):
        self.scrolltext.yview_scroll(int(-1*(event.delta/120)), "units")
        self.number_widget.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def scroll_both(self, action, position):
        self.textarea.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.textarea.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
    
class LineNumbers(tk.Listbox):
    ### Internal Part of Numbered Text
    def __init__(self, master, textwidget, **options):
        super().__init__(master, **options)

        self.textwidget = textwidget
        self.textwidget.bind("<Return>", self.update_num_list)
        self.textwidget.bind("<BackSpace>", self.update_num_list)
        self.textwidget.bind("<Control-v>", self.update_num_list)

        
        self.number_var = tk.Variable(self, value=["1"])

        self.configure(listvariable=self.number_var, selectmode=tk.SINGLE)
        self.set_width(1)
        self.set_font()

    def set_font(self):
        font = self.textwidget.cget("font")
        self.configure(font = font)

    def set_width(self, num_len):
        self.configure(width=num_len+1)

    def update_num_list(self, event):
        linenums = self.get_num_lines()
        current_column = self.get_current_colomn()
    
        if current_column != 0 and event.keycode == 8: return

        if current_column == 0 and linenums == 2 and event.keycode == 8 : return

        number_list = list(range(1, linenums+1)) if event.keycode == 13 or event.keycode == 86 else list(range(1, linenums-1))

        self.set_width(len(str(linenums)))
        self.number_var.set(number_list)
        self.yview("end")
        
    def get_num_lines(self):
        num_lines = int(self.textwidget.index("end").split(".")[0])
        return (num_lines)

    def get_current_colomn(self):
        curr_column = int(self.textwidget.index("insert").split(".")[1])
        return (curr_column)

    def get_current_row(self):
        curr_row = int(self.textwidget.index("insert").split(".")[0])
        return (curr_row)
