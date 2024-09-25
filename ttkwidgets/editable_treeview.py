"""
Author: Faraaz Kurawle
License: GNU GPLv3
Source: This repository
"""

from tkinter import ttk
import tkinter as tk

class PopupEntry(tk.Entry):
    """
    Provides a temporary tk.Entry widget which can be used to show a temporaty entry widget to retrive data from user.
    After retriving data, it returns the value back and gets destroyed.

    Used internaly by EditableTreeview.

    :param parent: parent of the widget, ideally EditableTreeview
    :type parent: widget

    :param x: location of x-axis where PoputEntry would be placed
    :type x: integer

    :param y: location of y-axis where PoputEntry would be placed
    :type x: integer

    :param textvar: Tkinter varaible which would store and return new value.
    :type x: Tkinter Varaible

    :param width: width of the Entry.
    :type x: integer

    :param height: height of the Entry
    :type x: integer

    :param entry_value: current value inside Entry widget.
    :type x: string

    :param options: All valid customization option of tk.Entry widget.
    """

    def __init__(
        self,
        parent,
        x,
        y,
        textvar,
        width,
        height,
        entry_value="",
        **options
    ):
        super().__init__(
            parent,
            textvariable=textvar,
            **options
        )
        self.place(x=x + 1, y=y, width=width, height=height)

        self.textvar = textvar
        self.textvar.set(entry_value)
        self.focus_set()
        self.select_range(0, "end")
        # move cursor to the end
        self.icursor("end")

        self.wait_var = tk.StringVar(master=self)

        self._bind_widget()
        self.wait_window()

    def _bind_widget(self):
        self.bind("<Return>", self.retrive_value)
        self.bind("<FocusOut>", self.retrive_value)

    def retrive_value(self, e):
        value = self.textvar.get()
        self.destroy()
        self.textvar.set(value)

class EditableTreeview(ttk.Treeview):
    """Customized Treeview with cell editing feature

    :param parent: parent widget
    :type parent: widget

    :param coloums: List of column names for the column heading.
    :type columns: tuple

    :param bind_key: key which would trigger editting of the cell
    :type bind_key: string in format "<DEMO>" OR "<<DEMO>>

    :noneditable_columns: List of Columns of which values wont be editted. In format "#COLUMN_NUMBER"
    :type noneditable_columns: tupple
    :note noneditable_columns: #0 is reserved for indexing, therefore all data inserted starts from #1.

    :param treeview_options: all valid treeview options"""

    def __init__(
        self,
        parent,
        columns: tuple,
        data: dict,
        bind_key="<Double-Button-1>",
        non_editable_columns=("",),
        **treeview_options
    ):
        super().__init__(parent,columns=columns, **treeview_options)
        self.parent = parent
        self.column_name = columns
        self.data = data
        self.bind_key = bind_key
        self.non_editable_columns = non_editable_columns

        self.set_primary_key_column_attributes()
        self.set_headings()
        self.insert_data()
        self.set_edit_bind_key()

    def set_primary_key_column_attributes(self):
        self.column("#0", width=100, stretch=1)

    def set_headings(self):
        for i in self.column_name:
            self.heading(column=i, text=i)

    def insert_data(self):
        for values in self.data.items():
            self.insert("", tk.END, values=values)
        

    def set_edit_bind_key(self):
        self.bind("<Double Button-1>", self.edit)

    def get_absolute_x_cord(self):
        rootx = self.winfo_pointerx()
        widgetx = self.winfo_rootx()

        x = rootx - widgetx

        return x

    def get_absolute_y_cord(self):
        rooty = self.winfo_pointery()
        widgety = self.winfo_rooty()

        y = rooty - widgety
        return y

    def get_current_column(self):
        pointer = self.get_absolute_x_cord()
        return self.identify_column(pointer)

    def get_cell_cords(self, row, column):
        return self.bbox(row, column=column)

    def get_selected_cell_cords(self):
        row = self.focus()
        column = self.get_current_column()
        return self.get_cell_cords(row=row, column=column)

    def update_row(self, values, current_row, currentindex):
        self.delete(current_row)
        self.insert("", currentindex, values=values)

    def check_region(self):
        result = self.identify_region(
            x=(self.winfo_pointerx() - self.winfo_rootx()),
            y=(self.winfo_pointery() - self.winfo_rooty()),
        )
        if result == "cell":
            return True
        else:
            return False

    def check_non_editable(self):
        if self.get_current_column() in self.non_editable_columns:
            return False
        else:
            return True

    def edit(self, e):
        if self.check_region() == False:
            return
        elif self.check_non_editable() == False:
            return

        current_row = self.focus()
        currentindex = self.index(self.focus())
        current_row_values = list(self.item(self.focus(), "values"))
        current_column = int(self.get_current_column().replace("#", "")) - 1
        current_cell_value = current_row_values[current_column]

        entry_cord = self.get_selected_cell_cords()
        entry_x = entry_cord[0] - 1
        entry_y = entry_cord[1] 
        entry_w = entry_cord[2]
        entry_h = entry_cord[3] 

        entry_var = tk.StringVar()
        
        PopupEntry(
            self,
            x=entry_x,
            y=entry_y,
            width=entry_w,
            height=entry_h,
            entry_value=current_cell_value,
            textvar=entry_var,
            relief="flat",
            bg="white",
        )

        if entry_var.get() != current_cell_value:
            current_row_values[current_column] = entry_var.get()
            self.update_row(
                values=current_row_values,
                current_row=current_row,
                currentindex=currentindex,
            )
