import tkinter as tk
from tkinter import ttk
import datetime as dt
import sqlite3


class ChiudiLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Chiudi Lotto")
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())
        '''
        Connessione al database
        '''
        self.conn = sqlite3.connect('data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()

        self.lotti_da_chiudere = []
        '''
        Disposizione Frame
        '''
        self.frame_treeview = ttk.Frame(self)
        self.frame_treeview.grid(row='1', column='0')

        self.frame_lotti_chiusi = ttk.Frame(self)
        self.frame_lotti_chiusi.grid(row='1', column='1')
        '''
        Treeview con riepilogo lotti aperti
        '''
        self.tree = ttk.Treeview(self.frame_treeview, height=25)
        self.tree['columns'] = ('data ingresso', 'fornitore', 'peso', 'residuo')

        self.tree.column("data ingresso", width=80)
        self.tree.column("fornitore", width=80)
        self.tree.column("peso", width=80)
        self.tree.column("residuo", width=60)

        self.tree.heading("data ingresso", text="data ingresso")
        self.tree.heading("fornitore", text="fornitore")
        self.tree.heading("peso", text="peso")
        self.tree.heading("residuo", text="residuo")

        self.tree.tag_configure('odd', background='light green')

        self.tree.bind("<Double-1>", self.ondoubleclick)

        self.tree.grid(row='1', column='0', sticky='w')
        '''
        LABEL lotti da chiudere
        '''
        self.lbl_nuovo_lotto = ttk.Label(self.frame_lotti_chiusi,
                                         text='LOTTI DA CHIUDERE',
                                         font=('Helvetica', 20))
        self.lbl_nuovo_lotto.grid(row='1', column='0')
        '''
        Treeview per lotti scelti da chiudere
        '''
        self.tree_lotti_selezionati = ttk.Treeview(self.frame_lotti_chiusi)
        self.tree_lotti_selezionati['columns'] = 'taglio'

        self.tree_lotti_selezionati.column("taglio", width=70)
        self.tree_lotti_selezionati.heading("taglio", text="taglio")

        self.tree_lotti_selezionati.grid(row='2', column='0')

        '''
        BOTTONE ESCI
        '''
        self.btn_esci = ttk.Button(self.frame_lotti_chiusi,
                                   text="Chiudi finestra",
                                   command=self.destroy)
        self.btn_esci.grid(row='4', column='0', pady=20)

        self.btn_salva = ttk.Button(self.frame_lotti_chiusi,
                                    text='salva dati',
                                    command=self.salva)
        self.btn_salva.grid(row='3', column='0', pady=20)

        self.aggiorna()

    def ondoubleclick(self, event):
        item = self.tree.selection()[0]
        self.tree_lotti_selezionati.insert('', 'end', text=self.tree.parent(item),
                                               values=(self.tree.item(item, 'text')))
        self.lotti_da_chiudere.append((self.tree.parent(item), (self.tree.item(item, 'text')),))

    def salva(self):

        self.c.executemany("UPDATE ingresso_merce SET lotto_chiuso = 'si' WHERE progressivo_acq = ? AND prodotto = ? ",
                           self.lotti_da_chiudere)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):

        self.tree.delete(*self.tree.get_children())
        self.tree_lotti_selezionati.delete(*self.tree_lotti_selezionati.get_children())
        for lista in self.c.execute("SELECT * from ingresso_merce WHERE lotto_chiuso = 'no'"):
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5], lista[6]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5], lista[6]))
                self.tree.item(lista[0], open='true')


if __name__ == '__main__':
    root = tk.Tk()
    new = ChiudiLotto()
    root.mainloop()
