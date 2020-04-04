"""
Author: Muhammet Emin TURGUT
License: GNU GPLv3
Source: https://github.com/muhammeteminturgut/ttkScrollableNotebook
"""
from tkinter import *
from tkinter import ttk

class ScrollableTabNotebook(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self.xLocation = 0
        self.notebookContent = ttk.Notebook(self,**kwargs)
        self.notebookContent.pack(fill="both", expand=True)

        self.notebookTab = ttk.Notebook(self,**kwargs)
        self.notebookTab.bind("<<NotebookTabChanged>>",self._tabChanger)

        slideFrame = ttk.Frame(self)
        slideFrame.place(relx=1.0, x=0, y=1, anchor=NE)
        leftArrow = ttk.Label(slideFrame, text="\u25c0")
        leftArrow.bind("<1>",self._leftSlide)
        leftArrow.pack(side=LEFT)
        rightArrow = ttk.Label(slideFrame, text=" \u25b6")
        rightArrow.bind("<1>",self._rightSlide)
        rightArrow.pack(side=RIGHT)
        self.notebookContent.bind( "<Configure>", self._resetSlide)

    def _tabChanger(self,event):
        self.notebookContent.select(self.notebookTab.index("current"))
        
    def _rightSlide(self,event):
        if self.notebookTab.winfo_width()>self.notebookContent.winfo_width()-30:
            if (self.notebookContent.winfo_width()-(self.notebookTab.winfo_width()+self.notebookTab.winfo_x()))<=35:
                self.xLocation-=20
                self.notebookTab.place(x=self.xLocation,y=0)
    def _leftSlide(self,event):
        if not self.notebookTab.winfo_x()== 0:
            self.xLocation+=20
            self.notebookTab.place(x=self.xLocation,y=0)

    def _resetSlide(self,event):
        self.notebookTab.place(x=0,y=0)
        self.xLocation = 0

    def add(self,frame,**kwargs):
        if len(self.notebookTab.winfo_children())!=0:
            self.notebookContent.add(frame, text="",state="hidden")
        else:
            self.notebookContent.add(frame, text="")
        self.notebookTab.add(ttk.Frame(self.notebookTab),**kwargs)

    def forget(self,tab_id):
        self.notebookContent.forget(tab_id)
        self.notebookTab.forget(tab_id)

    def hide(self,tab_id):
        self.notebookContent.hide(tab_id)
        self.notebookTab.hide(tab_id)

    def identify(self,x, y):
        return self.notebookTab.identify(x,y)

    def index(self,tab_id):
        return self.notebookTab.index(tab_id)

    def insert(self,pos,frame, **kwargs):
        self.notebookContent.insert(pos,frame, **kwargs)
        self.notebookTab.insert(pos,frame,**kwargs)

    def select(self,tab_id):
        self.notebookContent.select(tab_id)
        self.notebookTab.select(tab_id)

    def tab(self,tab_id, option=None, **kwargs):
        return self.notebookTab.tab(tab_id, option=None, **kwargs)

    def tabs(self):
        return self.notebookContent.tabs()

    def enable_traversal(self):
        self.notebookContent.enable_traversal()
        self.notebookTab.enable_traversal()
