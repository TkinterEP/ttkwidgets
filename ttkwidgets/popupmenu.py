import tkinter as tk
import _tkinter


class PopupMenu(tk.Menu):
    """
    A :class:`tkinter.Menu` that binds <Button-3> to display it.
    
    Arguments are the same as for a regular tkinter Menu
    """
    def __init__(self, *args, **kwargs):
        """
        :param activebackground: Default value is ‘SystemHighlight’. (the database name is activeBackground, the class is Foreground)
        :param activeborderwidth: Default value is 0. (activeBorderWidth/BorderWidth)
        :param activeforeground: Default value is ‘SystemHighlightText’. (activeForeground/Background)
        :param background: Default value is ‘SystemMenu’. (background/Background)
        :param bg: Same as background.
        :param borderwidth: Default value is 0. (borderWidth/BorderWidth)
        :param bd: Same as borderwidth.
        :param cursor: Default value is ‘arrow’. (cursor/Cursor)
        :param callbacks: list (default: []) list of python callables to call when
                          callbacks will be passed the event object from the display_contextual
                          callback (bound to <Button-3>)
        :param disabledforeground: Default value is ‘SystemDisabledText’. (disabledForeground/DisabledForeground)
        :param font: Default value is ‘MS Sans Serif 8’. (font/Font)
        :param foreground: Default value is ‘SystemMenuText’. (foreground/Foreground)
        :param fg: Same as foreground.
        :param postcommand: No default value. (postCommand/Command)
        :param relief: Default value is ‘flat’. (relief/Relief)
        :param selectcolor: Default value is ‘SystemMenuText’. (selectColor/Background)
        :param takefocus: Default value is 0. (takeFocus/TakeFocus)
        :param tearoffcommand: No default value. (tearOffCommand/TearOffCommand)
        :param title: No default value. (title/Title)
        :param type: Default value is ‘normal’. (type/Type)
        """
        kwargs["tearoff"] = 0
        self.callbacks = kwargs.pop("callbacks", [])
        super().__init__(*args, **kwargs)
        self.master.bind('<Button-3>', self.display_contextual)


    def display_contextual(self, event):
        for callback in self.callbacks:
            callback(event)
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        except _tkinter.TclError:
            pass
        finally:
            self.grab_release()
