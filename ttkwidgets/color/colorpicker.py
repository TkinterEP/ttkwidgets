# -*- coding: utf-8 -*-
"""
Author: Juliette Monsel
License: GNU GPLv3
Source: https://github.com/j4321/tkColorPicker

Edited by RedFantom for Python 2/3 cross-compatibility and docstring formatting


tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Colorpicker dialog
"""


from PIL import ImageTk
from .functions import tk, ttk, round2, create_checkered_image, \
    overlay, PALETTE, hsv_to_rgb, hexa_to_rgb, rgb_to_hexa, col2hue, rgb_to_hsv
from .alphabar import AlphaBar
from .gradientbar import GradientBar
from .colorsquare import ColorSquare
from .spinbox import Spinbox
from .limitvar import LimitVar
from locale import getdefaultlocale
import re


# --- Translation
EN = {}
FR = {"Red": "Rouge", "Green": "Vert", "Blue": "Bleu",
      "Hue": "Teinte", "Saturation": "Saturation", "Value": "Valeur",
      "Cancel": "Annuler", "Color Chooser": "Sélecteur de couleur",
      "Alpha": "Alpha"}

try:
    if getdefaultlocale()[0][:2] == 'fr':
        TR = FR
    else:
        TR = EN
except ValueError:
    TR = EN


def _(text):
    """Translate text."""
    return TR.get(text, text)


