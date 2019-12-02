import tkinter as tk
import tkinter.ttk as ttk


class _Debounce:
    """
    When holding a key down, multiple key press and key release events are fired in
    succession. Debouncing is implemented in order to squash these repeated events
    and know when the "real" KeyRelease and KeyPress events happen.
    Use by subclassing a tkinter widget along with this class:
        class DebounceTk(Debounce, tk.Tk):
            pass
    """

    # use classname as key to store class bindings
    # as single dict for all instances
    _bind_class_dict = {}

    # 'all' bindings stored here
    # single dict for all instances
    _bind_all_dict = {}

    def bind(self, event, function, debounce=True):
        """
        Override the bind method, acts as normal binding if not KeyPress or KeyRelease
        type events, optional debounce parameter can be set to false to force normal behavior
        """
        self._debounce_init()
        self._debounce_bind(event, function, debounce,
                            self._binding_dict, self._base.bind)

    def bind_all(self, event, function, debounce=True):
        """
        Override the bind_all method, acts as normal binding if not KeyPress or KeyRelease
        type events, optional debounce parameter can be set to false to force normal behavior
        """
        self._debounce_init()
        self._debounce_bind(event, function, debounce,
                            self._bind_all_dict, self._base.bind_all)

    def bind_class(self, event, function, debounce=True):
        """
        Override the bind_class method, acts as normal binding if not KeyPress or KeyRelease
        type events, optional debounce parameter can be set to false to force normal behavior
        unlike underlying tk bind_class this uses name of class on which its called
        instead of requireing clas name as a parameter
        """
        self._debounce_init()
        self._debounce_bind(event, function, debounce,
                            self._bind_class_dict[self.__class__.__name__],
                            self._base.bind_class, self.__class__.__name__)

    def _debounce_bind(self, event, function, debounce, bind_dict, bind_method, *args):
        """
        internal method to implement binding
        """
        self._debounce_init()
        # remove special symbols and split at first hyphen if present
        ev = event.replace("<", "").replace(">", "").split('-', 1)
        # if debounce and a supported event
        if (('KeyPress' in ev) or ('KeyRelease' in ev)) and debounce:
            if len(ev) == 2:  # not generic binding so use keynames as key
                evname = ev[1]
            else:  # generic binding, use event type
                evname = ev[0]
            if evname in bind_dict: # if have prev binding use that dict
                d = bind_dict[evname]
            else:  # no previous binding, create new default dict
                d = {'has_prev_key_release': None, 'has_prev_key_press': False}

            # add function to dict (as keypress or release depending on name)
            d[ev[0]] = function
            # save binding back into dict
            bind_dict[evname] = d
            # call base class binding
            if ev[0] == 'KeyPress':
                bind_method(self, *args, sequence=event, func=self._on_key_press_repeat)
            elif ev[0] == 'KeyRelease':
                bind_method(self, *args, sequence=event, func=self._on_key_release_repeat)

        else:  # not supported or not debounce, bind as normal
            bind_method(self, *args, sequence=event, func=function)

    def _debounce_init(self):
        # get first base class that isn't Debounce and save ref
        # this will be used for underlying bind methods
        if not hasattr(self, '_base'):
            for base in self.__class__.__bases__:
                if base.__name__ != 'Debounce':
                    self._base = base
                    break
        # for instance bindings
        if not hasattr(self, '_binding_dict'):
            self._binding_dict = {}

        # for class bindings
        try:  # check if this class has alread had class bindings
            self._bind_class_dict[self.__class__.__name__]
        except KeyError:  # create dict to store if not
            self._bind_class_dict[self.__class__.__name__] = {}

        # get the current bind tags
        bindtags = list(self.bindtags())
        # add our custom bind tag before the origional bind tag
        index = bindtags.index(self._base.__name__)
        bindtags.insert(index, self.__class__.__name__)
        # save the bind tags back to the widget
        self.bindtags(tuple(bindtags))

    def _get_evdict(self, event):
        """
        internal method used to get the dictionaries that store the special binding info
        """
        dicts = []
        names = {'2': 'KeyPress', '3': 'KeyRelease'}
        # loop through all applicable bindings
        for d in [self._binding_dict,  # instance binding
                  self._bind_class_dict[self.__class__.__name__],  # class
                  self._bind_all_dict]:  # all
            evdict = None
            generic = False
            if event.type in names:  # if supported event
                evname = event.keysym
                if evname not in d:  # if no specific binding
                    generic = True
                    evname = names[event.type]
                try:
                    evdict = d[evname]
                except KeyError:
                    pass
            if evdict:  # found a binding
                dicts.append((d, evdict, generic))
        return dicts

    def _on_key_release(self, event):
        """
        internal method, called by _on_key_release_repeat only when key is actually released
        this then calls the method that was passed in to the bind method
        """
        # get all binding details
        for d, evdict, generic in self._get_evdict(event):
            # call callback
            res = evdict['KeyRelease'](event)
            evdict['has_prev_key_release'] = None

            # record that key was released
            if generic:
                d['KeyPress'][event.keysym] = False
            else:
                evdict['has_prev_key_press'] = False
            # if supposed to break propagate this up
            if res == 'break':
                return 'break'

    def _on_key_release_repeat(self, event):
        """
        internal method, called by the 'KeyRelease' event, used to filter false events
        """
        # get all binding details
        for d, evdict, generic in self._get_evdict(event):
            if evdict["has_prev_key_release"]:
                # got a previous release so cancel it
                self.after_cancel(evdict["has_prev_key_release"])
                evdict["has_prev_key_release"] = None
            # queue new event for key release
            evdict["has_prev_key_release"] = self.after_idle(self._on_key_release, event)

    def _on_key_press(self, event):
        """
        internal method, called by _on_key_press_repeat only when key is actually pressed
        this then calls the method that was passed in to the bind method
        """
        # get all binding details
        for d, evdict, generic in self._get_evdict(event):
            # call callback
            res = evdict['KeyPress'](event)
            # record that key was pressed
            if generic:
                evdict[event.keysym] = True
            else:
                evdict['has_prev_key_press'] = True
            # if supposed to break propagate this up
            if res == 'break':
                return 'break'

    def _on_key_press_repeat(self, event):
        """
        internal method, called by the 'KeyPress' event, used to filter false events
        """
        # get binding details
        for _, evdict, generic in self._get_evdict(event):
            if not generic:
                if evdict["has_prev_key_release"]:
                    # got a previous release so cancel it
                    self.after_cancel(evdict["has_prev_key_release"])
                    evdict["has_prev_key_release"] = None
                else:
                    # if not pressed before (real event)
                    if not evdict['has_prev_key_press']:
                        self._on_key_press(event)
            else:
                # if not pressed before (real event)
                if (event.keysym not in evdict) or (not evdict[event.keysym]):
                    self._on_key_press(event)


class DebouncedTk(_Debounce, tk.Tk):
    pass


class DebouncedToplevel(_Debounce, tk.Toplevel):
    pass


class DebouncedFrame(_Debounce, ttk.Frame):
    pass
