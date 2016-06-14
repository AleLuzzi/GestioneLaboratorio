import tkinter as tk


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frm_alto = tk.Frame(self)
        self.frm_alto.grid()

        img_btn1 = tk.PhotoImage(file='.//immagini//logo.gif')

        self.btn1 = tk.Button(self.frm_alto, text='btn1', compound='bottom', image=img_btn1)
        self.btn1.grid()


if __name__ == "__main__":
    root = tk.Tk()
    Main(root).grid()
    root.mainloop()
