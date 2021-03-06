import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector
import configparser


class ChiudiLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Chiudi Lotto")
        self.geometry("1024x525+0+0")

        self.config = self._leggi_file_ini()

        # Connessione al database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        self.lotti_da_chiudere = []

        # Disposizione Frame
        self.frame_sx = tk.Frame(self)
        self.frame_dx = tk.Frame(self)
        self.frame_dx_basso = tk.Frame(self, background='white')

        # Treeview con riepilogo lotti aperti
        self.tree = ttk.Treeview(self.frame_sx, height=25)
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

        self.tree.bind("<Double-1>", self._ondoubleclick)

        # LABEL lotti da chiudere
        self.lbl_nuovo_lotto = ttk.Label(self.frame_dx,
                                         text='LOTTI DA CHIUDERE',
                                         font=('Helvetica', 20))

        # Treeview per lotti scelti da chiudere
        self.tree_lotti_selezionati = ttk.Treeview(self.frame_dx)
        self.tree_lotti_selezionati['columns'] = ('lotto', 'taglio')

        self.tree_lotti_selezionati['show'] = 'headings'

        self.tree_lotti_selezionati.column("lotto", width=70)
        self.tree_lotti_selezionati.column("taglio", width=170)
        self.tree_lotti_selezionati.heading("lotto", text="Lotto")
        self.tree_lotti_selezionati.heading("taglio", text="Taglio")

        # BOTTONE ESCI
        self.btn_esci = tk.Button(self.frame_dx_basso,
                                  text="Chiudi finestra",
                                  font=('Helvetica', 20),
                                  command=self.destroy)

        self.btn_salva = tk.Button(self.frame_dx_basso,
                                   text='salva dati',
                                   font=('Helvetica', 20),
                                   command=self._salva)

        self.btn_rimuovi_riga = tk.Button(self.frame_dx, text="Rimuovi riga", command=self._rimuovi_riga_selezionata)
        

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, rowspan=2)
        self.frame_dx.grid(row=0, column=1, columnspan=2, padx=30)
        self.frame_dx_basso.grid(row=1, column=1)

        self.tree.grid(row=0, column=0, sticky='w')
        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.tree_lotti_selezionati.grid(row=1, column=0)
        self.btn_rimuovi_riga.grid(row=2, column=0, sticky='we')

        self.btn_esci.grid(row=2, column=0, pady=20, padx=20)
        self.btn_salva.grid(row=2, column=1, pady=20, padx=20)

        self._aggiorna()

    @staticmethod
    def _leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def _rimuovi_riga_selezionata(self):
            curitem = self.tree_lotti_selezionati.selection()[0]
            self.tree_lotti_selezionati.delete(curitem)

    def _ondoubleclick(self, event):
        item = self.tree.selection()[0]
        self.tree_lotti_selezionati.insert("", 'end',
                                           values=(self.tree.parent(item),
                                                   self.tree.item(item, 'text')))

    def _salva(self):
        for child in self.tree_lotti_selezionati.get_children():
            self.lotti_da_chiudere.append(self.tree_lotti_selezionati.item(child)['values'])
        self.c.executemany("UPDATE ingresso_merce SET lotto_chiuso = 'si' WHERE progressivo_acq = %s AND prodotto = %s ",
                           self.lotti_da_chiudere)
        self.conn.commit()
        self._aggiorna()

    def _aggiorna(self):

        self.tree.delete(*self.tree.get_children())
        self.tree_lotti_selezionati.delete(*self.tree_lotti_selezionati.get_children())

        self.c.execute("SELECT * from ingresso_merce WHERE lotto_chiuso = 'no'")
        for lista in self.c:
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
