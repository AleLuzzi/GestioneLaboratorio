import tkinter as tk


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frm_alto = tk.Frame(self)

        self.btn1 = tk.Button(self, text='btn1')
        self.btn1.grid(row=0, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    Main(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
