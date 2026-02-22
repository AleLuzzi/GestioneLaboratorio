import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from theme import COLORS, get_font


class Dosi(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.configure(bg=COLORS["bg_light"])
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

        self.lbl_peso = ttk.Label(self, text='Inserisci peso (kg)', font=get_font(12, bold=True))
        self.ent_peso = ttk.Entry(self, textvariable=self.peso, width=8)
        self.ent_peso.focus()

        self.lbl_sale = ttk.Label(self, text='Sale', font=get_font())
        self.lbl_sale_gr = tk.Label(self, text='0 gr', font=get_font(), bg=COLORS["bg_light"], fg=COLORS["text_dark"])
        self.lbl_pepe = ttk.Label(self, text='Pepe', font=get_font())
        self.lbl_pepe_gr = tk.Label(self, text='0 gr', font=get_font(), bg=COLORS["bg_light"], fg=COLORS["text_dark"])
        self.lbl_aglio = ttk.Label(self, text='Aglio', font=get_font())
        self.lbl_aglio_gr = tk.Label(self, text='0 gr', font=get_font(), bg=COLORS["bg_light"], fg=COLORS["text_dark"])
        self.lbl_aromyl = ttk.Label(self, text='Aromyl', font=get_font())
        self.lbl_aromyl_gr = tk.Label(self, text='0 gr', font=get_font(), bg=COLORS["bg_light"], fg=COLORS["text_dark"])
        self.lbl_acqua = ttk.Label(self, text='Acqua', font=get_font())

        self.calcola = ttk.Button(self, text='Calcola', command=_calcola)
        self.reset = ttk.Button(self, text='Reset', command=_reset)
        self.chiudi = ttk.Button(self, text='Chiudi', command=_chiudi)

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
