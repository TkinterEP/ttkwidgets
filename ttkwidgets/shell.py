import tkinter as tk
import tkinter.font as tkfont
from collections import defaultdict


class Shell(tk.Canvas):
    def __init__(self, master, textvariable=None, prefix='', force_focus=True,
                 font=None, **kwargs):
        """
        :param master: parent widget
        :type master: tkinter.Widget
        :param textvariable: A tkinter variable that holds the current text buffer
        :type textvariable: tkinter.StringVar or None
        :param prefix: A prefix to show on every input line
        :type prefix: str
        :param force_focus: whether or not the shell should take the focus.
        :type force_focus: bool
        :param font: Font to use for the terminal
        :type font: tkinter.font.Font, tuple, or None
        """
        for key, value in {
            'background': 'black',
            'takefocus': True,
        }.items():
            if key not in kwargs:
                kwargs[key] = value
        super().__init__(master, **kwargs)
        if kwargs['takefocus'] and force_focus:
            self.focus_force()

        self.bind('<Key>', self.on_key_press)
        self.bind('<Configure>', self.on_configure)
        self.textvariable = textvariable if isinstance(textvariable, tk.StringVar) else tk.StringVar()
        self.prefix = prefix
        self.font = font or ('Terminal', 10)
        self.line_pos = (5, 5)
        self.texts = []
        self.last_text = None
        self.cursor = None
        self.blink = True
        self.buffer = prefix
        self.text_update()
        self.commands = defaultdict(list)
        self.cursor_blink()

    def on_key_press(self, event):
        if event.keysym == 'Return' and len(self.buffer) > len(self.prefix):
            self.texts.append(self.last_text)
            span = self.text_line_span()
            self.last_text = None
            self.line_pos = (5, self.line_pos[1] + 15 * span)
            self.call_command('onreturn', self.buffer[len(self.prefix):])
            self.buffer = self.prefix
            self.text_update()
            return

        if event.keysym == 'Tab':
            self.call_command('ontab', self)
            return

        if event.keysym == 'BackSpace' and len(self.buffer) > len(self.prefix):
            self.buffer = self.buffer[:-1]
            self.text_update()
            return

        if event.char.strip() or event.keysym == 'space':
            self.buffer += event.char
            self.text_update()
            return

    def on_configure(self, event):
        padding = 4
        width = self.master.winfo_width() - padding
        height = self.master.winfo_height() - padding
        self.config(width=width, height=height)
        for t in self.texts:
            self.itemconfig(t, width=width)
        self.itemconfig(self.last_text, width=width)

    def text_update(self):
        """
        Updates the text on the screen.
        """
        self.textvariable.set(self.buffer)
        if self.last_text:
            self.delete(self.last_text)
        kwargs = {
            'anchor': tk.NW,
            'fill': 'white',
            'text': self.buffer,
            'width': self['width'],
            'font': self.font,
        }
        self.last_text = self.create_text(*self.line_pos, **kwargs)
        return

    def cursor_blink(self):
        if self.cursor:
            self.delete(self.cursor)
            self.cursor = None
        if self.last_text is not None and self.blink:
            pos = self.cursor_pos
            font = self.itemcget(self.last_text, 'font').split()
            width, height = self.max_char_width, int(font[-1])
            pos = pos + (pos[0] + width, pos[1] + height)
            self.cursor = self.create_rectangle(*pos, fill='white')
        self.blink = not self.blink
        self.after(1000, self.cursor_blink)

    @property
    def max_char_width(self):
        """
        Gets the width of a W character

        :returns: width of W with the font the shell uses
        :rtype: int
        """
        font = tkfont.Font(self, font=self.itemcget(self.last_text, 'font'))
        return font.measure('W')

    @property
    def cursor_pos(self):
        text = self.itemcget(self.last_text, 'text')
        font = tkfont.Font(self, font=self.itemcget(self.last_text, 'font'))
        text_len = font.measure(text)
        width = self.max_char_width
        span = self.text_line_span()
        x = text_len % int(self['width']) + width + self.line_pos[0]
        y = self.line_pos[1] + 15 * (span - 1)
        return x, y

    def text_line_span(self):
        """
        Gets the number of lines to display the current text

        :returns: number of lines
        :rtype: int
        """
        text = self.itemcget(self.last_text, 'text')
        font = tkfont.Font(self, font=self.itemcget(self.last_text, 'font'))
        text_len = font.measure(text)
        n_lines = text_len // int(self['width']) + 1
        return n_lines

    def call_command(self, command, *args):
        """
        Calls command callbacks

        :param command: Command name to call
        :type command: str
        """
        commands = self.commands.get(command, [])
        if callable(commands):
            return commands(*args)

        for callback in commands:
            callback(*args)

    def add_command(self, command, *callbacks):
        """
        Adds a command callback

        :param command: command name to bind the callback to
        :type command: str
        :param *callbacks: list of callbacks to bind to the command
        :type *callbacks: list[callable]
        """
        assert all(callable(callback) for callback in callbacks), f'Callback should be a function'
        self.commands[command].extend(callbacks)

    def print(self, message):
        """
        Prints a message on the screen

        :param message: message to write
        :type message: str
        """
        self.buffer = message
        self.text_update()
        self.texts.append(self.last_text)
        span = self.text_line_span()
        self.last_text = None
        self.line_pos = (5, self.line_pos[1] + 15 * span)
        self.buffer = self.prefix
        self.text_update()


if __name__ == '__main__':
    import os

    def onreturn(buffer):
        import shlex
        lexed = shlex.split(buffer, posix=True)
        print(lexed)

    def contractuser(path):
        expand = os.path.expanduser('~')
        return path.replace(expand, '~')

    root = tk.Tk()
    root.title(os.getcwd())
    shell = Shell(root, prefix=contractuser(os.getcwd()) + ' ')
    shell.add_command('onreturn', onreturn)
    shell.pack()
    root.mainloop()
