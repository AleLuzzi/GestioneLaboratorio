import tkinter as tk
from tkinter import ttk


class Dosi(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Dosi')

        self.peso = tk.Label(self, text='INSERISCI PESO')
        self.ent_peso = tk.Entry(self)
        self.ent_peso.focus()
        self.calcola = ttk.Button(self, text='CALCOLA')
        self.lbl_sale = tk.Label(self, text='SALE')
        self.lbl_pepe = tk.Label(self, text='PEPE')
        self.lbl_aglio = tk.Label(self, text='AGLIO')
        self.lbl_aromyl = tk.Label(self, text='AROMYL')
        self.lbl_acqua = tk.Label(self, text='ACQUA')

        self.peso.grid(row=0, column=0)
        self.ent_peso.grid(row=0, column=1)
        self.calcola.grid(row=1, column=0, sticky='we')
        self.lbl_sale.grid(row=2, column=0)
        self.lbl_pepe.grid(row=3, column=0)
        self.lbl_aglio.grid(row=4, column=0)
        self.lbl_aromyl.grid(row=5, column=0)
        self.lbl_acqua.grid(row=6, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    new = Dosi()
    root.mainloop()