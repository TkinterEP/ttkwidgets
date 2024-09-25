from ttkwidgets.numberedtext import NumberedText
import tkinter as tk
def demo():
    root = tk.Tk()
    root.title("NumberedText Demo")
    NumberedText(root, bg="red").pack(side="left")
    root.mainloop()

if __name__ == "__main__":
    demo()