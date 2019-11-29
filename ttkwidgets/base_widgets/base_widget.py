import tkinter.ttk as ttk
from .tooltip import Tooltip


class Widget(ttk.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tooltip = kwargs.pop("tooltip", None)
        if tooltip is not None:
            if isinstance(tooltip, str):
                tooltip = (tooltip, )
            balloon_kw = {k: v for k, v in zip(["text", "background", "width", "max_width"], tooltip)}
            self.__balloon = Balloon(self, **balloon_kw)
    
    def bind(self, *args, **kwargs):
        add = None
        if len(args) == 3:
            add = args[-1]
        add = kwargs.pop("add", None) or add
        if add is None:
            add = "+"
        super().bind(*args, add=add, **kwargs)
