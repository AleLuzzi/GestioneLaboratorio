import tkinter as tk
import datetime
from tastiera_num import Tast_num

from config import get_config
from db import get_connection, close_connection
from ingresso_merce_TKinter import setup_window, build_ui


class IngressoMerce(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        setup_window(self)
        self.config = get_config()

        # Connessione al database
        self.conn = get_connection()
        self.c = self.conn.cursor()

        # Lettura progressivo lotto acquisto da db
        self.c.execute("SELECT prog_acq FROM progressivi")
        self.prog_lotto_acq = self.c.fetchone()[0]

        # Inizializzazione lista per valori da salvare sul database
        self.lista_da_salvare = []
        self.fornitore = tk.StringVar()
        self.taglio_s = tk.StringVar()
        self.peso = tk.StringVar()
        self.data = tk.StringVar()
        self.data.set(datetime.date.today().strftime("%d-%m-%Y"))

        # Creazione liste fornitori
        self.lista_fornitori = []
        self.c.execute("SELECT azienda FROM fornitori WHERE flag1_ing_merce = 1")
        for row in self.c:
            self.lista_fornitori.extend(row)
        self.lst_agnello = self._load_tagli_by_merceologia(12)
        self.lst_bovino = self._load_tagli_by_merceologia(10)
        self.lst_suino = self._load_tagli_by_merceologia(11)
        self.lst_vitello = self._load_tagli_by_merceologia(13)

        build_ui(self)

    def _load_tagli_by_merceologia(self, merceologia_id):
        lista_tagli = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = %s", (merceologia_id,))
        for row in self.c:
            lista_tagli.extend(row)
        return lista_tagli

    def _rimuovi_riga_selezionata(self):
            curitem = self.tree.selection()[0]
            self.tree.delete(curitem)

    def _invio(self, merc='11'):
        self.tree.insert("", 'end', values=((str(self.prog_lotto_acq)+'A'),
                                            datetime.datetime.strptime(self.data.get(), "%d-%m-%Y").date(),
                                            self.num_ddt.get(),
                                            self.fornitore.get(),
                                            self.taglio_s.get(),
                                            self.peso.get(),
                                            self.peso.get(),
                                            'no',
                                            merc))
        self.entry.delete(0, tk.END)

    def _salva_esci(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        self.c.executemany('INSERT INTO ingresso_merce VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_acq = %s', (self.prog_lotto_acq + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def _ins_peso(self):
        peso = Tast_num(self)
        val = peso.value.get()
        self.peso.set(val)

    def _ins_num_ddt(self):
        ddt_num = Tast_num(self)
        val = ddt_num.value.get()
        self.num_ddt.set(val)

    def _chiudi(self):
        self.destroy()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()
