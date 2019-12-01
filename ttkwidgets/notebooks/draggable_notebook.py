import tkinter as tk
import tkinter.ttk as ttk
import _tkinter


class DraggableNotebook(ttk.Notebook):
    """
    DraggableNotebook class.
    
    Allows the user to drag tabs around to reorder them. Subclass of the ttk::Notebook widget.
    
    Code partly translated from this Tcl/Tk snippet :
    https://wiki.tcl-lang.org/page/Drag+and+Drop+Notebook+Tabs
    
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._src_index = None
        self._toplevels = []
        self._children = []

        self.bind("<ButtonPress-1>", self._on_mouse_button_1_pressed)
        self.bind("<ButtonRelease-1>", self._on_mouse_button_1_released)
        self.bind("<B1-Motion>", self._on_mouse_button_1_motion)
        # self.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed)

    def _on_mouse_button_1_pressed(self, event=None):
        self._src_index = self.index(f'@{event.x},{event.y}')

    def _on_mouse_button_1_released(self, event=None):
        dst_index = None
        if isinstance(self._src_index, int):
            try:
                dst_index = self.index(f'@{event.x},{event.y}')
            except _tkinter.TclError:
                dst_index = None
            if isinstance(dst_index, int):
                tab = self.tabs()[self._src_index]
                self.insert(dst_index, tab)
    
    def _on_mouse_button_1_motion(self, event=None):
        # TODO: Pass down the event through the event queue to subwidgets
        # https://wiki.tcl-lang.org/page/Drag+and+Drop+Notebook+Tabs
        # https://wiki.tcl-lang.org/page/ttk::notebook
        # https://github.com/RedFantom/ttkwidgets/blob/master/ttkwidgets/table.py
        pass

    def _on_notebook_tab_changed(self, event=None):
        if self._mouse_button_1_pressed:
            self.insert(f"@{event.x},{event.y}", self.identify(*self._mouse_button_1_pressed))
    
    def _create_toplevel(self, child, tabkw):
        # TODO: Allow dragging the tabs to a new tkinter.Toplevel. Use new move_widget function
        
        tl = tk.Toplevel(self)
        nb = DraggableNotebook(tl)
        child.master = nb
        nb.add(child, **tabkw)
        nb.pack()
        self._toplevels.append(tl)
    
    def add(self, child, **kw):
        rv = super().add(child, **kw)
        self._children.append(child)
        return rv
