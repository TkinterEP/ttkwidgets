import tkinter.ttk as ttk
import os
import mimetypes
from ttkwidgets.utilities import auto_scroll, get_bitmap


class DirTree(ttk.Frame):
    """ A widget that shows a directory tree """
    def __init__(self, master=None, path=None, height=10, callbacks=None):
        """
        Constructor of the DirTree widget.

        :param master: parent widget to this widget. None by default.
        :param path: str or pathlib.Path object representing the directory to view.
        :param height: height of the widget, in number of items to show.
        :param callbacks: dictionnary of callbacks. Callbacks should be callable, and take a "path"
                          argument, which is the full path of the file being double-clicked.
                          The keys of the dictionnary should correspond to the first part of a mimetype,
                          i.e. "audio" in "audio/ogg".
        """
        super(DirTree, self).__init__(master)
        self.path = path
        self._name = ""
        self.height = 20 * height
        self.callbacks = {} if callbacks is None else callbacks
        self.init_treeview()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, ppath):
        self._path = ppath
        dir_ = os.path.abspath(self._path).replace('\\', '/')
        self._name = dir_.split("/")[-1]

    def init_treeview(self):
        self.vsb = ttk.Scrollbar(master=self, orient="vertical")
        self.hsb = ttk.Scrollbar(master=self, orient="horizontal")
        style = ttk.Style()
        style.configure("Custom.Treeview")
        style.configure("Custom.Treeview.Heading",
                        relief='flat')
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])
        self.tree = ttk.Treeview(self,
                                 columns=("fullpath", "type", "size"),
                                 displaycolumns=(),
                                 height=self.height // 20,
                                 selectmode="browse",
                                 yscrollcommand=lambda f, l: auto_scroll(self.vsb, f, l),
                                 xscrollcommand=lambda f, l: auto_scroll(self.hsb, f, l),
                                 style='Custom.Treeview',
                                 )

        self.tree.heading("#0", text="Directory Structure", anchor='w')
        self.tree.heading("size", text="File Size", anchor='w')
        self.tree.column("size", stretch=0, width=100)

        self.vsb['command'] = self.tree.yview
        self.hsb['command'] = self.tree.xview

        self.tree.grid(row=0, column=0)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ns")
        self.tree.bind('<<TreeviewOpen>>', self.update_tree)
        self.tree.bind('<Double-Button-1>', self.on_double_click)
        self.images = []

    def populate_tree(self, node=""):
        if self.tree.set(node, "type") != 'directory':
            return

        path = self.tree.set(node, "fullpath")
        self.tree.delete(*self.tree.get_children(node))

        special_dirs = []

        for p in special_dirs + os.listdir(path):
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p):
                ptype = "directory"
            elif os.path.isfile(p):
                ptype = "file"

            fname = os.path.split(p)[1]
            id_ = self.tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    self.images.append(get_bitmap("folder"))
                    self.tree.insert(id_, 0, text="dummy")
                    self.tree.item(id_, text=fname,
                                   image=self.images[-1],
                                   tags=("base",))
            elif ptype == 'file':
                mimetype = mimetypes.guess_type(fname)[0].split("/")[0]
                if mimetype == "image":
                    img = get_bitmap("image")
                elif mimetype == "video":
                    img = get_bitmap("video")
                elif mimetype == "audio":
                    img = get_bitmap("audio")
                else:
                    img = get_bitmap("text")
                self.images.append(img)
                self.tree.item(id_, image=self.images[-1])

    def sort_tree(self, node, col="type", reverse=False):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children(node)]
        items.sort(reverse=reverse)
        for index, (_, k) in enumerate(items):
            self.tree.move(k, node, index)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children(''))

    def populate_roots(self):
        """
        Populates the treeview with the directory's files.

        :return: None
        """
        dir_ = os.path.abspath(self._path).replace('\\', '/')
        node = self.tree.insert('', 'end',
                                text=self._name.capitalize(),
                                values=[dir_, "directory"], open=True,
                                tags=("base",))
        self.populate_tree(node)
        self.sort_tree(node)

    def update_tree(self, event):
        tree = event.widget
        self.populate_tree(tree.focus())
        self.sort_tree(tree.focus())

    def on_double_click(self, event):
        tree = event.widget
        node = tree.focus()
        if tree.item(node)["values"][1] == "directory":
            to_open = not bool(tree.item(node, option="open"))
            try:
                tree.item(node, option={"open": to_open})
            except TypeError:
                pass
        elif tree.item(node)["values"][1] == "file":
            path = tree.item(node)["values"][0]
            fname = path.split("/")[-1]
            mimetype = mimetypes.guess_type(fname)[0].split("/")[0]
            self.callbacks.get(mimetype, lambda *a, **kw: None)(path)

    def resize(self, width, height):
        self.tree.config(height=height // 20)
