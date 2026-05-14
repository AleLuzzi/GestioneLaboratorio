import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector

from config import get_config
from db import get_connection, close_connection
from theme import COLORS, get_font
from chiudi_lotto_TKinter import setup_window, build_ui


class ChiudiLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
       
        setup_window(self)

        # Connessione al database
        self.conn = get_connection()
        self.c = self.conn.cursor()

        self.lotti_da_chiudere = []

        build_ui(self)
        
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

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = ChiudiLotto()
    root.mainloop()
