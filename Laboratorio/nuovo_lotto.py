import tkinter as tk
import datetime as dt
import mysql.connector
from tkinter import messagebox
from tastiera_num import Tast_num

from config import get_config
from db import get_connection, close_connection
from nuovo_lotto_TKinter import setup_window, build_ui, populate_produzione_radio


class NuovoLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        setup_window(self)
        self.data = dt.date.today()

        self.config = get_config()

        self.conn = get_connection()
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        self.nuova_produzione = tk.StringVar()
        self.peso_da_inserire = tk.StringVar()
        self.prog_lotto_ven = self.genera_prog_vendita()

        build_ui(self)

        self.lotti_acq_aperti()
        self.riempi_lista_produzione()

    def _ins_peso(self):
        peso = Tast_num(self)
        val = peso.value.get()
        self.peso_da_inserire.set(val)

    def rimuovi_riga_selezionata(self):
        curitem = self.tree_lotti_selezionati.selection()[0]
        self.tree_lotti_selezionati.delete(curitem)

    def genera_prog_vendita(self):
        self.c.execute("SELECT prog_ven FROM progressivi")
        prog = self.c.fetchone()[0]
        return prog

    def riempi_lista_produzione(self):
        # Lista articoli per nuova produzione
        self.c.execute("SELECT prodotto FROM prodotti WHERE reparto = 'Macelleria'")
        for row in self.c:
            self.lista_nuova_produzione.extend(row)
        populate_produzione_radio(self)

    def lotti_acq_aperti(self):
        # Ciclo per inserire i lotti in acquisto da utilizzare
        self.c.execute("SELECT * from ingresso_merce WHERE lotto_chiuso = 'no'")
        for lista in self.c:
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')

    def esci_salva(self):
        for child in self.tree_lotti_selezionati.get_children():
            self.lista_da_salvare.append(self.tree_lotti_selezionati.item(child)['values'])
        self.c.executemany('INSERT INTO lotti_vendita VALUES (%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_ven = %s', (self.prog_lotto_ven + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def esci_senza_salvare(self):
        if bool(self.tree_lotti_selezionati.get_children()):
            messagebox.showinfo('Attenzione', 'Ci sono dati inseriti non salvati')
        else:
            self.destroy()

    def ondoubleclick(self, event):
        if (self.nuova_produzione.get() != '') and (self.peso_da_inserire.get() != ''):
            item = self.tree.selection()[0]
            self.tree_lotti_selezionati.insert('', 'end', values=((str(self.prog_lotto_ven) + 'V'),
                                                                  self.data,
                                                                  self.tree.parent(item),
                                                                  (self.nuova_produzione.get()),
                                                                  (self.peso_da_inserire.get()),
                                                                  (self.tree.item(item, 'text'))))
        else:
            pass

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLotto()
    root.mainloop()
