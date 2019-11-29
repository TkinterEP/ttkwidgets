from _tkinter import TclError


class TtkWidgetsError(TclError):
    pass


class I18NError(TtkWidgetsError):
    pass


class AssetNotFoundError(TtkWidgetsError):
    pass

class AssetMaskNotFoundError(TtkWidgetsError):
    pass
