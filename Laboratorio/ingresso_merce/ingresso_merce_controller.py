import tkinter as tk
import datetime
from tastiera_num import Tast_num

from config import get_config
from db import get_connection, close_connection
from .ingresso_merce_TKinter import setup_window, build_ui
from .mov_ingresso_merce import MovIngressoMerce
from anag_fornitori.fornitore import Fornitore


class IngressoMerce(tk.Toplevel):
    def __init__(self):
        super().__init__()
        setup_window(self)
        self.config = get_config()

        # Stati della UI
        self.modalita_inserimento = False
        self.modalita_modifica = False

        # Connessione al database
        self.conn = get_connection()
        self.c = self.conn.cursor()

        # progressivo lotto verrà richiesto in modo atomico quando si entra in modalità "NUOVO"
        # (vuoto -> non visualizzare nulla in label all'apertura)
        self.prog_lotto_acq = None
        # guard per evitare doppie allocazioni del progressivo in caso di click ripetuti / handler concorrenti
        self._allocating_prog_acq = False


        # Struttura temporanea per l'inserimento multiplo
        self.lista_da_salvare = []
        self.fornitore = tk.StringVar()
        self.taglio_s = tk.StringVar()
        self.peso = tk.StringVar()
        self.data = tk.StringVar()
        self.data.set(datetime.date.today().strftime("%d-%m-%Y"))

        # Cache liste (tagli) per merceologia
        self.lista_fornitori = []
        # Recupera le aziende dei fornitori abilitati per "ingresso merce" usando il modello.
        # Nota: `Fornitore` fornisce i campi completi; qui servono solo `azienda`.
        

        for f in Fornitore.fetch_all(self.c):
            if getattr(f, "flag1_ing_merce", 0) == 1:
                self.lista_fornitori.append(f.azienda)

        self.lst_agnello = self._load_tagli_by_merceologia(12)
        self.lst_bovino = self._load_tagli_by_merceologia(10)
        self.lst_suino = self._load_tagli_by_merceologia(11)
        self.lst_vitello = self._load_tagli_by_merceologia(13)

        build_ui(self)

        # Aggancio gestione click in tabella
        self.tree_elenco.bind("<<TreeviewSelect>>", self._onsingleclick)
        self.tree_elenco.bind("<ButtonRelease-1>", self._onsingleclick)

        self._carica_elenco_ingresso_merce()
        self._disabilita_campi()

    def _load_tagli_by_merceologia(self, merceologia_id):
        lista_tagli = []
        self.c.execute(
            "SELECT taglio FROM tagli WHERE Id_Merceologia = %s", (merceologia_id,)
        )
        for row in self.c:
            lista_tagli.extend(row)
        return lista_tagli

    def _rimuovi_riga(self):
        curitem = self.tree_elenco.selection()[0]
        self.tree_elenco.delete(curitem)

    def _aggiungi_riga(self, merc='11'):
        self.tree_elenco.insert(
            "",
            "end",
            values=(
                str(self.prog_lotto_acq) + 'A',
                self.data.get(),
                self.num_ddt.get(),
                self.fornitore.get(),
                self.taglio_s.get(),
                self.peso.get(),
                self.peso.get(),
                'no',
                merc,
            ),
        )
        self.entry_peso.delete(0, tk.END)

    def _salva(self):
        # Caso: aggiornamento di una riga già presente
        if self.modalita_modifica:
            sel = self.tree_elenco.selection()
            if not sel:
                return

            # Recupero i valori della riga selezionata per ricostruire la chiave DB
            item_values = self.tree_elenco.item(sel[0], "values")
            if not item_values or len(item_values) < 10:
                return

            nr_lotto, fornitore, data_db, prog_acq, num_ddt, taglio, peso_i, peso_f, lotto_chiuso, id_merc = item_values[
                :10
            ]

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

            if mov:
                # Aggiorno i campi con i valori inseriti dalla UI
                try:
                    mov.data = datetime.datetime.strptime(self.data.get(), "%d-%m-%Y").date()
                except Exception:
                    mov.data = self.data.get()

                mov.num_ddt = self.num_ddt.get()
                mov.fornitore = self.fornitore.get()
                mov.taglio = self.taglio_s.get()

                # Allineo il campo modello: la UI scrive in self.peso ma il modello usa peso_i
                mov.peso_i = self.peso.get()

                mov.save(self.c, self.conn)

            self._carica_elenco_ingresso_merce()
            self._disabilita_campi()
            return

        # Caso: inserimento di nuovi movimenti (workflow già implementato in UI)
        for child in self.tree_elenco.get_children():
            self.lista_da_salvare.append(self.tree_elenco.item(child)["values"])

        for values in self.lista_da_salvare:
            mov = MovIngressoMerce.from_row(values)
            mov.insert(self.c, self.conn)

        # Progressivo già assegnato in modalità "NUOVO".
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
        
    def _sposta_focus_su_peso(self, *args):
        """Sposta il focus su entry_peso quando viene selezionato un taglio.

        Nota: la UI può mettere entry_peso in state='disabled' (es. sola lettura).
        Per evitare focus non desiderati o non applicati, facciamo focus solo
        quando l'entry è abilitata e la finestra è in inserimento/modifica.
        """
        if not (self.taglio_s.get() and hasattr(self, "entry_peso")):
            return

        # Se la finestra è in sola lettura, non forzare il focus.
        if not (getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False)):
            return

        try:
            # Best-effort: se per qualche motivo lo stato non è normal, provo ad abilitarlo.
            if str(self.entry_peso.cget("state")) == "disabled":
                self.entry_peso.configure(state="normal")

            self.entry_peso.focus_set()
            self.entry_peso.select_range(0, "end")
        except Exception:
            pass


    def _carica_elenco_ingresso_merce(self):
        """Popola la tabella principale con 1 riga per ogni `progressivo_acq`.

        Nota: i movimenti vengono ordinati da `fetch_all` per data decrescente,
        quindi teniamo la prima occorrenza (quella più recente) per progressivo_acq.
        """
        for child in self.tree_elenco.get_children():
            self.tree_elenco.delete(child)

        movimenti = MovIngressoMerce.fetch_all(self.c)

        # Deduplica per progressivo_acq: 1 riga per progressivo.
        # In ordine data decrescente, la prima incontrata è la più recente.
        visto_prog_acq = set()
        for mov in movimenti:
            prog = mov.prog_acq
            if prog in visto_prog_acq:
                continue
            visto_prog_acq.add(prog)

            data_visibile = (
                mov.data.strftime("%d-%m-%Y")
                if hasattr(mov.data, "strftime")
                else str(mov.data)
            )

            self.tree_elenco.insert(
                "",
                "end",
                values=(
                    mov.prog_acq,
                    mov.fornitore,
                    data_visibile,
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
        """Aggiorna riepilogo e campi di input in base alla riga selezionata."""
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        sel = self.tree_elenco.selection()
        if not sel:
            return

        item_values = self.tree_elenco.item(sel[0], "values")
        if not item_values or len(item_values) < 10:
            return

        prog_acq_selezionato = item_values[3]
        # Aggiorna label del progressivo lotto in base alla riga selezionata nel tree_elenco
        try:
            self.label_prog_lotto.configure(text=str(prog_acq_selezionato))
        except Exception:
            # fallback best-effort: aggiorna direttamente il valore usato in UI
            try:
                self.label_prog_lotto.config(text=str(prog_acq_selezionato))
            except Exception:
                pass


        for child in self.tree_riepilogo.get_children():
            self.tree_riepilogo.delete(child)

        movimenti_lotto = MovIngressoMerce.fetch_by_progressivo(self.c, prog_acq_selezionato)

        for mov in movimenti_lotto:
            data_visibile = mov.data.strftime("%d-%m-%Y") if hasattr(mov.data, "strftime") else str(mov.data)
            valore_prodotto = getattr(mov, "prodotto", None) or getattr(mov, "taglio", None) or ""

            valori_riga = (
                mov.prog_acq or "",
                data_visibile,
                mov.num_ddt,
                mov.fornitore,
                valore_prodotto,
                mov.peso_i,
                mov.peso_f,
                mov.lotto_chiuso,
                mov.id_merc,
            )
            self.tree_riepilogo.insert("", "end", values=valori_riga)

        if movimenti_lotto:
            mov_primo = movimenti_lotto[0]
            self.fornitore.set(mov_primo.fornitore)

            if hasattr(mov_primo.data, "strftime"):
                self.data.set(mov_primo.data.strftime("%d-%m-%Y"))
            else:
                self.data.set(str(mov_primo.data))

            self.num_ddt.set(mov_primo.num_ddt)
            self.taglio_s.set(mov_primo.taglio)
            self.peso.set(mov_primo.peso_i)

        return

    def _disabilita_campi(self):
        """Imposta la finestra in sola lettura."""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        try:
            self.entry_ddt.configure(state="disabled")
        except Exception:
            pass
        try:
            self.entry_peso.configure(state="disabled")
        except Exception:
            pass

        try:
            self.data_picker.configure(state="disabled")
        except Exception:
            pass

        try:
            winfo_children = getattr(self.data_picker, "winfo_children", None)
            if callable(winfo_children):
                for child in winfo_children():
                    try:
                        child.configure(state="disabled")
                    except Exception:
                        pass
        except Exception:
            pass

        try:
            self.btn_ins_num_ddt.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_ins_peso.configure(state="disabled")
        except Exception:
            pass

        try:
            self.btn_nuovo.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_modifica.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_salva.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_annulla.configure(state="disabled")
        except Exception:
            pass

        try:
            self.btn_aggiungi_riga.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_rimuovi_riga.configure(state="disabled")
        except Exception:
            pass

    def _nuovo(self):
        """Attiva la modalità inserimento e abilita i campi necessari."""
        self.modalita_inserimento = True
        self.modalita_modifica = False

        try:
            if hasattr(self, "tree_elenco") and self.tree_elenco.selection():
                self.tree_elenco.selection_remove(self.tree_elenco.selection())
        except Exception:
            pass

        self.num_ddt.set("")
        self.peso.set("")
        self.fornitore.set("")
        self.taglio_s.set("")
        try:
            self.data.set(datetime.date.today().strftime("%d-%m-%Y"))
        except Exception:
            pass

        try:
            self.entry_ddt.configure(state="normal")
        except Exception:
            pass
        try:
            self.entry_peso.configure(state="normal")
        except Exception:
            pass

        try:
            self.data_picker.configure(state="normal")
        except Exception:
            try:
                for child in self.data_picker.winfo_children():
                    try:
                        child.configure(state="normal")
                    except Exception:
                        pass
            except Exception:
                pass

        try:
            self.btn_ins_num_ddt.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_ins_peso.configure(state="normal")
        except Exception:
            pass

        try:
            for child in self.winfo_children():
                self._best_effort_enable_widgets(child)
        except Exception:
            pass

        try:
            self.btn_nuovo.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_modifica.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_salva.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_annulla.configure(state="normal")
        except Exception:
            pass

        try:
            self.btn_aggiungi_riga.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_rimuovi_riga.configure(state="disabled")
        except Exception:
            pass

        # Richiedi progressivo in modo atomico (evita race condition tra finestre)
        # Solo al primo accesso alla modalità "NUOVO".
        if self.prog_lotto_acq is None:
            self.prog_lotto_acq = self._next_prog_acq()


            # aggiorna UI
            try:
                self.label_prog_lotto.configure(text=f"{self.prog_lotto_acq}A")
            except Exception:
                try:
                    self.label_prog_lotto.config(text=f"{self.prog_lotto_acq}A")
                except Exception:
                    pass

        # abilita riga (non deve dipendere dall'allocazione progressivo: evita blocchi UI)
        try:
            self.btn_aggiungi_riga.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_rimuovi_riga.configure(state="normal")
        except Exception:
            pass

        return


    def _next_prog_acq(self):
        """Preleva e incrementa il progressivo in modo atomico (consumo DB).

        Nota: questa funzione è resa robusta contro lo stato transazionale già aperto
        (evita ProgrammingError: "Transaction already in progress").
        """
        # guard contro doppie allocazioni
        if self._allocating_prog_acq:
            # se chiamata concorrente/click ripetuti, non allocare due volte
            raise RuntimeError("Allocazione progressivo già in corso")

        self._allocating_prog_acq = True
        try:
            # best-effort: se esiste già una transaction attiva, facciamo rollback
            # (evita l'errore di start_transaction)
            try:
                self.conn.rollback()
            except Exception:
                pass

            self.conn.start_transaction()
            self.c.execute("SELECT prog_acq FROM progressivi FOR UPDATE")
            row = self.c.fetchone()
            if not row:
                raise RuntimeError("Nessun progressivo presente in tabella progressivi")
            current = row[0]
            self.c.execute("UPDATE progressivi SET prog_acq = prog_acq + 1")
            self.conn.commit()
            return current
        except Exception:
            try:
                self.conn.rollback()
            except Exception:
                pass
            raise
        finally:
            self._allocating_prog_acq = False



    def _best_effort_disable_widgets(self, widget):

        """Disabilita widget compatibili con state='disabled' (best-effort)."""
        try:
            widget.configure(state="disabled")
        except Exception:
            pass

        try:
            for gc in widget.winfo_children():
                self._best_effort_disable_widgets(gc)
        except Exception:
            pass

    def _modifica(self):
        """Attiva la modalità modifica e abilita i campi relativi."""
        sel = self.tree_elenco.selection()
        if not sel:
            return

        self.modalita_inserimento = False
        self.modalita_modifica = True

        self.entry_ddt.configure(state="normal")
        self.entry_peso.configure(state="normal")

        try:
            self.data_picker.configure(state="normal")
        except Exception:
            try:
                for child in self.data_picker.winfo_children():
                    try:
                        child.configure(state="normal")
                    except Exception:
                        pass
            except Exception:
                pass

        try:
            self.btn_ins_num_ddt.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_ins_peso.configure(state="normal")
        except Exception:
            pass

        try:
            for child in self.winfo_children():
                self._best_effort_enable_widgets(child)
        except Exception:
            pass

        try:
            self.btn_nuovo.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_modifica.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_salva.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_annulla.configure(state="normal")
        except Exception:
            pass

        try:
            self.btn_aggiungi_riga.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_rimuovi_riga.configure(state="disabled")
        except Exception:
            pass

        return

    def _annulla(self):
        """Annulla modifica/inserimento ripristinando i valori della riga selezionata."""
        sel = self.tree_elenco.selection()
        if not sel:
            self.modalita_inserimento = False
            self.modalita_modifica = False
            self._disabilita_campi()
            return

        self.modalita_inserimento = False
        self.modalita_modifica = False

        item_values = self.tree_elenco.item(sel[0], "values")
        if not item_values or len(item_values) < 10:
            self._disabilita_campi()
            return

        _, fornitore, data_db, prog_acq, num_ddt, taglio, peso_i, peso_f, lotto_chiuso, id_merc = item_values[:10]

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

        if mov:
            self.fornitore.set(getattr(mov, "fornitore", None) or fornitore or "")
            try:
                if hasattr(mov.data, "strftime"):
                    self.data.set(mov.data.strftime("%d-%m-%Y"))
                else:
                    self.data.set(str(mov.data))
            except Exception:
                self.data.set(str(data_db))

            self.num_ddt.set(getattr(mov, "num_ddt", None) or num_ddt or "")
            self.taglio_s.set(getattr(mov, "taglio", None) or taglio or "")
            self.peso.set(getattr(mov, "peso_i", None) or peso_i or "")
        else:
            self.fornitore.set(fornitore or "")
            self.data.set(str(data_db))
            self.num_ddt.set(num_ddt or "")
            self.taglio_s.set(taglio or "")
            self.peso.set(peso_i or "")

        self._disabilita_campi()

        try:
            self.btn_nuovo.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_modifica.configure(state="normal")
        except Exception:
            pass
        try:
            self.btn_salva.configure(state="disabled")
        except Exception:
            pass
        try:
            self.btn_annulla.configure(state="disabled")
        except Exception:
            pass

        return

    def _best_effort_enable_widgets(self, widget):
        """Abilita widget compatibili con state='normal' (best-effort)."""
        try:
            widget.configure(state="normal")
        except Exception:
            pass

        try:
            for gc in widget.winfo_children():
                self._best_effort_enable_widgets(gc)
        except Exception:
            pass

    def _chiudi(self):
        self.destroy()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()

