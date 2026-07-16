import tkinter as tk
import datetime
from tastiera_num import Tast_num

from config import get_config
from db import get_connection, close_connection
from .ingresso_merce_TKinter import setup_window, build_ui
from .mov_ingresso_merce import MovIngressoMerce


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

        # Bind click singolo/selection sul riepilogo inserimenti
        # Event standard ttk.Treeview:
        #   - <<TreeviewSelect>> quando cambia la selection
        #   - fallback su rilascio tasto per casi in cui l'evento virtuale non viene catturato
        self.tree_elenco.bind("<<TreeviewSelect>>", self._onsingleclick)
        self.tree_elenco.bind("<ButtonRelease-1>", self._onsingleclick)

        self._carica_elenco_ingresso_merce()

    def _load_tagli_by_merceologia(self, merceologia_id):
        lista_tagli = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = %s", (merceologia_id,))
        for row in self.c:
            lista_tagli.extend(row)
        return lista_tagli

    def _rimuovi_riga_selezionata(self):
        curitem = self.tree_elenco.selection()[0]
        self.tree_elenco.delete(curitem)

    def _invio(self, merc='11'):
        self.tree_elenco.insert("", 'end', values=((str(self.prog_lotto_acq)+'A'),
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
        for child in self.tree_elenco.get_children():
            self.lista_da_salvare.append(self.tree_elenco.item(child)['values'])

        # Sostituzione query INSERT con metodi MovIngressoMerce
        for values in self.lista_da_salvare:
            mov = MovIngressoMerce.from_row(values)
            mov.insert(self.c, self.conn)

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

    def _carica_elenco_ingresso_merce(self):
        """
        Carica nel tree_elencoview elenco la lista dei movimenti presenti su `ingresso_merce`.

        Colonne visibili:
          - nr Lotto = prog_acq + "A"
          - Fornitore = fornitore
          - Data = data

        Colonne nascoste (servono per ricostruire la chiave composta in _onsingleclick):
          - prog_acq, num_ddt, taglio, peso_i, peso_f, lotto_chiuso, id_merc
        """
        # Pulisce eventuali righe presenti
        for child in self.tree_elenco.get_children():
            self.tree_elenco.delete(child)

        movimenti = MovIngressoMerce.fetch_all(self.c)
        for mov in movimenti:
            nr_lotto = mov.prog_acq
            self.tree_elenco.insert(
                "",
                "end",
                values=(
                    nr_lotto,
                    mov.fornitore,
                    mov.data,
                    mov.prog_acq,
                    mov.num_ddt,
                    mov.taglio,
                    mov.peso_i,
                    mov.peso_f,
                    mov.lotto_chiuso,
                    mov.id_merc,
                ),
            )

    def _onsingleclick(self, event=None):
        """
        Popola i campi di inserimento quando l'utente seleziona una riga
        nel riepilogo (tree_elenco).

        Recupera i dettagli completi dal DB tramite MovIngressoMerce.
        """
        # Se l'utente sta editando, non sovrascrivere i campi
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        sel = self.tree_elenco.selection()
        if not sel:
            return

        item_values = self.tree_elenco.item(sel[0], "values")
        if not item_values or len(item_values) < 10:
            return

        # Valori della riga (coerenti con UI columns)
        nr_lotto, fornitore, data_db, prog_acq, num_ddt, taglio, peso_i, peso_f, lotto_chiuso, id_merc = item_values[:10]

        # Ricostruzione chiave composta (9 valori) per find_by_key
        # (prog_acq, data, num_ddt, fornitore, taglio, peso_i, peso_f, lotto_chiuso, id_merc)
        key = (
            prog_acq,
            data_db,
            num_ddt,
            fornitore,
            taglio,
            peso_i,
            peso_f,
            lotto_chiuso,
            id_merc,
        )

        mov = MovIngressoMerce.find_by_key(self.c, key)
        if not mov:
            return

        # Popolamento campi UI
        # NOTE: i radio button fornitore hanno come value i dati letti da DB con `SELECT azienda ...`,
        # quindi per selezionare correttamente dobbiamo valorizzare la StringVar con quella "azienda"
        # (che è esattamente `fornitore` preso dal tree_elencoview riga).
        self.fornitore.set(fornitore)

        try:
            # In UI controller usa formato stringa dd-mm-YYYY per self.data
            if hasattr(mov.data, "strftime"):
                self.data.set(mov.data.strftime("%d-%m-%Y"))
            else:
                self.data.set(str(mov.data))
        except Exception:
            self.data.set(str(data_db))

        try:
            self.num_ddt.set(getattr(mov, "num_ddt", None) or num_ddt or "")
        except Exception:
            self.num_ddt.set(num_ddt)

        # taglio (prodotto) -> se mov è incerto, usiamo il valore dal tree_elencoview
        self.taglio_s.set(getattr(mov, "taglio", None) or taglio or "")

        # peso_i (quantità) -> se mov è incerto, usiamo il valore dal tree_elencoview
        self.peso.set(getattr(mov, "peso_i", None) or peso_i or "")

        # Non richiamiamo aggiorna UI/ripristini perché qui è solo "read-only populate"
        return

    def _chiudi(self):
        self.destroy()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()