class ColorPicker(tk.Toplevel):
    """Color picker dialog."""

    def __init__(self, parent=None, color=(255, 0, 0), alpha=False,
                 title=_("Color Chooser")):
        """
        Create a ColorPicker dialog.

        :param parent: parent widget
        :type parent: widget
        :param color: initially selected color (RGB(A), HEX or tkinter color name)
        :type color: sequence[int] or str
        :param alpha: whether to display the alpha channel
        :type alpha: bool
        :param title: dialog title
        :type title: str
        """
        tk.Toplevel.__init__(self, parent)

        self.title(title)
        self.transient(self.master)
        self.resizable(False, False)
        self.rowconfigure(1, weight=1)

        self.color = ""
        self.alpha_channel = bool(alpha)
        style = ttk.Style(self)
        style.map("palette.TFrame", relief=[('focus', 'sunken')],
                  bordercolor=[('focus', "#4D4D4D")])
        self.configure(background=style.lookup("TFrame", "background"))

        if isinstance(color, str):
            if re.match(r"^#[0-9A-F]{8}$", color.upper()):
                col = hexa_to_rgb(color)
                self._old_color = col[:3]
                if alpha:
                    self._old_alpha = col[3]
                    old_color = color
                else:
                    old_color = color[:7]
            elif re.match(r"^#[0-9A-F]{6}$", color.upper()):
                self._old_color = hexa_to_rgb(color)
                old_color = color
                if alpha:
                    self._old_alpha = 255
                    old_color += 'FF'
            else:
                col = self.winfo_rgb(color)
                self._old_color = tuple(round2(c * 255 / 65535) for c in col)
                args = self._old_color
                if alpha:
                    self._old_alpha = 255
                    args = self._old_color + (255,)
                old_color = rgb_to_hexa(*args)
        else:
            self._old_color = color[:3]
            if alpha:
                if len(color) < 4:
                    color += (255,)
                    self._old_alpha = 255
                else:
                    self._old_alpha = color[3]
            old_color = rgb_to_hexa(*color)

        # --- GradientBar
        hue = col2hue(*self._old_color)
        bar = ttk.Frame(self, borderwidth=2, relief='groove')
        self.bar = GradientBar(bar, hue=hue, width=200, highlightthickness=0)
        self.bar.pack()

        # --- ColorSquare
        square = ttk.Frame(self, borderwidth=2, relief='groove')
        self.square = ColorSquare(square, hue=hue, width=200, height=200,
                                  color=rgb_to_hsv(*self._old_color),
                                  highlightthickness=0)
        self.square.pack()

        frame = ttk.Frame(self)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

        # --- color preview: initial color and currently selected color side by side
        preview_frame = ttk.Frame(frame, relief="groove", borderwidth=2)
        preview_frame.grid(row=0, column=0, sticky="nw", pady=2)
        if alpha:
            self._transparent_bg = create_checkered_image(42, 32)
            transparent_bg_old = create_checkered_image(42, 32,
                                                        (100, 100, 100, 255),
                                                        (154, 154, 154, 255))
            prev_old = overlay(transparent_bg_old, hexa_to_rgb(old_color))
            prev = overlay(self._transparent_bg, hexa_to_rgb(old_color))
            self._im_old_color = ImageTk.PhotoImage(prev_old, master=self)
            self._im_color = ImageTk.PhotoImage(prev, master=self)
            old_color_prev = tk.Label(preview_frame, padx=0, pady=0,
                                      image=self._im_old_color,
                                      borderwidth=0, highlightthickness=0)
            self.color_preview = tk.Label(preview_frame, pady=0, padx=0,
                                          image=self._im_color,
                                          borderwidth=0, highlightthickness=0)
        else:
            old_color_prev = tk.Label(preview_frame, background=old_color[:7],
                                      width=5, highlightthickness=0, height=2,
                                      padx=0, pady=0)
            self.color_preview = tk.Label(preview_frame, width=5, height=2,
                                          pady=0, background=old_color[:7],
                                          padx=0, highlightthickness=0)
        old_color_prev.bind("<1>", self._reset_preview)
        old_color_prev.grid(row=0, column=0)
        self.color_preview.grid(row=0, column=1)

        # --- palette
        palette = ttk.Frame(frame)
        palette.grid(row=0, column=1, rowspan=2, sticky="ne")
        for i, col in enumerate(PALETTE):
            f = ttk.Frame(palette, borderwidth=1, relief="raised",
                          style="palette.TFrame")
            l = tk.Label(f, background=col, width=2, height=1)
            l.bind("<1>", self._palette_cmd)
            f.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            l.pack()
            f.grid(row=i % 2, column=i // 2, padx=2, pady=2)

        col_frame = ttk.Frame(self)
        # --- hsv
        hsv_frame = ttk.Frame(col_frame, relief="ridge", borderwidth=2)
        hsv_frame.pack(pady=(0, 4), fill="x")
        hsv_frame.columnconfigure(0, weight=1)
        self.hue = LimitVar(0, 360, self)
        self.saturation = LimitVar(0, 100, self)
        self.value = LimitVar(0, 100, self)

        s_h = Spinbox(hsv_frame, from_=0, to=360, width=4, name='spinbox',
                      textvariable=self.hue, command=self._update_color_hsv)
        s_s = Spinbox(hsv_frame, from_=0, to=100, width=4,
                      textvariable=self.saturation, name='spinbox',
                      command=self._update_color_hsv)
        s_v = Spinbox(hsv_frame, from_=0, to=100, width=4, name='spinbox',
                      textvariable=self.value, command=self._update_color_hsv)
        h, s, v = rgb_to_hsv(*self._old_color)
        s_h.delete(0, 'end')
        s_h.insert(0, h)
        s_s.delete(0, 'end')
        s_s.insert(0, s)
        s_v.delete(0, 'end')
        s_v.insert(0, v)
        s_h.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        s_s.grid(row=1, column=1, sticky='w', padx=4, pady=4)
        s_v.grid(row=2, column=1, sticky='w', padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Hue')).grid(row=0, column=0, sticky='e',
                                                 padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Saturation')).grid(row=1, column=0, sticky='e',
                                                        padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Value')).grid(row=2, column=0, sticky='e',
                                                   padx=4, pady=4)

        # --- rgb
        rgb_frame = ttk.Frame(col_frame, relief="ridge", borderwidth=2)
        rgb_frame.pack(pady=4, fill="x")
        rgb_frame.columnconfigure(0, weight=1)
        self.red = LimitVar(0, 255, self)
        self.green = LimitVar(0, 255, self)
        self.blue = LimitVar(0, 255, self)

        s_red = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                        textvariable=self.red, command=self._update_color_rgb)
        s_green = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                          textvariable=self.green, command=self._update_color_rgb)
        s_blue = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                         textvariable=self.blue, command=self._update_color_rgb)
        s_red.delete(0, 'end')
        s_red.insert(0, self._old_color[0])
        s_green.delete(0, 'end')
        s_green.insert(0, self._old_color[1])
        s_blue.delete(0, 'end')
        s_blue.insert(0, self._old_color[2])
        s_red.grid(row=0, column=1, sticky='e', padx=4, pady=4)
        s_green.grid(row=1, column=1, sticky='e', padx=4, pady=4)
        s_blue.grid(row=2, column=1, sticky='e', padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Red')).grid(row=0, column=0, sticky='e',
                                                 padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Green')).grid(row=1, column=0, sticky='e',
                                                   padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Blue')).grid(row=2, column=0, sticky='e',
                                                  padx=4, pady=4)
        # --- hexa
        hexa_frame = ttk.Frame(col_frame)
        hexa_frame.pack(fill="x")
        self.hexa = ttk.Entry(hexa_frame, justify="center", width=10, name='entry')
        self.hexa.insert(0, old_color.upper())
        ttk.Label(hexa_frame, text="HTML").pack(side="left", padx=4, pady=(4, 1))
        self.hexa.pack(side="left", padx=6, pady=(4, 1), fill='x', expand=True)

        # --- alpha
        if alpha:
            alpha_frame = ttk.Frame(self)
            alpha_frame.columnconfigure(1, weight=1)
            self.alpha = LimitVar(0, 255, self)
            alphabar = ttk.Frame(alpha_frame, borderwidth=2, relief='groove')
            self.alphabar = AlphaBar(alphabar, alpha=self._old_alpha, width=200,
                                     color=self._old_color, highlightthickness=0)
            self.alphabar.pack()
            s_alpha = Spinbox(alpha_frame, from_=0, to=255, width=4,
                              textvariable=self.alpha, command=self._update_alpha)
            s_alpha.delete(0, 'end')
            s_alpha.insert(0, self._old_alpha)
            alphabar.grid(row=0, column=0, padx=(0, 4), pady=4, sticky='w')
            ttk.Label(alpha_frame, text=_('Alpha')).grid(row=0, column=1, sticky='e',
                                                         padx=4, pady=4)
            s_alpha.grid(row=0, column=2, sticky='w', padx=(4, 6), pady=4)

        # --- validation
        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="Ok",
                   command=self.ok).pack(side="right", padx=10)
        ttk.Button(button_frame, text=_("Cancel"),
                   command=self.destroy).pack(side="right", padx=10)

        # --- placement
        bar.grid(row=0, column=0, padx=10, pady=(10, 4), sticky='n')
        square.grid(row=1, column=0, padx=10, pady=(9, 0), sticky='n')
        if alpha:
            alpha_frame.grid(row=2, column=0, columnspan=2, padx=10,
                             pady=(1, 4), sticky='ewn')
        col_frame.grid(row=0, rowspan=2, column=1, padx=(4, 10), pady=(10, 4))
        frame.grid(row=3, column=0, columnspan=2, pady=(4, 10), padx=10, sticky="new")
        button_frame.grid(row=4, columnspan=2, pady=(0, 10), padx=10)

        # --- bindings
        self.bar.bind("<ButtonRelease-1>", self._change_color, True)
        self.bar.bind("<Button-1>", self._unfocus, True)
        if alpha:
            self.alphabar.bind("<ButtonRelease-1>", self._change_alpha, True)
            self.alphabar.bind("<Button-1>", self._unfocus, True)
        self.square.bind("<Button-1>", self._unfocus, True)
        self.square.bind("<ButtonRelease-1>", self._change_sel_color, True)
        self.square.bind("<B1-Motion>", self._change_sel_color, True)
        s_red.bind('<FocusOut>', self._update_color_rgb)
        s_green.bind('<FocusOut>', self._update_color_rgb)
        s_blue.bind('<FocusOut>', self._update_color_rgb)
        s_red.bind('<Return>', self._update_color_rgb)
        s_green.bind('<Return>', self._update_color_rgb)
        s_blue.bind('<Return>', self._update_color_rgb)
        s_red.bind('<Control-a>', self._select_all_spinbox)
        s_green.bind('<Control-a>', self._select_all_spinbox)
        s_blue.bind('<Control-a>', self._select_all_spinbox)
        s_h.bind('<FocusOut>', self._update_color_hsv)
        s_s.bind('<FocusOut>', self._update_color_hsv)
        s_v.bind('<FocusOut>', self._update_color_hsv)
        s_h.bind('<Return>', self._update_color_hsv)
        s_s.bind('<Return>', self._update_color_hsv)
        s_v.bind('<Return>', self._update_color_hsv)
        s_h.bind('<Control-a>', self._select_all_spinbox)
        s_s.bind('<Control-a>', self._select_all_spinbox)
        s_v.bind('<Control-a>', self._select_all_spinbox)
        if alpha:
            s_alpha.bind('<Return>', self._update_alpha)
            s_alpha.bind('<FocusOut>', self._update_alpha)
            s_alpha.bind('<Control-a>', self._select_all_spinbox)
        self.hexa.bind("<FocusOut>", self._update_color_hexa)
        self.hexa.bind("<Return>", self._update_color_hexa)
        self.hexa.bind("<Control-a>", self._select_all_entry)

        self.hexa.focus_set()
        self.wait_visibility()
        self.lift()
        self.grab_set()

    def get_color(self):
        """
        Return selected color, return an empty string if no color is selected.

        :return: selected color as a (RGB, HSV, HEX) tuple or ""
        """
        return self.color

    @staticmethod
    def _select_all_spinbox(event):
        """Select all entry content."""
        event.widget.selection('range', 0, 'end')
        return "break"

    @staticmethod
    def _select_all_entry(event):
        """Select all entry content."""
        event.widget.selection_range(0, 'end')
        return "break"

    def _unfocus(self, event):
        """Unfocus palette items when click on bar or square."""
        w = self.focus_get()
        if w != self and 'spinbox' not in str(w) and 'entry' not in str(w):
            self.focus_set()

    def _update_preview(self):
        """Update color preview."""
        color = self.hexa.get()
        if self.alpha_channel:
            prev = overlay(self._transparent_bg, hexa_to_rgb(color))
            self._im_color = ImageTk.PhotoImage(prev, master=self)
            self.color_preview.configure(image=self._im_color)
        else:
            self.color_preview.configure(background=color)

    def _reset_preview(self, event):
        """Respond to user click on a palette item."""
        label = event.widget
        label.master.focus_set()
        label.master.configure(relief="sunken")
        args = self._old_color
        if self.alpha_channel:
            args += (self._old_alpha,)
            self.alpha.set(self._old_alpha)
            self.alphabar.set_color(args)
        color = rgb_to_hexa(*args)
        h, s, v = rgb_to_hsv(*self._old_color)
        self.red.set(self._old_color[0])
        self.green.set(self._old_color[1])
        self.blue.set(self._old_color[2])
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self.hexa.delete(0, "end")
        self.hexa.insert(0, color.upper())
        self.bar.set(h)
        self.square.set_hsv((h, s, v))
        self._update_preview()

    def _palette_cmd(self, event):
        """Respond to user click on a palette item."""
        label = event.widget
        label.master.focus_set()
        label.master.configure(relief="sunken")
        r, g, b = self.winfo_rgb(label.cget("background"))
        r = round2(r * 255 / 65535)
        g = round2(g * 255 / 65535)
        b = round2(b * 255 / 65535)
        args = (r, g, b)
        if self.alpha_channel:
            a = self.alpha.get()
            args += (a,)
            self.alphabar.set_color(args)
        color = rgb_to_hexa(*args)
        h, s, v = rgb_to_hsv(r, g, b)
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self.hexa.delete(0, "end")
        self.hexa.insert(0, color.upper())
        self.bar.set(h)
        self.square.set_hsv((h, s, v))
        self._update_preview()

    def _change_sel_color(self, event):
        """Respond to motion of the color selection cross."""
        (r, g, b), (h, s, v), color = self.square.get()
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.saturation.set(s)
        self.value.set(v)
        self.hexa.delete(0, "end")
        self.hexa.insert(0, color.upper())
        if self.alpha_channel:
            self.alphabar.set_color((r, g, b))
            self.hexa.insert('end',
                             ("%2.2x" % self.alpha.get()).upper())
        self._update_preview()

    def _change_color(self, event):
        """Respond to motion of the hsv cursor."""
        h = self.bar.get()
        self.square.set_hue(h)
        (r, g, b), (h, s, v), sel_color = self.square.get()
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self.hexa.delete(0, "end")
        self.hexa.insert(0, sel_color.upper())
        if self.alpha_channel:
            self.alphabar.set_color((r, g, b))
            self.hexa.insert('end',
                             ("%2.2x" % self.alpha.get()).upper())
        self._update_preview()

    def _change_alpha(self, event):
        """Respond to motion of the alpha cursor."""
        a = self.alphabar.get()
        self.alpha.set(a)
        hexa = self.hexa.get()
        hexa = hexa[:7] + ("%2.2x" % a).upper()
        self.hexa.delete(0, 'end')
        self.hexa.insert(0, hexa)
        self._update_preview()

    def _update_color_hexa(self, event=None):
        """Update display after a change in the HEX entry."""
        color = self.hexa.get().upper()
        self.hexa.delete(0, 'end')
        self.hexa.insert(0, color)
        if re.match(r"^#[0-9A-F]{6}$", color):
            r, g, b = hexa_to_rgb(color)
            self.red.set(r)
            self.green.set(g)
            self.blue.set(b)
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)
            self.bar.set(h)
            self.square.set_hsv((h, s, v))
            if self.alpha_channel:
                a = self.alpha.get()
                self.hexa.insert('end', ("%2.2x" % a).upper())
                self.alphabar.set_color((r, g, b, a))
        elif self.alpha_channel and re.match(r"^#[0-9A-F]{8}$", color):
            r, g, b, a = hexa_to_rgb(color)
            self.red.set(r)
            self.green.set(g)
            self.blue.set(b)
            self.alpha.set(a)
            self.alphabar.set_color((r, g, b, a))
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)
            self.bar.set(h)
            self.square.set_hsv((h, s, v))
        else:
            self._update_color_rgb()
        self._update_preview()

    def _update_alpha(self, event=None):
        """Update display after a change in the alpha spinbox."""
        a = self.alpha.get()
        hexa = self.hexa.get()
        hexa = hexa[:7] + ("%2.2x" % a).upper()
        self.hexa.delete(0, 'end')
        self.hexa.insert(0, hexa)
        self.alphabar.set(a)
        self._update_preview()

    def _update_color_hsv(self, event=None):
        """Update display after a change in the HSV spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            h = self.hue.get()
            s = self.saturation.get()
            v = self.value.get()
            sel_color = hsv_to_rgb(h, s, v)
            self.red.set(sel_color[0])
            self.green.set(sel_color[1])
            self.blue.set(sel_color[2])
            if self.alpha_channel:
                sel_color += (self.alpha.get(),)
                self.alphabar.set_color(sel_color)
            hexa = rgb_to_hexa(*sel_color)
            self.hexa.delete(0, "end")
            self.hexa.insert(0, hexa)
            self.square.set_hsv((h, s, v))
            self.bar.set(h)
            self._update_preview()

    def _update_color_rgb(self, event=None):
        """Update display after a change in the RGB spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            r = self.red.get()
            g = self.green.get()
            b = self.blue.get()
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)
            args = (r, g, b)
            if self.alpha_channel:
                args += (self.alpha.get(),)
                self.alphabar.set_color(args)
            hexa = rgb_to_hexa(*args)
            self.hexa.delete(0, "end")
            self.hexa.insert(0, hexa)
            self.square.set_hsv((h, s, v))
            self.bar.set(h)
            self._update_preview()

    def ok(self):
        """Validate color selection and destroy dialog."""
        rgb, hsv, hexa = self.square.get()
        if self.alpha_channel:
            hexa = self.hexa.get()
            rgb += (self.alpha.get(),)
        self.color = rgb, hsv, hexa
        self.destroy()


def askcolor(color="red", parent=None, title=_("Color Chooser"), alpha=False):
    """
    Open a ColorPicker dialog and return the chosen color.

    :return: the selected color in RGB(A) and hexadecimal #RRGGBB(AA) formats.
             (None, None) is returned if the color selection is cancelled.

    :param color: initially selected color (RGB(A), HEX or tkinter color name)
    :type color: sequence[int] or str
    :param parent: parent widget
    :type parent: widget
    :param title: dialog title
    :type title: str
    :param alpha: whether to display the alpha channel
    :type alpha: bool
    """
    col = ColorPicker(parent, color, alpha, title)
    col.wait_window(col)
    res = col.get_color()
    if res:
        return res[0], res[2]
    else:
        return None, None
