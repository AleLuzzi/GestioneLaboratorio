import tkinter as tk
from tkinter import ttk


class Dosi(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Dosi')

        self.peso = tk.IntVar()
        self.peso.set('')

        def _calcola():
            sale = self.peso.get()*26
            self.lbl_sale_gr['text'] = str(sale) + ' gr'

            pepe = self.peso.get()*6
            self.lbl_pepe_gr['text'] = str(pepe) + ' gr'

            aglio = round(((self.peso.get()/100)*20), 2)
            self.lbl_aglio_gr['text'] = str(aglio) + ' gr'

            aromyl= self.peso.get()*8
            self.lbl_aromyl_gr['text'] = str(aromyl) + ' gr'

        def _reset():
            self.ent_peso.delete(0, 'end')

        def _chiudi():
            self.destroy()

        # DEFINIZIONE WIDGET
        self.lbl_peso = tk.Label(self, text='INSERISCI PESO',
                                       foreground='blue',
                                       font=('Verdana', 15))
        self.ent_peso = tk.Entry(self, textvariable=self.peso, width=25)
        self.ent_peso.focus()

        self.lbl_sale = tk.Label(self, text='SALE')
        self.lbl_sale_gr = tk.Label(self, text='')

        self.lbl_pepe = tk.Label(self, text='PEPE')
        self.lbl_pepe_gr = tk.Label(self, text='')

        self.lbl_aglio = tk.Label(self, text='AGLIO')
        self.lbl_aglio_gr = tk.Label(self, text='')
        
        self.lbl_aromyl = tk.Label(self, text='AROMYL')
        self.lbl_aromyl_gr = tk.Label(self, text='')
        
        self.lbl_acqua = tk.Label(self, text='ACQUA')
        
        self.calcola = ttk.Button(self, text='CALCOLA', command=_calcola)
        self.reset = ttk.Button(self, text='Reset', command=_reset)
        self.chiudi = ttk.Button(self, text='Chiudi', command=_chiudi)
        
        # LAYOUT
        self.lbl_peso.grid(row=0, column=0)
        self.ent_peso.grid(row=0, column=1)

        self.lbl_sale.grid(row=2, column=0)
        self.lbl_sale_gr.grid(row=2, column=1)

        self.lbl_pepe.grid(row=3, column=0)
        self.lbl_pepe_gr.grid(row=3, column=1)

        self.lbl_aglio.grid(row=4, column=0)
        self.lbl_aglio_gr.grid(row=4, column=1)
        
        self.lbl_aromyl.grid(row=5, column=0)
        self.lbl_aromyl_gr.grid(row=5, column=1)
        
        self.lbl_acqua.grid(row=6, column=0)

        self.calcola.grid(row=7, column=0, columnspan=2, sticky='we')
        self.reset.grid(row=8, column=0, sticky='we')
        self.chiudi.grid(row=8, column=1, sticky='we')


if __name__ == "__main__":
    root = tk.Tk()
    new = Dosi()
    root.mainloop()
