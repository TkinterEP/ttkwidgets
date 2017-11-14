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
            * tickinterval: if not 0, display ticks with the given interval
            * digits: number of digits after the comma to display, default is 0
            * all ttk.Scale options:
                class, cursor, style, takefocus, command, from, length, orient,
                to, value, variable
        """
        ttk.Frame.__init__(self, master, class_='TickScale', padding=2)
        self._showvalue = kwargs.pop('showvalue', True)
        self._tickinterval = kwargs.pop('tickinterval', 0)
        self._digits = kwargs.pop('digits', 0)
        self._command = kwargs.get('command', lambda value: None)

        self._formatter = '{:.' + str(self._digits) + 'f}'

        self.style = ttk.Style(self)
        self.scale = ttk.Scale(self, **kwargs)

        self._style_name = self.scale.cget('style')
        if not self._style_name:
            self._style_name = '%s.TScale' % (str(self.scale.cget('orient')).capitalize())
        self._update_slider_length()
        self._extent = kwargs['to'] - kwargs['from_']
        self._start = kwargs['from_']
        self.ticks = []
        self.ticklabels = []
        self.label = ttk.Label(self)

        self._init()
        self._apply_style()

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
        elif key == 'digits':
            return self._digits
        else:
            return self.scale.cget(key)

    def configure(self, cnf={}, **kw):
        kw.update(cnf)
        reinit = False
        if 'showvalue' in kw:
            self._showvalue = kw.pop('showvalue')
            reinit = True
        if 'tickinterval' in kw:
            self._tickinterval = kw.pop('tickinterval')
            reinit = True
        if 'digits' in kw:
            self._digits = kw.pop('digits')
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
            else:
                self._style_name = self._style_name.replace('Vertical', 'Horizontal')
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
        self.rowconfigure(0, weight=1)
        self.scale.grid(row=0, sticky='ns')
        padx1, padx2 = 0, 0
        # showvalue
        if self._showvalue:
            self.label.configure(text=self._formatter.format(self._start))
            self.label.place(in_=self.scale, bordermode='outside', x=-1, y=0,
                             anchor='e')
            self.update_idletasks()
            padx1 = self.label.winfo_width()
            self.label.configure(text=self._formatter.format(self._start + self._extent))
            self.update_idletasks()
            padx1 = max(self.label.winfo_width(), padx1) + 1
            self._display_value_vertical(self.scale.get())

        # ticks
        if self._tickinterval:
            self.ticks = []
            self.ticklabels = []
            nb_interv = int(round(self._extent / self._tickinterval))
            for i in range(nb_interv + 1):
                tick = self._start + i * self._tickinterval
                self.ticks.append(tick)
                self.ticklabels.append(ttk.Label(self, text=self._formatter.format(tick)))
                self.ticklabels[i].place(in_=self.scale, bordermode='outside',
                                         x=-1 - padx1, y=0,
                                         anchor='e')
                self.update_idletasks()
                padx2 = max(self.ticklabels[i].winfo_width(), padx2)
            self._place_ticks_vertical()
        self.scale.grid_configure(padx=(padx1 + padx2 + 1, 0), pady=0)

    def _init_horizontal(self):
        """Create and grid the widgets for a horizontal orientation."""
        self.columnconfigure(0, weight=1)
        pady1, pady2 = 0, 0
        # showvalue
        if self._showvalue:
            self.label.configure(text=self._formatter.format(self._start))
            self.label.place(in_=self.scale, bordermode='outside', x=0, y=0, anchor='s')
            pady1 = self._display_value_horizontal(self.scale.get())

        self.scale.grid(row=0, sticky='ew')

        # ticks
        if self._tickinterval:
            self.ticks = []
            self.ticklabels = []
            nb_interv = int(round(self._extent / self._tickinterval))
            for i in range(nb_interv + 1):
                tick = self._start + i * self._tickinterval
                self.ticks.append(tick)
                self.ticklabels.append(ttk.Label(self, text=self._formatter.format(tick)))
                self.ticklabels[i].place(in_=self.scale, bordermode='outside', x=0, rely=1, anchor='n')
            pady2 = self._place_ticks_horizontal()
        self.scale.grid_configure(pady=(pady1, pady2), padx=0)

    def _display_value_horizontal(self, value):
        pad = 0
        if self._showvalue:
            # position (in pixel) of the center of the slider
            x = self.convert_to_pixels(float(value))
            # pay attention to the borders
            half_width = self.label.winfo_width() / 2
            if x + half_width > self.scale.winfo_width():
                x = self.scale.winfo_width() - half_width
            elif x - half_width < 0:
                x = half_width
            self.label.place_configure(x=x)
            self.label.configure(text=self._formatter.format(float(value)))
            self.update_idletasks()
            pad = self.label.winfo_height()
        return pad

    def _display_value_vertical(self, value):
        if self._showvalue:
            y = self.convert_to_pixels(float(value))
            self.label.place_configure(y=y)
            self.label.configure(text=self._formatter.format(float(value)))
        return 0

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
        return label.winfo_height()

    def _place_ticks_vertical(self):
        for tick, label in zip(self.ticks, self.ticklabels):
            y = self.convert_to_pixels(tick)
            label.place_configure(y=y)
        return 0

    def _style_change(self, event=None):
        """Apply style and update widgets position."""
        self._apply_style()
        self.update_idletasks()
        self._update_slider_length()
        self._update_display(event)

    def _update_display(self, event):
        """Redisplay the ticks and the label so that they adapt to the new size of the scale."""
        pady1, pady2 = 0, 0
        try:
            if self._showvalue:
                pady1 = self.display_value(self.scale.get())
            if self._tickinterval:
                pady2 = self.place_ticks()
        except tk.TclError:
            # happens when configure is called during an orientation change
            pass
        self.scale.grid_configure(pady=(pady1, pady2))
