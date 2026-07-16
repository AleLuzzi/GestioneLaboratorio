import tkinter as tk
from tkinter import messagebox

from db import close_connection, get_connection
from anag_merceologie.merceologia import Merceologia
from anag_merceologie.anag_merceologie_TKinter import build_ui



class AnagMerceologieController(tk.Toplevel):
    """Controller per la gestione tabella `merceologie`.

    Separazione rispetto alla GUI: la finestra UI deve chiamare metodi su
    questa classe (es. `_nuovo`, `_modifica`, `_salva`, `_aggiorna`, etc.).

    Questo controller usa `Merceologia` come modello dati.
    """

    ATTRIBUTI = [
        "Mostra nel modulo Inventario",
        "Mostra nel Tab Tagli",
        "Mostra nel Tab ingredienti base",
    ]

    def __init__(self):
        super().__init__()

        self.item = ""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        # Connessione al DB
        self.conn = get_connection()
        self.c = self.conn.cursor()

        # Cache dataset completo (usata anche per popolare la UI)
        self.dati_merceologie_totali = []
        self._carica_cache()

        # GUI build
        build_ui(self)

        # Popola tree
        self._aggiorna()

    def _carica_cache(self):
        self.dati_merceologie_totali = Merceologia.fetch_all(self.c)

    def _aggiorna(self):
        self.tree_elenco.delete(*self.tree_elenco.get_children())

        # Svuota il filtro all'aggiornamento dei dati generali
        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        # Preferisco cache per performance, ma se vuoi sempre freschezza possiamo fare fetch_all qui.
        self._carica_cache()

        for m in self.dati_merceologie_totali:
            self.tree_elenco.insert(
                "",
                "end",
                values=(m.id, m.merceologia, m.id_reparto),
            )

        # Mantenere reparti combobox coerente
        if hasattr(self, "cmb_box_reparto"):
            self._carica_reparti_combobox()

    def _filtra_merceologia(self, event=None):
        """Filtra gli elementi della Treeview in base al testo digitato nella Entry."""
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        testo_ricerca = self.entry_filtro.get().lower()

        self.tree_elenco.delete(*self.tree_elenco.get_children())

        if not hasattr(self, "dati_merceologie_totali"):
            return

        for m in self.dati_merceologie_totali:
            if testo_ricerca in str(m.merceologia).lower() or testo_ricerca in str(m.id):
                self.tree_elenco.insert(
                    "",
                    "end",
                    values=(m.id, m.merceologia, m.id_reparto),
                )

    def _reset_ricerca(self):
        """Svuota il filtro, ripristina la lista completa e pulisce i dettagli."""
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        if self.tree_elenco.selection():
            self.tree_elenco.selection_remove(self.tree_elenco.selection())

        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        self.tree_elenco.delete(*self.tree_elenco.get_children())

        if hasattr(self, "dati_merceologie_totali"):
            for m in self.dati_merceologie_totali:
                self.tree_elenco.insert(
                    "",
                    "end",
                    values=(m.id, m.merceologia, m.id_reparto),
                )

        # Pulisce dettagli a destra
        self.ent_merceologia.configure(state="normal")
        self.ent_merceologia.delete(0, "end")
        self.cmb_box_reparto_value.set("")

        for a in self.ATTRIBUTI:
            if a in self.valore_flag:
                self.valore_flag[a].set(0)

        self._disabilita_campi()


    def _carica_reparti_combobox(self):
        # Carica valori testo 'reparto' e non id: come nell'old.
        lista_reparti = []
        self.c.execute("SELECT reparto FROM reparti")
        for row in self.c:
            lista_reparti.extend(row)
        self.cmb_box_reparto["values"] = lista_reparti

    def _seleziona_per_popolamento(self):
        sel = self.tree_elenco.selection()
        if not sel:
            return None
        values = self.tree_elenco.item(sel[0], "values")
        if not values:
            return None
        # values: (id, merceologia, id_reparto) oppure (id, merceologia, reparto_testo)
        m_id = int(values[0])
        m = next((r for r in self.dati_merceologie_totali if r.id == m_id), None)
        if m is None:
            m = Merceologia.find_by_id(self.c, m_id)
        self.item = values
        return m

    def _onsingleclick(self, event=None):
        # Se l'utente sta scrivendo (Nuovo o Modifica), blocca gli eventi della tabella ---
        if getattr(self, 'modalita_inserimento', False) or getattr(self, 'modalita_modifica', False):
            return

        # Recupera la riga selezionata nel Treeview
        sel = self.tree_elenco.selection()
        if not sel:
            return

        # Sblocca temporaneamente i campi per consentire la scrittura via codice ---
        self.ent_merceologia.configure(state="normal")
        self.cmb_box_reparto.configure(state="normal")

        # Reset completo dei campi della UI grafica
        self.ent_merceologia.delete(0, "end")
        self.cmb_box_reparto_value.set("")

        # Estrae i valori visibili della riga
        self.item = self.tree_elenco.item(sel[0], "values")
        m_id = int(self.item[0])

        # Cerca l'oggetto direttamente nella cache locale
        m = next((r for r in self.dati_merceologie_totali if r.id == m_id), None)

        # Se per qualsiasi motivo non è in cache, usa il metodo di classe sul DB
        if not m:
            m = Merceologia.find_by_id(self.c, m_id)

        if not m:
            return

        # Popola l'interfaccia grafica leggendo le proprietà dell'oggetto
        self.ent_merceologia.insert(0, m.merceologia)

        # La UI usa 'reparto' testuale.
        # Delego la conversione a `Reparto` (anag_reparti/reparto.py) invece della query locale.
        from anag_reparti.reparto import Reparto

        reparto = Reparto.find_by_id(self.c, m.id_reparto)
        self.cmb_box_reparto_value.set(reparto.reparto if reparto else "")


        self.valore_flag[self.ATTRIBUTI[0]].set(m.flag1_inv)

        self.valore_flag[self.ATTRIBUTI[1]].set(m.flag2_taglio)
        self.valore_flag[self.ATTRIBUTI[2]].set(m.flag3_ing_base)

        # Blocca nuovamente i campi in modalità sola lettura dopo il popolamento ---
        self._disabilita_campi()

    def _disabilita_campi(self):
        self.modalita_inserimento = False
        self.modalita_modifica = False

        self.ent_merceologia.configure(state="disabled")
        self.cmb_box_reparto.configure(state="disabled")
        for a in self.ATTRIBUTI:
            self.ckbutton[a].configure(state="disabled")

        # Pulsanti principali
        if hasattr(self, "btn_nuovo"):
            self.btn_nuovo.configure(state="normal")
        if hasattr(self, "btn_modifica"):
            self.btn_modifica.configure(state="normal")
        if hasattr(self, "btn_elimina"):
            self.btn_elimina.configure(state="normal")

        # Pulsanti salvataggio / annulla
        if hasattr(self, "btn_salva"):
            self.btn_salva.configure(state="disabled")
        if hasattr(self, "btn_annulla"):
            self.btn_annulla.configure(state="disabled")

    def _abilita_campi(self):
        self.ent_merceologia.configure(state="normal")
        self.cmb_box_reparto.configure(state="normal")
        for a in self.ATTRIBUTI:
            self.ckbutton[a].configure(state="normal")

        if hasattr(self, "btn_nuovo"):
            self.btn_nuovo.configure(state="disabled")
        if hasattr(self, "btn_modifica"):
            self.btn_modifica.configure(state="disabled")
        if hasattr(self, "btn_elimina"):
            self.btn_elimina.configure(state="disabled")

        if hasattr(self, "btn_salva"):
            self.btn_salva.configure(state="normal")
        if hasattr(self, "btn_annulla"):
            self.btn_annulla.configure(state="normal")

    def _nuovo(self):
        self.modalita_inserimento = True
        self.modalita_modifica = False

        # Deseleziona eventuale record
        if self.tree_elenco.selection():
            self.tree_elenco.selection_remove(self.tree_elenco.selection())
        self.item = ""

        # Pulisci campi e abilita scrittura
        self.ent_merceologia.configure(state="normal")
        self.ent_merceologia.delete(0, "end")
        self.cmb_box_reparto_value.set("")
        for a in self.ATTRIBUTI:
            self.valore_flag[a].set(0)

        # Abilita modalità inserimento
        self._abilita_campi()

    def _modifica(self):
        m = self._seleziona_per_popolamento()
        if not m:
            messagebox.showinfo("Attenzione", "Seleziona una merceologia per poterla modificare.")
            return

        self.modalita_modifica = True
        self.modalita_inserimento = False

        self._abilita_campi()

    def _salva(self):
        rep_text = self.cmb_box_reparto_value.get().strip()
        merc_text = self.ent_merceologia.get().strip()

        if not merc_text or not rep_text:
            messagebox.showinfo("ATTENZIONE", "CI SONO CAMPI VUOTI")
            return

        self.c.execute("SELECT id FROM reparti WHERE reparto = %s", (rep_text,))
        row = self.c.fetchone()
        if not row:
            messagebox.showwarning("Attenzione", "Reparto non valido.")
            return
        id_reparto = row[0]

        flag1 = self.valore_flag[self.ATTRIBUTI[0]].get()
        flag2 = self.valore_flag[self.ATTRIBUTI[1]].get()
        flag3 = self.valore_flag[self.ATTRIBUTI[2]].get()

        try:
            if self.modalita_inserimento:
                m = Merceologia(
                    id=None,
                    merceologia=merc_text,
                    id_reparto=id_reparto,
                    flag1_inv=flag1,
                    flag2_taglio=flag2,
                    flag3_ing_base=flag3,
                )
                m.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuova merceologia inserita.")

            elif self.modalita_modifica:
                if not self.item:
                    # fallback da treeview
                    m = self._seleziona_per_popolamento()
                    if not m:
                        return
                    m_id = int(self.item[0])
                else:
                    m_id = int(self.item[0])

                m = Merceologia(
                    id=m_id,
                    merceologia=merc_text,
                    id_reparto=id_reparto,
                    flag1_inv=flag1,
                    flag2_taglio=flag2,
                    flag3_ing_base=flag3,
                )
                m.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Merceologia aggiornata.")

        finally:
            self.modalita_inserimento = False
            self.modalita_modifica = False
            self._aggiorna()
            self._disabilita_campi()

    def _annulla(self):
        self.modalita_inserimento = False
        self.modalita_modifica = False

        # Se c'è selezione, ripopola con i dati originali
        m = self._seleziona_per_popolamento()
        self.ent_merceologia.configure(state="normal")
        self.ent_merceologia.delete(0, "end")

        if m:
            self.ent_merceologia.insert(0, m.merceologia)

            try:
                # UI usa reparto testuale
                self.cmb_box_reparto_value.set("")
                self.c.execute("SELECT reparto FROM reparti WHERE id = %s", (m.id_reparto,))
                row = self.c.fetchone()
                self.cmb_box_reparto_value.set(row[0] if row else "")
            except Exception:
                self.cmb_box_reparto_value.set("")

            self.valore_flag[self.ATTRIBUTI[0]].set(m.flag1_inv)
            self.valore_flag[self.ATTRIBUTI[1]].set(m.flag2_taglio)
            self.valore_flag[self.ATTRIBUTI[2]].set(m.flag3_ing_base)

        self._disabilita_campi()

    def _elimina(self):
        m = self._seleziona_per_popolamento()
        if not m:
            messagebox.showinfo("Attenzione", "Seleziona una merceologia per poterla eliminare.")
            return

        conferma = messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente:\n'{m.merceologia}'?",
        )
        if not conferma:
            return

        try:
            m.delete(self.c, self.conn)
            messagebox.showinfo("Successo", "Merceologia eliminata.")
        finally:
            self._aggiorna()
            self._disabilita_campi()


    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)

