import tkinter as tk
from tkinter import ttk


class Dosi(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Dosi')


if __name__ == "__main__":
    root = tk.Tk()
    new = Dosi()
    root.mainloop()