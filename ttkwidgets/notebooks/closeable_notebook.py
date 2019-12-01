import tkinter as tk
import tkinter.ttk as ttk


class CloseableNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        """
        CloseableNotebook generates a <<NotebookTabClosed>> when a tab is closed. 
        The event object has a tab keyword argument containing the tab id that was just closed.
        
        args and kwargs are the same as for a regular ttk::Notebook
        """
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CloseableNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)
        self._active = None
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>", tab=self._active)

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        try:
            style.element_create("close", "image", "img_close",
                                 ("active", "pressed", "!disabled", "img_closepressed"),
                                 ("active", "!disabled", "img_closeactive"), border=8, sticky='e')
        except tk.TclError:
            pass

        style.layout("CloseableNotebook", [("CloseableNotebook.client", {"sticky": "nswe"})])

        style.layout("CloseableNotebook.Tab", [
            ("CloseableNotebook.tab", {
                "sticky": "nswe",
                "expand": 1,
                "children": [
                    ("CloseableNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CloseableNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CloseableNotebook.label", {"side": "left", "sticky": 'w'}),
                                    ("CloseableNotebook.close", {"side": "left", "sticky": 'e'}),
                                ]})
                        ]})
                ]})])
