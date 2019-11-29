import tkinter as tk
import tkinter.ttk as ttk
from copy import copy


class KeybindingEntry(ttk.Entry):
    """ An Entry subclass that allows the user to enter a key binding"""
    def __init__(self, master=None, current=None, **kwargs):
        """
        KeybindingEntry allows the user to set keyboard shortcuts by pressing the required keys.
        
        Generates a virtual <<KeybindingValidated>> event if the keybinding is successfully validated.
        See KeybindingEntry.validate_keybinding() documentation for the validation process.
        
        :param master: The master widget
        :param current: A list of keysyms for the current keybinding. If None, the list is empty.
        :param **kwargs: a dict of params passed on to the underlying entry widget
        """
        super().__init__(master, **kwargs)

        if current is None:
            current = []
        self.keys_pressed = copy(current)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<KeyPress>", self._on_key_pressed)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<KeyRelease>", self._on_key_release)
        self.update()

    def _on_focus_in(self, event):
        self.clear()

    def _on_key_pressed(self, event):
        keysym = self.format_keysym(event.keysym)
        if keysym not in self.keys_pressed:
            self.keys_pressed.append(keysym)
            self.update()
        return 'break'
    
    def _on_focus_out(self, event):
        if not self.validate_keybinding():
            self.clear()
            return
        self.event_generate("<<KeybindingValidated>>", when="tail")

    def _on_key_release(self, event):
        if not self.validate_keybinding():
            self.clear()
            return
        self.event_generate("<<KeybindingValidated>>", when="tail")
    
    def validate_keybinding(self):
        """
        Method validate_keybinding of KeybindingEntry.
        Validates the current keybinding set up by the user.
        Valid keybindings are keybindings that include at most 0-2 modifiers and
        exactly 1 detail, as per the tkinter documentation on events.
        
        :returns: whether the current keybinding is valid or not
        :rtype: bool
        """
        if len(self.modifiers) > 2:
            return False
        if len(self.details) != 1:
            return False
        return True

    @staticmethod
    def is_modifier(keysym):
        """
        Returns whether keysym is a modifier or not
        
        :param keysym: the key symbol to test
        :type keysym: str
        
        :returns: whether the keysym is a modifier or not
        :rtype: bool
        """
        return keysym in ("Shift", "Control", "Alt")

    @staticmethod
    def format_keysym(keysym):
        keysym = keysym.capitalize()
        keysym = keysym.split("_")[0]
        return keysym

    @property
    def modifiers(self):
        """
        property that returns the modifiers for the current keybinding
        
        :returns: list of keysyms that are modifiers
        :rtype: list
        """
        return [mod for mod in self.keys_pressed if self.is_modifier(mod)]

    @property
    def details(self):
        """
        property that returns the details for the current keybinding
        
        :returns: list of keysyms that are details
        :rtype: list
        """
        return [mod for mod in self.keys_pressed if not self.is_modifier(mod)]

    @property
    def event_format(self):
        """
        Format the currently set keybinding to be used by tkinter.Widget's bind method
        
        :returns: properly formatted keybinding for tkinter's bind method
        :rtype: str
        """
        rv = '<'
        if self.modifiers:
            rv += "-".join(self.modifiers) + "-"
        rv += self.details[0]
        rv += '>'
        return rv

    def update(self):
        """
        Update the text on the entry to show the currently set keybinding
        """
        self.delete(0, tk.END)
        self.insert(tk.END, "+".join(self.keys_pressed))

    def clear(self):
        """
        Clears the currently set keybinding
        """
        self.keys_pressed = []
        self.update()
