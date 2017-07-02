# -*- coding:Utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: https://github.com/RedFantom/tkColorPicker

Edited by RedFantom for Python 2/3 cross-compatibility and docstring formatting
"""

"""
tkColorPicker - Alternative to colorchooser for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkColorPicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkColorPicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

try:
    import Tkinter as tk
    from ttk import Entry, Button, Label, Frame, Style
except ImportError:
    import tkinter as tk
    from tkinter.ttk import Entry, Button, Label, Frame, Style
import re
from math import atan2, sqrt, pi
import colorsys
from locale import getdefaultlocale


# in some python versions round returns a float instead of an int
if not isinstance(round(1.0), int):
    def round2(nb):
        """Round number to 0 digits and return an int."""
        return int(nb + 0.5)  # works because nb >= 0
else:
    round2 = round

# Translation
EN = {}
FR = {"Red": "Rouge", "Green": "Vert", "Blue": "Bleu",
      "Hue": "Teinte", "Saturation": "Saturation", "Value": "Valeur",
      "Cancel": "Annuler", "Color Chooser": u"Sélecteur de couleur"}

if getdefaultlocale()[0][:2] == 'fr':
    TR = FR
else:
    TR = EN


PALETTE = ("red", "dark red", "orange", "yellow", "green", "lightgreen", "blue",
           "royal blue", "sky blue", "purple", "magenta", "pink", "black",
           "white", "gray", "saddle brown", "lightgray", "wheat")


def _(text):
    return TR.get(text, text)


### conversion functions
def rgb_to_hsv(r, g, b):
    """Convert RGB color to HSV."""
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    return round2(h * 360), round2(s * 100), round2(v * 100)


