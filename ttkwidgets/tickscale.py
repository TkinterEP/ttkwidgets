try:
    import Tkinter as tk
    import ttk
except ImportError:
    from tkinter import ttk
    import tkinter as tk


class TickScale(ttk.Frame):
    """
    A ttk.Scale that can display the current value next to the slider and
    supports ticks.
    """
    def __init__(self, master=None, **kwargs):
        """
        Create a TickScale with parent master.

        Arguments:
            * master: parent window
            * showvalue: display current value next to the slider
            * labelpos: if showvalue is True, position of the label:
                n, s, e, w
            * tickinterval: if not 0, display ticks with the given interval
            * tickpos: if tickinterval is not 0, position of the ticks:
                vertical scale: w or e
                horizontal scale: n or s
            * digits: number of digits after the comma to display, if negative
                use the %g format
            * all ttk.Scale options:
                class, cursor, style, takefocus, command, from, length, orient,
                to, value, variable

                The style must derive from Vertical.TScale or Horizontal.TScale
                depending on the orientation.
        """
        ttk.Frame.__init__(self, master, class_='TickScale', padding=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._showvalue = kwargs.pop('showvalue', True)
        self._tickinterval = kwargs.pop('tickinterval', 0)

        interv = str(self._tickinterval)
        self._digits = kwargs.pop('digits', interv[::-1].find('.'))
        if not isinstance(self._digits, int):
            raise TypeError("'digits' must be an integer or None.")

        if 'digits' not in kwargs and self._digits < 0:
            if 'e' not in interv:
                self._digits = 0
                self._formatter = '{:.' + str(self._digits) + 'f}'
            else:
                self._formatter = '{:g}'
        elif self._digits < 0:
            self._formatter = '{:g}'
        else:
            self._formatter = '{:.' + str(self._digits) + 'f}'

        self._command = kwargs.get('command', lambda value: None)
        orient = kwargs.get('orient', 'horizontal')
        self._labelpos = kwargs.pop('labelpos',
                                    'n' if orient == 'horizontal' else 'w')
        if self._labelpos not in ['w', 'e', 'n', 's']:
            raise ValueError("'labelpos' must be 'n', 's', 'e', or 'w'.")
        self._tickpos = kwargs.pop('tickpos',
                                   's' if orient == 'horizontal' else 'w')

        self.style = ttk.Style(self)
        self.scale = ttk.Scale(self, **kwargs)

        if orient == 'vertical' and self._tickpos not in ['w', 'e']:
            raise ValueError("For a vertical TickScale, 'tickpos' must be 'w' or 'e'.")
        elif orient == 'horizontal' and self._tickpos not in ['n', 's']:
            raise ValueError("For a horizontal TickScale, 'tickpos' must be 'n' or 's'.")

        self._style_name = self.scale.cget('style')
        if not self._style_name:
            self._style_name = '%s.TScale' % (str(self.scale.cget('orient')).capitalize())
        self._update_slider_length()
        self._extent = kwargs['to'] - kwargs['from_']
        self._start = kwargs['from_']
        self.ticks = []
        self.ticklabels = []
        self.label = ttk.Label(self, padding=1)

        self._apply_style()
        self._init()

        def cmd(value):
            self._command(value)
            self.display_value(value)

        self.scale.configure(command=cmd)

        self.scale.bind('<Configure>', self._update_display)
        self.scale.bind('<<ThemeChanged>>', self._style_change)

        self.get = self.scale.get
        self.set = self.scale.set
        self.coords = self.scale.coords
        self.instate = self.scale.instate
        self.state = self.scale.state

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, item, value):
        self.configure({item: value})

    def keys(self):
        keys = self.scale.keys()
        return keys + ['showvalue', 'tickinterval', 'digits']

    def cget(self, key):
        if key == 'showvalue':
            return self._showvalue
        elif key == 'tickinterval':
            return self._tickinterval
        elif key == 'tickpos':
            return self._tickpos
        elif key == 'labelpos':
            return self._labelpos
        elif key == 'digits':
            return self._digits
        else:
            return self.scale.cget(key)

    def configure(self, cnf={}, **kw):
        kw.update(cnf)
        reinit = False
        if 'showvalue' in kw:
            self._showvalue = bool(kw.pop('showvalue'))
            reinit = True
        if 'tickinterval' in kw:
            self._tickinterval = kw.pop('tickinterval')
            reinit = True
        if 'tickpos' in kw:
            tickpos = kw.pop('tickpos')
            orient = kw.get('orient', str(self.cget('orient')))
            if orient == 'vertical' and tickpos not in ['w', 'e']:
                raise ValueError("For a vertical TickScale, 'tickpos' must be 'w' or 'e'.")
            elif orient == 'horizontal' and tickpos not in ['n', 's']:
                raise ValueError("For a horizontal TickScale, 'tickpos' must be 'n' or 's'.")
            elif orient in ['vertical', 'horizontal']:
                self._tickpos = tickpos
                reinit = True
        if 'labelpos' in kw:
            labelpos = kw.pop('labelpos')
            if labelpos not in ['w', 'e', 'n', 's']:
                raise ValueError("'labelpos' must be 'n', 's', 'e' or 'w'.")
            else:
                self._labelpos = labelpos
                reinit = True
        if 'digits' in kw:
            digits = kw.pop('digits')
            if not isinstance(digits, int):
                raise TypeError("'digits' must be an integer.")
            elif digits < 0:
                self._digits = digits
                self._formatter = '{:g}'
                reinit = True
            else:
                self._digits = digits
                self._formatter = '{:.' + str(self._digits) + 'f}'
                reinit = True
        self.scale.configure(**kw)
        if 'from_' in kw or 'from' in kw or 'to' in kw:
            self._extent = self.scale.cget('to') - self.scale.cget('from')
            self._start = self.scale.cget('from')
            reinit = True
        if 'style' in kw:
            self._style_name = kw['style']
            if not self._style_name:
                self._style_name = '%s.TScale' % (str(self.scale.cget('orient')).capitalize())
            self._style_change()
        if 'command' in kw:
            self._command = kw['command']

            def cmd(value):
                self._command(value)
                self.display_value(value)

            self.scale.configure(command=cmd)
        if 'orient' in kw:
            if kw['orient'] == 'vertical':
                self._style_name = self._style_name.replace('Horizontal', 'Vertical')
                if 'tickpos' not in kw:
                    self._tickpos = 'w'
            else:
                self._style_name = self._style_name.replace('Vertical', 'Horizontal')
                if 'tickpos' not in kw:
                    self._tickpos = 's'
            self.scale.configure(style=self._style_name)
            reinit = True
        if reinit:
            self._init()

            def cmd(value):
                self._command(value)
                self.display_value(value)

            self.scale.configure(command=cmd)

    def config(self, cnf={}, **kw):
        self.configure(cnf={}, **kw)

    def convert_to_pixels(self, value):
        """Convert value in the scale's unit into a position in pixels."""
        percent = ((value - self._start) / self._extent)
        return percent * (self.get_scale_length() - self._sliderlength) + self._sliderlength / 2

    def _update_slider_length(self):
        self._sliderlength = self.style.lookup(self._style_name, 'sliderlength', default=30)

    def _apply_style(self):
        """Apply the scale style to the frame and labels."""
        ttk.Frame.configure(self, style=self._style_name + ".TFrame")
        self.label.configure(style=self._style_name + ".TLabel")
        for label in self.ticklabels:
            label.configure(style=self._style_name + ".TLabel")
        self.style.configure(self._style_name + ".TFrame",
                             background=self.style.lookup(self._style_name, 'background'))
        self.style.map(self._style_name + ".TFrame",
                       background=self.style.map(self._style_name, 'background'))
        self.style.configure(self._style_name + ".TLabel",
                             font=self.style.lookup(self._style_name, 'font'),
                             background=self.style.lookup(self._style_name, 'background'),
                             foreground=self.style.lookup(self._style_name, 'foreground'))
        self.style.map(self._style_name + ".TLabel",
                       font=self.style.map(self._style_name, 'font'),
                       background=self.style.map(self._style_name, 'background'),
                       foreground=self.style.map(self._style_name, 'foreground'))

    def _init(self):
        """Create and grid the widgets."""
        for label in self.ticklabels:
            label.destroy()
        self.label.place_forget()
        self.ticks = []
        self.ticklabels = []
        if str(self.scale.cget('orient')) == "horizontal":
            self.get_scale_length = self.scale.winfo_width
            self.display_value = self._display_value_horizontal
            self.place_ticks = self._place_ticks_horizontal
            self._init_horizontal()
        else:
            self.get_scale_length = self.scale.winfo_height
            self.display_value = self._display_value_vertical
            self.place_ticks = self._place_ticks_vertical
            self._init_vertical()

    def _init_vertical(self):
        """Create and grid the widgets for a vertical orientation."""
        self.scale.grid(row=0, sticky='ns')
        self.update_idletasks()
        # showvalue
        padx1, padx2 = 0, 0
        pady1, pady2 = 0, 0
        if self._showvalue:
            self.label.configure(text=self._formatter.format(self._start))
            if self._labelpos == 'w':
                self.label.place(in_=self.scale, bordermode='outside',
                                 relx=0, y=0, anchor='e')
                self.update_idletasks()
                padx1 = self.label.winfo_width()
                self.label.configure(text=self._formatter.format(self._start + self._extent))
                self.update_idletasks()
                padx1 = max(self.label.winfo_width(), padx1)
            elif self._labelpos == 'e':
                self.label.place(in_=self.scale, bordermode='outside',
                                 relx=1, y=1, anchor='w')
                self.update_idletasks()
                padx2 = self.label.winfo_width()
                self.label.configure(text=self._formatter.format(self._start + self._extent))
                self.update_idletasks()
                padx2 = max(self.label.winfo_width(), padx2)
            else:  # self._labelpos in ['n', 's']:
                if self._labelpos == 'n':
                    rely = 0
                    anchor = 's'
                    pady1 = self.label.winfo_reqheight()
                else:
                    rely = 1
                    anchor = 'n'
                    pady2 = self.label.winfo_reqheight()
                self.label.place(in_=self.scale, bordermode='outside', relx=0.5,
                                 rely=rely, anchor=anchor)
                self.update_idletasks()
                w = self.label.winfo_width()
                self.label.configure(text=self._formatter.format(self._start + self._extent))
                self.update_idletasks()
                w = max(w, self.label.winfo_width())
                ws = self.scale.winfo_reqwidth()
                if w > ws:
                    padx = (w - ws) // 2
                    if self._tickinterval:
                        if self._tickpos == 'e':
                            padx1 = padx
                        else:   # self._tickpos == 'w'
                            padx2 = padx
                    else:
                        padx1, padx2 = padx, padx

            self._display_value_vertical(self.scale.get())

        # ticks
        padx1_2, padx2_2 = 0, 0
        if self._tickinterval:
            nb_interv = int(round(self._extent / self._tickinterval))
            if self._tickpos == 'w':
                for i in range(nb_interv + 1):
                    tick = self._start + i * self._tickinterval
                    self.ticks.append(tick)
                    self.ticklabels.append(ttk.Label(self,
                                                     style=self._style_name + ".TLabel",
                                                     text=self._formatter.format(tick)))
                    self.ticklabels[i].place(in_=self.scale, bordermode='outside',
                                             x=-1 - padx1, y=0,
                                             anchor='e')
                    self.update_idletasks()
                    padx1_2 = max(self.ticklabels[i].winfo_width(), padx1_2)
            else:  # self._tickpos == 'e'
                w = self.scale.winfo_reqwidth()
                for i in range(nb_interv + 1):
                    tick = self._start + i * self._tickinterval
                    self.ticks.append(tick)
                    self.ticklabels.append(ttk.Label(self,
                                                     style=self._style_name + ".TLabel",
                                                     text=self._formatter.format(tick)))
                    self.ticklabels[i].place(in_=self.scale, bordermode='outside',
                                             x=w + 1 + padx2, y=0,
                                             anchor='w')
                    self.update_idletasks()
                    padx2_2 = max(self.ticklabels[i].winfo_width(), padx2_2)
            self._place_ticks_vertical()
        self.scale.grid_configure(padx=(padx1 + padx1_2 + 1, padx2 + padx2_2 + 1),
                                  pady=(pady1, pady2))

    def _init_horizontal(self):
        """Create and grid the widgets for a horizontal orientation."""
        self.scale.grid(row=0, sticky='ew')
        padx1, padx2 = 0, 0
        pady1, pady2 = 0, 0
        # showvalue
        if self._showvalue:
            self.label.configure(text=self._formatter.format(self._start))
            self.update_idletasks()
            if self._labelpos == 'n':
                self.label.place(in_=self.scale, bordermode='outside',
                                 rely=0, x=0, anchor='s')
                pady1 = self.label.winfo_reqheight()
            elif self._labelpos == 's':
                self.label.place(in_=self.scale, bordermode='outside',
                                 rely=1, x=0, anchor='n')
                pady2 = self.label.winfo_reqheight()
            elif self._labelpos in ['w', 'e']:
                padx = self.label.winfo_reqwidth()
                self.label.configure(text=self._formatter.format(self._start + self._extent))
                self.update_idletasks()
                padx = max(padx, self.label.winfo_reqwidth())
                if self._labelpos == 'w':
                    anchor = 'e'
                    relx = 0
                    padx1 = padx
                else:
                    anchor = 'w'
                    relx = 1
                    padx2 = padx
                self.label.place(in_=self.scale, bordermode='outside',
                                 relx=relx, rely=0.5, anchor=anchor)

                h = self.label.winfo_reqheight()
                hs = self.scale.winfo_reqheight()
                if h > hs:
                    pady = (h - hs) // 2
                    if self._tickinterval:
                        if self._tickpos == 'n':
                            pady1 = pady
                        else:   # self._tickpos == 's'
                            pady2 = pady
                    else:
                        pady1, pady2 = pady, pady

            self._display_value_horizontal(self.scale.get())

        # ticks
        pady1_2, pady2_2 = 0, 0
        if self._tickinterval:
            nb_interv = int(round(self._extent / self._tickinterval))
            h = self.scale.winfo_reqheight()
            if self._tickpos == 's':
                for i in range(nb_interv + 1):
                    tick = self._start + i * self._tickinterval
                    self.ticks.append(tick)
                    self.ticklabels.append(ttk.Label(self,
                                                     style=self._style_name + ".TLabel",
                                                     text=self._formatter.format(tick)))
                    self.ticklabels[i].place(in_=self.scale, bordermode='outside',
                                             x=0, y=h + pady2 + 1, anchor='n')
                pady2_2 = self.ticklabels[-1].winfo_reqheight()
            else:  # self._tickpos == 'n':
                for i in range(nb_interv + 1):
                    tick = self._start + i * self._tickinterval
                    self.ticks.append(tick)
                    self.ticklabels.append(ttk.Label(self,
                                                     style=self._style_name + ".TLabel",
                                                     text=self._formatter.format(tick)))
                    self.ticklabels[i].place(in_=self.scale, bordermode='outside',
                                             x=0, y=-1 - pady1, anchor='s')
                pady1_2 = self.ticklabels[-1].winfo_reqheight()
            self._place_ticks_horizontal()
        self.scale.grid_configure(pady=(pady1 + pady1_2, pady2 + pady2_2),
                                  padx=(padx1, padx2))

    def _display_value_horizontal(self, value):
        if self._showvalue:
            self.label.configure(text=self._formatter.format(float(value)))
            self.update_idletasks()
            if self._labelpos in ['n', 's']:
                # position (in pixel) of the center of the slider
                x = self.convert_to_pixels(float(value))
                # pay attention to the borders
                half_width = self.label.winfo_width() / 2
                if x + half_width > self.scale.winfo_width():
                    x = self.scale.winfo_width() - half_width
                elif x - half_width < 0:
                    x = half_width
                self.label.place_configure(x=x)

    def _display_value_vertical(self, value):
        """
        Display the current value and update the label position.
        Return the pady necessary to display the label.
        """
        if self._showvalue:
            self.label.configure(text=self._formatter.format(float(value)))
            if self._labelpos in ['e', 'w']:
                y = self.convert_to_pixels(float(value))
                self.label.place_configure(y=y)

    def _place_ticks_horizontal(self):
        # first tick
        tick = self.ticks[0]
        label = self.ticklabels[0]
        x = self.convert_to_pixels(tick)
        half_width = label.winfo_width() / 2
        if x - half_width < 0:
            x = half_width
        label.place_configure(x=x)
        # ticks in the middle
        for tick, label in zip(self.ticks[1:-1], self.ticklabels[1:-1]):
            x = self.convert_to_pixels(tick)
            label.place_configure(x=x)
        # last tick
        tick = self.ticks[-1]
        label = self.ticklabels[-1]
        x = self.convert_to_pixels(tick)
        half_width = label.winfo_width() / 2
        if x + half_width > self.scale.winfo_width():
            x = self.scale.winfo_width() - half_width
        label.place_configure(x=x)
        self.update_idletasks()

    def _place_ticks_vertical(self):
        for tick, label in zip(self.ticks, self.ticklabels):
            y = self.convert_to_pixels(tick)
            label.place_configure(y=y)

    def _style_change(self, event=None):
        """Apply style and update widgets position."""
        self._apply_style()
        self._init()
        self.update_idletasks()
        self._update_slider_length()

    def _update_display(self, event):
        """Redisplay the ticks and the label so that they adapt to the new size of the scale."""
        try:
            if self._showvalue:
                self.display_value(self.scale.get())
            if self._tickinterval:
                self.place_ticks()
        except Exception:
            # happens when configure is called during an configuration change
            pass
