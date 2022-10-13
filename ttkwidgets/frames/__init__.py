# Copyright (c) The ttkwidgets authors 2017
# Available under the license found in LICENSE
from .scrolledframe import ScrolledFrame
from .toggledframe import ToggledFrame
from .tooltip import Tooltip


def Balloon(*args, **kwargs):
    from warnings import warn
    warn("'Balloon' has been renamed to 'Tooltip'", DeprecationWarning, stacklevel=2)
    return Tooltip(*args, **kwargs)
