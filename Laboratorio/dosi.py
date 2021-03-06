import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Dosi(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Dosi')

        self.peso = tk.DoubleVar()
        self.peso.set('')

        def _calcola(event=None):
            if self.peso.get() == 0 or self.peso.get() == 1:
                messagebox.showinfo("-- ERRORE --", "Valore inserito non valido", icon="warning")
                self.ent_peso.focus()
            if self.peso.get() > 1:
                sale = round(self.peso.get() * 26, 2)
                self.lbl_sale_gr['text'] = str(sale) + ' gr'

                pepe = round(self.peso.get() * 5, 2)
                self.lbl_pepe_gr['text'] = str(pepe) + ' gr'

                aglio = round(((self.peso.get() / 100) * 20), 2)
                self.lbl_aglio_gr['text'] = str(aglio) + ' gr'

                aromyl = round(self.peso.get() * 8, 2)
                self.lbl_aromyl_gr['text'] = str(aromyl) + ' gr'

        def _reset():
            self.ent_peso.delete(0, 'end')
            self.lbl_sale_gr['text'] = '0 gr'
            self.lbl_pepe_gr['text'] = '0 gr'
            self.lbl_aglio_gr['text'] = '0 gr'
            self.lbl_aromyl_gr['text'] = '0 gr'
            self.ent_peso.focus()

        def _chiudi():
            self.destroy()

        # DEFINIZIONE WIDGET
        self.bind('<Return>', _calcola)

        self.lbl_peso = tk.Label(self, text='INSERISCI PESO',
                                 foreground='blue',
                                 font=('Verdana', 15),
                                 relief='ridge',
                                 bg='white')
        self.ent_peso = tk.Entry(self, textvariable=self.peso,
                                 width=5, font=('Verdana', 30))
        self.ent_peso.focus()

        self.lbl_sale = tk.Label(self, text='SALE', font=('Verdana', 15))
        self.lbl_sale_gr = tk.Label(self, text='0 gr', font=('Verdana', 15))

        self.lbl_pepe = tk.Label(self, text='PEPE', font=('Verdana', 15))
        self.lbl_pepe_gr = tk.Label(self, text='0 gr', font=('Verdana', 15))

        self.lbl_aglio = tk.Label(self, text='AGLIO', font=('Verdana', 15))
        self.lbl_aglio_gr = tk.Label(self, text='0 gr', font=('Verdana', 15))

        self.lbl_aromyl = tk.Label(self, text='AROMYL', font=('Verdana', 15))
        self.lbl_aromyl_gr = tk.Label(self, text='0 gr', font=('Verdana', 15))

        self.lbl_acqua = tk.Label(self, text='ACQUA', font=('Verdana', 15))

        style = ttk.Style()
        style.configure('W.TButton', font=('Verdana', 12, 'bold'))

        self.calcola = ttk.Button(self, text='CALCOLA', style='W.TButton', command=_calcola)
        self.reset = ttk.Button(self, text='Reset', style='W.TButton', command=_reset)
        self.chiudi = ttk.Button(self, text='Chiudi', style='W.TButton', command=_chiudi)

        # LAYOUT
        self.lbl_peso.grid(row=0, column=0, sticky='ns')
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
