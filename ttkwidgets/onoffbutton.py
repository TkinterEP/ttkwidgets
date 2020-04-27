"""
Author: Fredy Ramirez
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

# TODO:
# - takefocus (focus traversal)
# - test on linux

class OnOffButton(ttk.Frame):
    """
    A simple On/Off button.
    """

    _style_class = None
    _style_opts = None

    def __init__(self, master=None, size=24, command=None, state='!disabled',
                onvalue=1, offvalue=0, variable=None, style=None):
        """
        Create an OnOffButton.
        
        :param master: master widget
        :type master: widget
        :param size: Siwtch button diameter size.
        :type size: int
        :command: A function to be called whenever the state of this onoffbutton changes.
        :type command: callback function.
        :param state: Initial state of onoffbutton. Default '!disabled'.
        :type master: str
	    :param onvalue: Value returned by onoffbutton when it is 'on'. Default 1.
        :type onvalue: It depends of variable type.
	    :param offvalue: Value returned by onoffbutton when it is 'off'. Default 0.
        :type offvalue: It depends of variable type.
	    :param variable: A control variable that tracks the current state of the onoffbutton.
        :                It can be IntVar, BooleanVar or StringVar. Default IntVar.
        :type variable: Tk control variable.
        :style: The ttk style to be used in rendering onoffbutton. Default 'OnOffButton'.
        :       Note that onoffbutton is based on canvas drawing, wich is not a ttk widget,
        :       so some functionalitys does not work. For example, you can not change its style
        :       dinamicaly, you need to pass the style changes to onoffbutton.config(style=new_style)
        :       to take efect.
        :       'OnOffButton' style defines folowing options: background, switchcolor, oncolor, offcolor,
        :       disabledcolor and switchdisabledcolor.
        :type style: str.
        """
        OnOffButton._get_style()
        if style is None:
            curr_style = OnOffButton._style_class
        else:
            curr_style = style
            OnOffButton._validate_style(curr_style)
        # Always pass predefined style for Frame
        kwargs_frame = {'style': OnOffButton._style_class + '.TFrame'}

        super(OnOffButton, self).__init__(master, **kwargs_frame)

        self._command = command
        self._command_result = None
        self._size = self._validate_size(size)
        self._variable, self._onvalue, self._offvalue = \
                self._validate_variable(variable, onvalue, offvalue)
        self._curr_style_class = curr_style
        self._canvas = tk.Canvas(self,
                width=self._size * 2,
                height=self._size, border=-2,
            )
        self._canvas.pack()
        self._draw()
        self._variable.set(self._offvalue)

    def invoke(self):
        '''
        This method toggles the state of the onoffbutton.
        If there is a command callback, it calls that callback, and returns whatever value
        the callback returned.
        '''
        value = \
            self._offvalue if self._variable.get() == self._onvalue else self._onvalue
        self._variable.set(value)
        #TODO takefocus
        return self._command_result

    def get(self):
        """
        Get current state value of onoffbutton.
        Returns 'onvalue' or 'offvalue'.
        """
        return self._variable.get()

    def set(self, value):
        """
        Set the state value for onoffbutton.
        
        :param value: Value to set. It must be 'onvalue' or 'offvalue'.
        """
        self._variable.set(value)

    def keys(self):
        keys = super(OnOffButton, self).keys()
        keys.extend(['state', 'size',
            'variable', 'onvalue', 'offvalue'])
        keys.sort()
        return keys

    def cget(self, key):
        if key == 'state':
            return self._canvas.cget('state')
        elif key == 'size':
            return self._size
        elif key == 'variable':
            return self._variable
        elif key == 'onvalue':
            return self._onvalue
        elif key == 'offvalue':
            return self._offvalue
        elif key == 'style':
            return self._curr_style_class
        else:
            super(OnOffButton, self).cget(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        return self.configure({key: value})

    def configure(self, cnf={}, **kw):
        kw.update(cnf)
        if 'variable' in kw:
            # ignore
            kw.pop('variable')
        if 'state' in kw:
            self._canvas.configure(state=kw.pop('state'))
        if 'onvalue' in kw:
            value = kw.pop('onvalue')
            if self._onvalue != value: 
                change = True if self._variable.get() == self._onvalue else None
                self._onvalue = value
                if change: 
                    self._variable.set(value)
        if 'offvalue' in kw:
            value = kw.pop('offvalue')
            if self._onvalue != value: 
                change = True if self._variable.get() == self._offvalue else None
                self._offvalue = value
                if change: 
                    self._variable.set(value)
        if 'style' in kw:
            st = kw.pop('style')
            OnOffButton._validate_style(st)
            self._curr_style_class = st
            self._draw()
            value = \
                self._offvalue if self._variable.get() == self._offvalue else self._onvalue
            self._variable.set(value)

    config = configure

    def _draw(self):
        style = ttk.Style()
        background = style.lookup(self._curr_style_class, 'background')
        switchcolor = style.lookup(self._curr_style_class, 'switchcolor')
        oncolor = style.lookup(self._curr_style_class, 'oncolor')
        offcolor = style.lookup(self._curr_style_class, 'offcolor')
        disabledcolor = style.lookup(
                self._curr_style_class, 'disabledcolor')
        switchdisabledcolor = style.lookup(
                self._curr_style_class, 'switchdisabledcolor')

        half = self._size / 2
        space = self._size * 0.15

        self._canvas.delete('circle')
        self._canvas.delete('rectangle_off')
        self._canvas.delete('rectangle_on')
        self._canvas.tag_unbind('rectangle_on', '<Button-1>')
        self._canvas.tag_unbind('rectangle_off', '<Button-1>')
        self._canvas.config(bg=background)

        self._create_rectangle('rectangle_off', offcolor, disabledcolor, half)
        self._create_rectangle('rectangle_on', oncolor, disabledcolor, half)

        self._create_circle(
            half * 3, half, half - space,
            tag=('circle', 'right_circle'), fill=switchcolor,
            outline=None, width=0, disabledfill=switchdisabledcolor)
        self._create_circle(
            half, half, half - space,
            tag=('circle', 'left_circle'), fill=switchcolor,
            outline=None, width=0, disabledfill=switchdisabledcolor)

        self._canvas.tag_bind('rectangle_on', '<Button-1>', self._on_click)
        self._canvas.tag_bind('rectangle_off', '<Button-1>', self._on_click)

    def _create_rectangle(self, tag, fill, disabledcolor, half):
        self._canvas.create_rectangle(half, 0, half * 3, self._size,
            tag=tag, fill=fill, outline=None, width=0, disabledfill='gray')
        self._create_circle(
            half, half, half - 1, tag=tag,
                fill=fill, outline=None, width=0, disabledfill=disabledcolor)
        self._create_circle(
            half * 3, half, half - 1, tag=tag,
                fill=fill, outline=None, width=0, disabledfill=disabledcolor)

    def _create_circle(self, x, y, r, **kwargs):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self._canvas.create_oval(x0, y0, x1, y1, **kwargs)

    def _on_click(self, event=None):
        value = \
            self._offvalue if self._variable.get() == self._onvalue else self._onvalue
        self._variable.set(value)

    def _variable_write(self, a, b, c):
        value = self._variable.get()
        if value not in [self._onvalue, self._offvalue]:
            raise ValueError("Invalid value '{}'".format(value))
        self._command_result = self._toggle()

    def _toggle(self):
        self._canvas.tag_lower('circle')
        value = True if self._variable.get() == self._onvalue else None
        if value:
            self._canvas.tag_raise('rectangle_on')
            self._canvas.tag_raise('right_circle')
        else:
            self._canvas.tag_raise('rectangle_off')
            self._canvas.tag_raise('left_circle')

        self._command_result = None
        if self._command is not None:
            return self._command(self)

    @classmethod
    def _validate_style(cls, name):
        style = ttk.Style()
        add_opts = {}
        for opt, value in OnOffButton._style_opts.items():
            if not style.lookup(name, opt):
                add_opts[opt] = value
        if add_opts:
            style.configure(name, **add_opts)

    @classmethod
    def _get_style(cls):
        if OnOffButton._style_class is not None:
            return

        style = ttk.Style()
        OnOffButton._style_class = 'OnOffButton'

        # Frame style
        style.configure(OnOffButton._style_class + '.TFrame',
            background=style.lookup('TFrame', 'background'), padding=0)

        # default options
        OnOffButton._style_opts = {
                'background': style.lookup('TFrame', 'background'),
                'switchcolor': 'white',
                'oncolor': 'green',
                'offcolor': 'red',
                'disabledcolor': 'gray',
                'switchdisabledcolor': '#d9d9d9',
            }

        onoff_style = style.configure(OnOffButton._style_class)
        if onoff_style is None:
            style.configure(OnOffButton._style_class, **OnOffButton._style_opts)
        else:
            cls._validate_style(OnOffButton._style_class)

    def _validate_variable(self, variable, onvalue, offvalue):
        if variable is None:
            variable = tk.IntVar()
        if isinstance(variable, tk.IntVar):
            self._validate_type('int', 'onvalue', onvalue)
            self._validate_type('int', 'offvalue', offvalue)
        if isinstance(variable, tk.BooleanVar):
            onvalue = True
            offvalue = False
        if isinstance(variable, tk.StringVar):
            onvalue = str(onvalue)
            offvalue = str(offvalue)
        if onvalue == offvalue:
            raise ValueError('onvalue and offvalue must be diferent.')
        variable.trace_variable('w', self._variable_write)
        return variable, onvalue, offvalue

    def _validate_size(self, size):
        self._validate_type('int', 'size', size)
        if size < 12:
            size = 12
        if size > 100:
            size = 100
        return size

    def _validate_type(self, type_, field, val):
        invalid = None
        if type_ == 'int':
            if not isinstance(val, int):
                invalid = True
        if type_ == 'bool':
            if not isinstance(val, bool):
                invalid = True
        if invalid:
            raise TypeError("'{}' not of '{}' type".format(field, type_))
