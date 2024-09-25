from ttkwidgets.editable_treeview import EditableTreeview
import tkinter as tk

def demo():
    root = tk.Tk()
    root.title("NumberedText Demo")
    columns = ("attribute", "value")
    data = {f"Demo {i}": f"Demo {i}" for i in range(1, 101)}

    widget = EditableTreeview(root, columns=columns, show=" tree", bind_key="<Double-Button-1>", data=data)
    widget.pack(expand=1, fill="both", padx=20, pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    demo()