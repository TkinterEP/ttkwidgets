"""
Author: Juliette Monsel
License: GNU GPLv3
Source: This repository
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    from tkinter import ttk
    import tkinter as tk


class TickScale(ttk.Frame):
    """
    A :class:`ttk.Scale` that can display the current value next to the slider and
    supports ticks.
    """
    def __init__(self, master=None, **kwargs):
        """
        Create a TickScale with parent master.

        :param master: master widget
        :type master: widget
        :param digits: number of digits after the comma to display, 
                       if negative use the %g format
        :type digits: int
        :param labelpos: "n", "s", "e or "w": if showvalue is True, 
                          position of the label
        :type labelpos: str
        :param resolution: increment by which the slider can be moved. 
                           0 means continuous sliding.
        :type resolution: float
        :param showvalue: whether to display current value next to the slider
        :type showvalue: bool
        :param tickinterval: if not 0, display ticks with the given interval
        :type tickinterval: float
        :param tickpos: "w" or "e" (vertical scale), "n" or "s" (horizontal scale): if tickinterval is not 0, position of the ticks
        :type tickpos: str
        :param kwargs: options to be passed on to the :class:`ttk.Scale` initializer
                       (class, cursor, style, takefocus, command, from, 
                       length, orient, to, value, variable)

        .. note:: The style must derive from "Vertical.TScale" or 
                  "Horizontal.TScale" depending on the orientation. 
                  Depending on the theme, the default slider length 
                  might not be correct. If it is the case, this can
                  be solve by setting the 'sliderlength' through 
                  :class:`ttk.Style`.
        """
        ttk.Frame.__init__(self, master, class_='TickScale', padding=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._showvalue = kwargs.pop('showvalue', True)
        self._tickinterval = kwargs.pop('tickinterval', 0)
        try:
            self._resolution = float(kwargs.pop('resolution', 0))
            if self._resolution < 0:
                raise ValueError("'resolution' must be non negative.")
        except ValueError:
            raise TypeError("'resolution' must be a float.")
        if self._tickinterval != 0 and self._resolution > self._tickinterval:
            self._tickinterval = self._resolution

        orient = kwargs.get('orient', 'horizontal')
        self._labelpos = kwargs.pop('labelpos',
                                    'n' if orient == 'horizontal' else 'w')
        if self._labelpos not in ['w', 'e', 'n', 's']:
            raise ValueError("'labelpos' must be 'n', 's', 'e', or 'w'.")
        self._tickpos = kwargs.pop('tickpos',
                                   's' if orient == 'horizontal' else 'w')

        self._digits = kwargs.pop('digits', None)

        if 'variable' not in kwargs:
            self._var = tk.DoubleVar(self)
            kwargs['variable'] = self._var
        else:
            self._var = kwargs['variable']

        self.style = ttk.Style(self)
        self.scale = ttk.Scale(self, **kwargs)

        if self._resolution > 0:
            nb_steps = round((self.scale.cget('to') - self.scale.cget('from')) / self._resolution)
            self.scale.configure(to=self.scale.cget('from') + nb_steps * self._resolution)

        # adapt resolution, digits and tickinterval to avoid conflicting values
        interv = self._get_precision(self._tickinterval)
        resol = self._get_precision(self._resolution)
        from_ = self._get_precision(self.scale.cget('from'))
        to = self._get_precision(self.scale.cget('to'))
        d = max(interv, resol, from_, to)
        if self._tickinterval == 0 and self._resolution == 0:
            if self._digits is None:
                self._digits = -1
        else:
            if self._digits is None:
                self._digits = d
            if 0 <= self._digits < d:
                self._resolution = float('1e-{}'.format(self._digits))
                self._tickinterval = round(self._tickinterval, self._digits)
                if self._resolution > self._tickinterval:
                    self._tickinterval = self._resolution
                self.scale.configure(from_=round(self.scale.get('from'), self._digits),
                                     to=round(self.scale.get('to'), self._digits))

        if not isinstance(self._digits, int):
            raise TypeError("'digits' must be an integer.")

        if self._digits < 0:
            self._formatter = '{:g}'
        else:
            self._formatter = '{:.' + str(self._digits) + 'f}'

        if orient == 'vertical' and self._tickpos not in ['w', 'e']:
            raise ValueError("For a vertical TickScale, 'tickpos' must be 'w' or 'e'.")
        elif orient == 'horizontal' and self._tickpos not in ['n', 's']:
            raise ValueError("For a horizontal TickScale, 'tickpos' must be 'n' or 's'.")

        self._style_name = self.scale.cget('style')
        if not self._style_name:
            self._style_name = '%s.TScale' % (str(self.scale.cget('orient')).capitalize())
        self._sliderlength = self.style.lookup(self._style_name, 'sliderlength', default=30)
        self._extent = self.scale.cget('to') - self.scale.cget('from')
        self._start = self.scale.cget('from')
        self._var.set(self._start)
        self.ticks = []
        self.ticklabels = []
        self.label = ttk.Label(self, padding=1)

        try:
            self._trace = self._var.trace_add('write', self._increment)
        except AttributeError:
            # backward compatibility
            self._trace = self._var.trace('w', self._increment)

        self._apply_style()
        self._init()

        self.scale.bind('<Configure>', self._update_display)
        self.scale.bind('<<ThemeChanged>>', self._style_change)

        self.set = self.scale.set
        self.coords = self.scale.coords
        self.instate = self.scale.instate
        self.state = self.scale.state

    def __getitem__(self, item):
        return self.cget(item)

    def __setitem__(self, item, value):
        self.configure({item: value})

    @staticmethod
    def _get_precision(number):
        """
        Return the number of digits after the comma necessary to display number.

        The default number of digits after the comma of '%f' is 6, so -1 is
        returned if number < 1e-6
        """
        if number < 1e-6:
            return -1
        else:
            return '{:f}'.format(number).strip('0')[::-1].find('.')

    def keys(self):
        keys = self.scale.keys()
        return keys + ['showvalue', 'tickinterval', 'digits']

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method :meth:`~TickScale.keys`.
        """
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
        elif key == 'resolution':
            return self._resolution
        else:
            return self.scale.cget(key)

    def configure(self, cnf={}, **kw):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method :meth:`~TickScale.keys`.
        See :meth:`~TickScale.__init__` for a description of the widget specific option.
        """
        kw.update(cnf)
        reinit = False
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
        if 'resolution' in kw:
            try:
                self._resolution = float(kw.pop('resolution'))
                if self._resolution < 0:
                    raise ValueError("'resolution' must be non negative.")
            except ValueError:
                raise TypeError("'resolution' must be a float.")
        if self._tickinterval != 0 and self._resolution > self._tickinterval:
            self._tickinterval = self._resolution
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
                interv = self._get_precision(self._tickinterval)
                resol = self._get_precision(self._resolution)
                start = kw.get('from', kw.get('from_', self._start))
                end = kw.get('to', self.scale.cget('to'))
                from_ = self._get_precision(start)
                to = self._get_precision(end)
                d = max(interv, resol, from_, to)
                if self._digits < d:
                    self._resolution = float('1e-{}'.format(self._digits))
                    self._tickinterval = round(self._tickinterval, self._digits)
                    if self._resolution > self._tickinterval:
                        self._tickinterval = self._resolution
                    kw['to'] = round(end, self._digits)
                    if 'from_' in kw:
                        del kw['from_']
                    kw['from'] = round(start, self._digits)
                reinit = True
        elif self._digits > 0:
            start = kw.get('from', kw.get('from_', self._start))
            end = kw.get('to', self.scale.cget('to'))
            from_ = self._get_precision(start)
            to = self._get_precision(end)
            interv = self._get_precision(self._tickinterval)
            resol = self._get_precision(self._resolution)
            digits = max(self._digits, interv, resol, from_, to)
            if digits != self._digits:
                self._digits = digits
                self._formatter = '{:.' + str(self._digits) + 'f}'
                reinit = True
        if 'variable' in kw:
            self._var = kw['variable']
            if not self._var:
                self._var = tk.DoubleVar(self, self.get())
                kw['variable'] = self._var
            try:
                self._var.trace_add('write', self._increment)
            except AttributeError:
                # backward compatibility
                self._var.trace('w', self._increment)

        self.scale.configure(**kw)

        if 'from_' in kw or 'from' in kw or 'to' in kw:
            self._extent = self.scale.cget('to') - self.scale.cget('from')
            self._start = self.scale.cget('from')
            reinit = True
        if 'style' in kw:
            self._style_name = kw['style']
            if not self._style_name:
                self._style_name = '%s.TScale' % (str(self.scale.cget('orient')).capitalize())
        if reinit:
            self._init()
        if 'orient' in kw:
            # needed after the reinitialization in case of orientation change
            self._apply_style()

    config = configure

    def get(self):
        if self._digits >= 0:
            return round(self.scale.get(), self._digits)
        else:
            return self.scale.get()

    def convert_to_pixels(self, value):
        """
        Convert value in the scale's unit into a position in pixels.
        
        :param value: value to convert
        :type value: float
        
        :return: the corresponding position in pixels
        :rtype: float
        """
        percent = ((value - self._start) / self._extent)
        return percent * (self.get_scale_length() - self._sliderlength) + self._sliderlength / 2

    def _update_slider_length_horizontal(self):
        """
        Measure the length of the slider and update the value of self._sliderlength.

        self.scale.identify(x, y) is used to find the first and last pixels of
        the slider. Indeed, self.scale.identify(x, y) returns the element
        of the ttk.Scale to which the pixel (x, y) belongs. So, the length of
        the slider is determined by scanning horizontally the pixels of the scale.
        """
        if not self.scale.identify(2, 2):
            # if self.scale.identify(2, 2) is an empty string it means that the scale
            # is not displayed yet so we cannot measure the length of the slider,
            # so wait for the scale to be properly displayed.
            # binding to <Map> event does not work, it can still be to soon to
            # get any result from identify
            self.after(10, self._update_slider_length_horizontal)
        else:
            w = self.scale.winfo_width()
            i = 0
            # find the first pixel of the slider
            while i < w and 'slider' not in self.scale.identify(i, 2):
                # increment i until the pixel (i, 2) belongs to the slider
                i += 1
            j = i
            # find the last pixel of the slider
            while j < w and 'slider' in self.scale.identify(j, 2):
                # increment j until the pixel (2, j) no longer belongs to the slider
                j += 1
            if j == i:
                # the length of the slider was not determined properly,
                # so the value of the sliderlength from the style is used
                self._sliderlength = self.style.lookup(self._style_name, 'sliderlength', default=30)
            else:
                # update ticks and label placement
                self._sliderlength = j - i
            self._update_display()

    def _update_slider_length_vertical(self):
        """
        Measure the length of the slider and update the value of self._sliderlength.

        self.scale.identify(x, y) is used to find the first and last pixels of
        the slider. Indeed, self.scale.identify(x, y) returns the element
        of the ttk.Scale to which the pixel (x, y) belongs. So, the length of
        the slider is determined by scanning vertically the pixels of the scale.
        """
        if not self.scale.identify(2, 2):
            # if self.scale.identify(2, 2) is an empty string it means that the scale
            # is not displayed yet so we cannot measure the length of the slider,
            # so wait for the scale to be properly displayed.
            # binding to <Map> event does not work, it can still be to soon to
            # get any result from identify
            self.after(10, self._update_slider_length_vertical)
        else:
            h = self.scale.winfo_height()
            i = 0
            # find the first pixel of the slider
            while i < h and 'slider' not in self.scale.identify(2, i):
                # increment i until the pixel (2, i) belongs to the slider
                i += 1
            j = i
            # find the last pixel of the slider
            while j < h and 'slider' in self.scale.identify(2, j):
                # increment j until the pixel (2, j) no longer belongs to the slider
                j += 1
            if j == i:
                # the length of the slider was not determined properly,
                # so the value of the sliderlength from the style is used
                self._sliderlength = self.style.lookup(self._style_name, 'sliderlength', default=30)
            else:
                self._sliderlength = j - i
            # update ticks and label placement
            self._update_display()

    def _apply_style(self):
        """Apply the scale style to the frame and labels."""
        ttk.Frame.configure(self, style=self._style_name + ".TFrame")
        self.label.configure(style=self._style_name + ".TLabel")
        bg = self.style.lookup('TFrame', 'background', default='light grey')
        for label in self.ticklabels:
            label.configure(style=self._style_name + ".TLabel")
        self.style.configure(self._style_name + ".TFrame",
                             background=self.style.lookup(self._style_name,
                                                          'background',
                                                          default=bg))
        self.style.map(self._style_name + ".TFrame",
                       background=self.style.map(self._style_name, 'background'))
        self.style.configure(self._style_name + ".TLabel",
                             font=self.style.lookup(self._style_name, 'font', default='TkDefaultFont'),
                             background=self.style.lookup(self._style_name, 'background', default=bg),
                             foreground=self.style.lookup(self._style_name, 'foreground', default='black'))
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
        if self._resolution > 0:
            nb_steps = round((self.scale.cget('to') - self.scale.cget('from')) / self._resolution)
            self.scale.configure(to=self.scale.cget('from') + nb_steps * self._resolution)
            self._extent = self.scale.cget('to') - self.scale.cget('from')
        if str(self.scale.cget('orient')) == "horizontal":
            self.get_scale_length = self.scale.winfo_width
            self.display_value = self._display_value_horizontal
            self._update_slider_length = self._update_slider_length_horizontal
            self.place_ticks = self._place_ticks_horizontal
            self._init_horizontal()
        else:
            self.get_scale_length = self.scale.winfo_height
            self.display_value = self._display_value_vertical
            self._update_slider_length = self._update_slider_length_vertical
            self.place_ticks = self._place_ticks_vertical
            self._init_vertical()
        self.scale.lift()
        try:
            self._var.trace_remove('write', self._trace)
            self._trace = self._var.trace_add('write', self._increment)
        except AttributeError:
            # backward compatibility
            self._var.trace_vdelete('w', self._trace)
            self._trace = self._var.trace('w', self._increment)
        self._update_slider_length()

    def _init_vertical(self):
        """Create and grid the widgets for a vertical orientation."""
        self.scale.grid(row=0, sticky='ns')
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
        # ticks
        padx1_2, padx2_2 = 0, 0
        if self._tickinterval:
            nb_interv = int(self._extent / self._tickinterval)
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

        # ticks
        pady1_2, pady2_2 = 0, 0
        if self._tickinterval:
            nb_interv = int(self._extent / self._tickinterval)
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
            self.update_idletasks()
        self.scale.grid_configure(pady=(pady1 + pady1_2, pady2 + pady2_2),
                                  padx=(padx1, padx2))

    def _display_value_horizontal(self, value):
        """Display the current value and update the label position."""
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
        """Display the current value and update the label position."""
        if self._showvalue:
            self.label.configure(text=self._formatter.format(float(value)))
            if self._labelpos in ['e', 'w']:
                y = self.convert_to_pixels(float(value))
                self.label.place_configure(y=y)

    def _place_ticks_horizontal(self):
        """Display the ticks for a horizontal scale."""
        # first tick
        tick = self.ticks[0]
        label = self.ticklabels[0]
        x = self.convert_to_pixels(tick)
        half_width = label.winfo_reqwidth() / 2
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
        half_width = label.winfo_reqwidth() / 2
        if x + half_width > self.scale.winfo_reqwidth():
            x = self.scale.winfo_width() - half_width
        label.place_configure(x=x)

    def _place_ticks_vertical(self):
        """Display the ticks for a vertical slider."""
        for tick, label in zip(self.ticks, self.ticklabels):
            y = self.convert_to_pixels(tick)
            label.place_configure(y=y)

    def _increment(self, *args):
        """Move the slider only by increment given by resolution."""
        value = self._var.get()
        if self._resolution:
            value = self._start + int(round((value - self._start) / self._resolution)) * self._resolution
            self._var.set(value)
        self.display_value(value)

    def _style_change(self, event=None):
        """Apply style and update widgets position."""
        self._apply_style()
        self._init()

    def _update_display(self, event=None):
        """Redisplay the ticks and the label so that they adapt to the new size of the scale."""
        try:
            if self._showvalue:
                self.display_value(self.scale.get())
            if self._tickinterval:
                self.place_ticks()
        except IndexError:
            # happens when configure is called during a orientation change
            # because self.ticks is empty
            pass