def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB."""
    r, g, b = colorsys.hsv_to_rgb(h / 360., s / 100., v / 100.)
    return round2(r * 255), round2(g * 255), round2(b * 255)


def rgb_to_html(r, g, b):
    """Convert RGB color to hexadecimal."""
    return ("#%2.2x%2.2x%2.2x" % (r, g, b)).upper()


def html_to_rgb(color):
    """Convert hexadecimal color to RGB."""
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:], 16)
    return r, g, b


def col2hue(r, g, b):
    """Return hue value corresponding to given RGB color."""
    return round2(180 / pi * atan2(sqrt(3) * (g - b), 2 * r - g - b) + 360) % 360


def hue2col(h):
    """Return the color in RGB format corresponding to (h, 100, 100) in HSV."""
    if h < 0 or h > 360:
        raise ValueError("Hue should be between 0 and 360")
    else:
        return hsv_to_rgb(h, 100, 100)


### classes
class Spinbox(tk.Spinbox):
    """Spinbox closer to ttk look (designed to be used with clam)."""

    def __init__(self, parent, **kwargs):
        """
        Create a Spinbox.

        The keyword arguments are the same as for a tk.Spinbox.
        """
        self.style = Style(parent)
        self.frame = Frame(parent, class_="ttkSpinbox",
                           relief=kwargs.get("relief", "sunken"),
                           borderwidth=1)
        self.style.configure("%s.spinbox.TFrame" % self.frame,
                             background="white")
        self.frame.configure(style="%s.spinbox.TFrame" % self.frame)
        kwargs["relief"] = "flat"
        kwargs["highlightthickness"] = 0
        kwargs["selectbackground"] = self.style.lookup("TEntry",
                                                       "selectbackground",
                                                       ("focus",))
        kwargs["selectbackground"] = self.style.lookup("TEntry",
                                                       "selectbackground",
                                                       ("focus",))
        kwargs["selectforeground"] = self.style.lookup("TEntry",
                                                       "selectforeground",
                                                       ("focus",))
        tk.Spinbox.__init__(self, self.frame, **kwargs)
        tk.Spinbox.pack(self, padx=1, pady=1)
        self.frame.spinbox = self

        # pack/place/grid methods
        self.pack = self.frame.pack
        self.pack_slaves = self.frame.pack_slaves
        self.pack_propagate = self.frame.pack_propagate
        self.pack_configure = self.frame.pack_configure
        self.pack_info = self.frame.pack_info
        self.pack_forget = self.frame.pack_forget

        self.grid = self.frame.grid
        self.grid_slaves = self.frame.grid_slaves
        self.grid_size = self.frame.grid_size
        self.grid_rowconfigure = self.frame.grid_rowconfigure
        self.grid_remove = self.frame.grid_remove
        self.grid_propagate = self.frame.grid_propagate
        self.grid_info = self.frame.grid_info
        self.grid_location = self.frame.grid_location
        self.grid_columnconfigure = self.frame.grid_columnconfigure
        self.grid_configure = self.frame.grid_configure
        self.grid_forget = self.frame.grid_forget
        self.grid_bbox = self.frame.grid_bbox
        try:
            self.grid_anchor = self.frame.grid_anchor
        except AttributeError:
            pass

        self.place = self.frame.place
        self.place_configure = self.frame.place_configure
        self.place_forget = self.frame.place_forget
        self.place_info = self.frame.place_info
        self.place_slaves = self.frame.place_slaves

        self.bind_class("ttkSpinbox", "<FocusIn>", self.focusin, True)
        self.bind_class("ttkSpinbox", "<FocusOut>", self.focusout, True)

    @staticmethod
    def focusout(event):
        """Change style on focus out events."""
        w = event.widget.spinbox
        bc = w.style.lookup("TEntry", "bordercolor", ("!focus",))
        dc = w.style.lookup("TEntry", "darkcolor", ("!focus",))
        lc = w.style.lookup("TEntry", "lightcolor", ("!focus",))
        w.style.configure("%s.spinbox.TFrame" % event.widget, bordercolor=bc,
                          darkcolor=dc, lightcolor=lc)

    @staticmethod
    def focusin(event):
        """Change style on focus in events."""
        w = event.widget.spinbox
        w.old_value = w.get()
        bc = w.style.lookup("TEntry", "bordercolor", ("focus",))
        dc = w.style.lookup("TEntry", "darkcolor", ("focus",))
        lc = w.style.lookup("TEntry", "lightcolor", ("focus",))
        w.style.configure("%s.spinbox.TFrame" % event.widget, bordercolor=bc,
                          darkcolor=dc, lightcolor=lc)


class ColorSquare(tk.Canvas):
    """Square color gradient with selection cross."""

    def __init__(self, parent, hue, color=None, height=256, width=256, **kwargs):
        """
        Create a ColorSquare.

        Keyword arguments:
            * parent: parent window
            * hue: color square gradient for given hue (color in top right corner
                   is (hue, 100, 100) in HSV
            * color: initially selected color given in HSV
            * width, height and any keyword option accepted by a tkinter Canvas
        """
        tk.Canvas.__init__(self, parent, height=height, width=width, **kwargs)
        self.bg = tk.PhotoImage(width=width, height=height, master=self)
        self._hue = hue
        if not color:
            color = hue2col(hue)
        self.bind('<Configure>', lambda e: self._draw(color))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _fill(self):
        """Create the gradient."""
        r, g, b = hue2col(self._hue)
        width = self.winfo_width()
        height = self.winfo_height()
        h = float(height - 1)
        w = float(width - 1)
        if height:
            c = [(r + i / h * (255 - r), g + i / h * (255 - g), b + i / h * (255 - b)) for i in range(height)]
            data = []
            for i in range(height):
                line = []
                for j in range(width):
                    rij = round2(j / w * c[i][0])
                    gij = round2(j / w * c[i][1])
                    bij = round2(j / w * c[i][2])
                    color = rgb_to_html(rij, gij, bij)
                    line.append(color)
                data.append("{" + " ".join(line) + "}")
            self.bg.put(" ".join(data))

    def _draw(self, color):
        """Draw the gradient and the selection cross on the canvas."""
        width = self.winfo_width()
        height = self.winfo_height()
        self.delete("bg")
        self.delete("cross_h")
        self.delete("cross_v")
        del(self.bg)
        self.bg = tk.PhotoImage(width=width, height=height, master=self)
        self._fill()
        self.create_image(0, 0, image=self.bg, anchor="nw", tags="bg")
        self.tag_lower("bg")
        h, s, v = color
        x = v / 100.
        y = (1 - s / 100.)
        self.create_line(0, y * height, width, y * height, tags="cross_h",
                         fill="#C2C2C2")
        self.create_line(x * width, 0, x * width, height, tags="cross_v",
                         fill="#C2C2C2")

    def get_hue(self):
        """Return hue."""
        return self._hue

    def set_hue(self, value):
        """Set hue."""
        old = self._hue
        self._hue = value
        if value != old:
            self._fill()

    def _on_click(self, event):
        """Move cross on click."""
        x = event.x
        y = event.y
        self.coords('cross_h', 0, y, self.winfo_width(), y)
        self.coords('cross_v', x, 0, x, self.winfo_height())

    def _on_move(self, event):
        """Make the cross follow the cursor."""
        w = self.winfo_width()
        h = self.winfo_height()
        x = min(max(event.x, 0), w)
        y = min(max(event.y, 0), h)
        self.coords('cross_h', 0, y, w, y)
        self.coords('cross_v', x, 0, x, h)

    def get(self):
        """Return selected color with format (RGB, HSV, HTML)."""
        x = self.coords('cross_v')[0]
        y = self.coords('cross_h')[1]
        xp = min(x, self.bg.width() - 1)
        yp = min(y, self.bg.height() - 1)
        try:
            r, g, b = self.bg.get(round2(xp), round2(yp))
        except ValueError:
            r, g, b = self.bg.get(round2(xp), round2(yp)).split()
            r, g, b = int(r), int(g), int(b)
        html = rgb_to_html(r, g, b)
        h = self.get_hue()
        s = round2((1 - float(y) / self.winfo_height()) * 100)
        v = round2(100 * float(x) / self.winfo_width())
        return (r, g, b), (h, s, v), html

    def set_rgb(self, sel_color):
        """Put cursor on sel_color given in RGB."""
        width = self.winfo_width()
        height = self.winfo_height()
        h, s, v = rgb_to_hsv(*sel_color)
        self.set_hue(h)
        x = v / 100.
        y = (1 - s / 100.)
        self.coords('cross_h', 0, y * height, width, y * height)
        self.coords('cross_v', x * width, 0, x * width, height)

    def set_hsv(self, sel_color):
        """Put cursor on sel_color given in HSV."""
        width = self.winfo_width()
        height = self.winfo_height()
        h, s, v = sel_color
        self.set_hue(h)
        x = v / 100.
        y = (1 - s / 100.)
        self.coords('cross_h', 0, y * height, width, y * height)
        self.coords('cross_v', x * width, 0, x * width, height)


class GradientBar(tk.Canvas):
    """HSV gradient colorbar with selection cursor."""

    def __init__(self, parent, hue=0, height=10, width=256, **kwargs):
        """
        Create a GradientBar.

        Keyword arguments:
            * parent: parent window
            * hue: initially selected hue value
            * height, width, and any keyword argument accepted by a tkinter Canvas
        """
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        self.bind('<Configure>', lambda e: self._draw_gradient(hue))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _draw_gradient(self, hue):
        """Draw the gradient and put the cursor on hue."""
        self.delete("gradient")
        self.delete("cursor")
        del(self.gradient)
        width = self.winfo_width()
        height = self.winfo_height()

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        line = []
        for i in range(width):
            line.append(rgb_to_html(*hue2col(float(i) / width * 360)))
        line = "{" + " ".join(line) + "}"
        self.gradient.put(" ".join([line for j in range(height)]))
        self.create_image(0, 0, anchor="nw", tags="gardient",
                          image=self.gradient)
        self.lower("gradient")

        x = hue / 360. * width
        self.create_line(x, 0, x, height, width=2, tags='cursor')

    def _on_click(self, event):
        """Move selection cursor on click."""
        x = event.x
        self.coords('cursor', x, 0, x, self.winfo_height())

    def _on_move(self, event):
        """Make selection cursor follow the cursor."""
        w = self.winfo_width()
        x = min(max(event.x, 0), w)
        self.coords('cursor', x, 0, x, self.winfo_height())

    def get(self):
        """Return hue of color under cursor."""
        coords = self.coords('cursor')
        return round2(360 * coords[0] / self.winfo_width())

    def set(self, hue):
        """Set cursor position on the color corresponding to the hue value."""
        x = hue / 360. * self.winfo_width()
        self.coords('cursor', x, 0, x, self.winfo_height())


class ColorPicker(tk.Toplevel):
    """Color picker dialog."""

    def __init__(self, parent=None, color=(255, 0, 0), title=_("Color Chooser")):
        """
        Create a ColorPicker dialog.

        Arguments:
            * parent: parent window
            * color: initially selected color in rgb or html format
            * title: dialog title
        """
        tk.Toplevel.__init__(self, parent)

        self.title(title)
        self.transient(self.master)
        self.resizable(False, False)

        self.color = ""
        style = Style(self)
        style.map("palette.TFrame", relief=[('focus', 'sunken')],
                  bordercolor=[('focus', "#4D4D4D")])
        self.configure(background=style.lookup("TFrame", "background"))

        if isinstance(color, str):
            if re.match(r"^#[0-9A-F]{6}$", color):
                self.old_color = html_to_rgb(color)
                old_color = color
            else:
                col = self.winfo_rgb(color)
                self.old_color = tuple(round2(c * 255 / 65535) for c in col)
                old_color = rgb_to_html(*self.old_color)
        else:
            self.old_color = color
            old_color = rgb_to_html(*color)

        hue = col2hue(*self.old_color)
        bar = Frame(self, borderwidth=2, relief='groove')
        self.bar = GradientBar(bar, hue=hue, width=200, highlightthickness=0)
        self.bar.pack()

        square = Frame(self, borderwidth=2, relief='groove')
        self.square = ColorSquare(square, hue=hue, width=200, height=200,
                                  color=rgb_to_hsv(*self.old_color),
                                  highlightthickness=0)
        self.square.pack()

        frame = Frame(self)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        ### color preview: initial color and currently selected color side by side
        preview_frame = Frame(frame, relief="groove", borderwidth=2)
        preview_frame.grid(row=0, column=0, sticky="sw")
        l = tk.Label(preview_frame, background=old_color, width=5,
                     highlightthickness=0, height=2)
        l.bind("<1>", self._palette_cmd)
        l.grid(row=0, column=0)
        self.color_preview = tk.Label(preview_frame, background=old_color,
                                      width=5, height=2, highlightthickness=0)
        self.color_preview.grid(row=0, column=1)
        ### palette
        palette = Frame(frame)
        palette.grid(row=0, column=1, sticky="e")
        for i, col in enumerate(PALETTE):
            f = Frame(palette, borderwidth=1, relief="raised",
                      style="palette.TFrame")
            l = tk.Label(f, background=col, width=2, height=1)
            l.bind("<1>", self._palette_cmd)
            f.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            l.pack()
            f.grid(row=i % 2, column=i // 2, padx=2, pady=2)

        col_frame = Frame(self)
        ### hsv
        hsv_frame = Frame(col_frame, relief="ridge", borderwidth=2)
        hsv_frame.pack(pady=(0, 4), fill="x")
        hsv_frame.columnconfigure(0, weight=1)
        self.hue = tk.StringVar(self)
        self.saturation = tk.StringVar(self)
        self.value = tk.StringVar(self)

        s_h = Spinbox(hsv_frame, from_=0, to=360, width=4,
                      textvariable=self.hue, command=self._update_color_hsv)
        s_s = Spinbox(hsv_frame, from_=0, to=100, width=4,
                      textvariable=self.saturation,
                      command=self._update_color_hsv)
        s_v = Spinbox(hsv_frame, from_=0, to=100, width=4,
                      textvariable=self.value, command=self._update_color_hsv)
        h, s, v = rgb_to_hsv(*self.old_color)
        s_h.delete(0, 'end')
        s_h.insert(0, h)
        s_s.delete(0, 'end')
        s_s.insert(0, s)
        s_v.delete(0, 'end')
        s_v.insert(0, v)
        s_h.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        s_s.grid(row=1, column=1, sticky='w', padx=4, pady=4)
        s_v.grid(row=2, column=1, sticky='w', padx=4, pady=4)
        Label(hsv_frame, text=_('Hue')).grid(row=0, column=0, sticky='e',
                                             padx=4, pady=4)
        Label(hsv_frame, text=_('Saturation')).grid(row=1, column=0, sticky='e',
                                                    padx=4, pady=4)
        Label(hsv_frame, text=_('Value')).grid(row=2, column=0, sticky='e',
                                               padx=4, pady=4)

        ### rgb
        rgb_frame = Frame(col_frame, relief="ridge", borderwidth=2)
        rgb_frame.pack(pady=6, fill="x")
        rgb_frame.columnconfigure(0, weight=1)
        self.red = tk.StringVar(self)
        self.green = tk.StringVar(self)
        self.blue = tk.StringVar(self)

        s_red = Spinbox(rgb_frame, from_=0, to=255, width=4,
                        textvariable=self.red, command=self._update_color_rgb)
        s_green = Spinbox(rgb_frame, from_=0, to=255, width=4,
                          textvariable=self.green, command=self._update_color_rgb)
        s_blue = Spinbox(rgb_frame, from_=0, to=255, width=4,
                         textvariable=self.blue, command=self._update_color_rgb)
        s_red.delete(0, 'end')
        s_red.insert(0, self.old_color[0])
        s_green.delete(0, 'end')
        s_green.insert(0, self.old_color[1])
        s_blue.delete(0, 'end')
        s_blue.insert(0, self.old_color[2])
        s_red.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        s_green.grid(row=1, column=1, sticky='w', padx=4, pady=4)
        s_blue.grid(row=2, column=1, sticky='w', padx=4, pady=4)
        Label(rgb_frame, text=_('Red')).grid(row=0, column=0, sticky='e',
                                             padx=4, pady=4)
        Label(rgb_frame, text=_('Green')).grid(row=1, column=0, sticky='e',
                                               padx=4, pady=4)
        Label(rgb_frame, text=_('Blue')).grid(row=2, column=0, sticky='e',
                                              padx=4, pady=4)

        ### html
        html_frame = Frame(col_frame)
        html_frame.pack(pady=(6, 0), fill="x")
        self.html = Entry(html_frame, justify="center", width=10)
        self.html.insert(0, old_color)
        Label(html_frame, text="HTML").pack(side="left", padx=4, pady=4)
        self.html.pack(side="left", padx=4, pady=4)

        ### validation
        button_frame = Frame(self)
        Button(button_frame, text="Ok",
               command=self.ok).pack(side="right", padx=10)
        Button(button_frame, text=_("Cancel"),
               command=self.destroy).pack(side="right", padx=10)

        ### placement
        bar.grid(row=0, column=0, padx=10, pady=(10, 2))
        square.grid(row=1, column=0, padx=10, pady=2)
        frame.grid(row=2, column=0, columnspan=2, pady=(4, 10), padx=10, sticky="ew")
        col_frame.grid(row=0, rowspan=2, column=1, padx=(4, 10), pady=(10, 4))
        button_frame.grid(row=3, columnspan=2, pady=(0, 10), padx=10)

        ### bindings
        self.bar.bind("<ButtonRelease-1>", self._change_color, True)
        self.bar.bind("<Button-1>", self._unfocus, True)
        self.square.bind("<Button-1>", self._unfocus, True)
        self.square.bind("<ButtonRelease-1>", self._change_sel_color, True)
        self.square.bind("<B1-Motion>", self._change_sel_color, True)
        s_red.bind('<FocusOut>', self._update_color_rgb)
        s_green.bind('<FocusOut>', self._update_color_rgb)
        s_blue.bind('<FocusOut>', self._update_color_rgb)
        s_red.bind('<Return>', self._update_color_rgb)
        s_green.bind('<Return>', self._update_color_rgb)
        s_blue.bind('<Return>', self._update_color_rgb)
        s_h.bind('<FocusOut>', self._update_color_hsv)
        s_s.bind('<FocusOut>', self._update_color_hsv)
        s_v.bind('<FocusOut>', self._update_color_hsv)
        s_h.bind('<Return>', self._update_color_hsv)
        s_s.bind('<Return>', self._update_color_hsv)
        s_v.bind('<Return>', self._update_color_hsv)
        self.html.bind("<FocusOut>", self._update_color_html)
        self.html.bind("<Return>", self._update_color_html)

        self.wait_visibility()
        self.lift()
        self.grab_set()

    def get_color(self):
        """Return selected color, return an empty string if no color is selected."""
        return self.color

    def _unfocus(self, event):
        """Unfocus palette items when click on bar or square."""
        w = self.focus_get()
        if w != self and 'spinbox' not in str(w) and 'entry' not in str(w):
            self.focus_set()

    @staticmethod
    def get_color_value(string_var):
        """
        Convert string_var content into an int between 0 and 255.

        Return the value of string_var interpreting it as an integer between
        0 and 255. If it is not the case, the value of the string_var is
        corrected (to 0 or 255 depending on the value) and the corrected
        result is returned.
        """
        try:
            r = int(string_var.get())
            if r > 255:
                string_var.set(255)
                return 255
            elif r < 0:
                string_var.set(0)
                return 0
            else:
                return r
        except ValueError:
            string_var.set(0)
            return 0

    @staticmethod
    def get_sv_value(string_var):
        """
        Convert string_var content into an int between 0 and 100.

        Return the value of string_var interpreting it as an integer between
        0 and 100. If it is not the case, the value of the string_var is
        corrected (to 0 or 100 depending on the value) and the corrected
        result is returned.
        """
        try:
            r = int(string_var.get())
            if r > 100:
                string_var.set(100)
                return 100
            elif r < 0:
                string_var.set(0)
                return 0
            else:
                return r
        except ValueError:
            string_var.set(0)
            return 0

    @staticmethod
    def get_hue_value(string_var):
        """
        Convert string_var content into an int between 0 and 360.

        Return the value of string_var interpreting it as an integer between
        0 and 360. If it is not the case, the value of the string_var is
        corrected (to 0 or 360 depending on the value) and the corrected
        result is returned.
        """
        try:
            r = int(string_var.get())
            if r > 360:
                string_var.set(360)
                return 360
            elif r < 0:
                string_var.set(0)
                return 0
            else:
                return r
        except ValueError:
            string_var.set(0)
            return 0

    def _palette_cmd(self, event):
        """Respond to user click on a palette item."""
        label = event.widget
        label.master.focus_set()
        label.master.configure(relief="sunken")
        r, g, b = self.winfo_rgb(label.cget("background"))
        r = round2(r * 255 / 65535)
        g = round2(g * 255 / 65535)
        b = round2(b * 255 / 65535)
        color = rgb_to_html(r, g, b)
        h, s, v = rgb_to_hsv(r, g, b)
        self.color_preview.configure(background=color)
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self.html.delete(0, "end")
        self.html.insert(0, color.upper())
        self.bar.set(h)
        self.square.set_hsv((h, s, v))

    def _change_sel_color(self, event):
        """Respond to motion of the color selection cross."""
        (r, g, b), (h, s, v), color = self.square.get()
        self.color_preview.configure(background=color)
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.saturation.set(s)
        self.value.set(v)
        self.html.delete(0, "end")
        self.html.insert(0, color.upper())

    def _change_color(self, event):
        """Respond to motion of the hsv cursor."""
        h = self.bar.get()
        self.square.set_hue(h)
        (r, g, b), (h, s, v), sel_color = self.square.get()
        self.color_preview.configure(background=sel_color)
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self.html.delete(0, "end")
        self.html.insert(0, sel_color.upper())

    def _update_color_html(self, event=None):
        """Update display after a change in the HTML entry."""
        color = self.html.get().upper()
        if re.match(r"^#[0-9A-F]{6}$", color):
            r, g, b = html_to_rgb(color)
            self.red.set(r)
            self.green.set(g)
            self.blue.set(b)
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)
            self.bar.set(h)
            self.square.set_hsv((h, s, v))
            self.color_preview.configure(background=color)
        else:
            self._update_color_rgb()

    def _update_color_hsv(self, event=None):
        """Update display after a change in the HSV spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            h = self.get_hue_value(self.hue)
            s = self.get_sv_value(self.saturation)
            v = self.get_sv_value(self.value)
            sel_color = hsv_to_rgb(h, s, v)
            self.red.set(sel_color[0])
            self.green.set(sel_color[1])
            self.blue.set(sel_color[2])
            html = rgb_to_html(*sel_color)
            self.html.delete(0, "end")
            self.html.insert(0, html)
            self.square.set_hsv((h, s, v))
            self.bar.set(h)
            self.color_preview.configure(background=html)

    def _update_color_rgb(self, event=None):
        """Update display after a change in the RGB spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            r = self.get_color_value(self.red)
            g = self.get_color_value(self.green)
            b = self.get_color_value(self.blue)
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)
            html = rgb_to_html(r, g, b)
            self.html.delete(0, "end")
            self.html.insert(0, html)
            self.square.set_hsv((h, s, v))
            self.bar.set(h)
            self.color_preview.configure(background=html)

    def ok(self):
        self.color = self.square.get()
        self.destroy()


def askcolor(color="red", parent=None, title=_("Color Chooser")):
    """
    Open a ColorPicker dialog and return the chosen color.

    The selected color is retunred in RGB and hexadecimal formats. An empty
    tuple is returned if selection is cancelled.

    Arguments:
        * color: initially selected color (RGB, html or tkinter color name)
        * parent: parent window
        * title: dialog title
    """
    col = ColorPicker(parent, color, title)
    col.wait_window(col)
    res = col.get_color()
    if res:
        return res[0], res[2]
    else:
        return (None, None)


if __name__ == "__main__":
    root = tk.Tk()
    s = Style(root)
    s.theme_use('clam')
    print(askcolor("sky blue", parent=root))
    root.mainloop()
