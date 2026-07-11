import tkinter as tk
from tkinter import messagebox

import mysql.connector

from db import get_connection, close_connection
from anag_tagli.anag_tagli_Tkinter import setup_window, build_ui
from anag_tagli.tagli import Taglio


class AnagTagliController(tk.Toplevel):
    def __init__(self):
        super().__init__()

        # stato
        self.item = ""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        # Connessione DB
        self.conn = get_connection()
        self.c = self.conn.cursor()

        # UI
        setup_window(self)
        build_ui(self)

        # abilita primo aggiornamento dati (se UI non chiama _aggiorna)
        if hasattr(self, "_aggiorna"):
            self._aggiorna()

    def _nuovo(self):
        self.modalita_inserimento = True
        self.modalita_modifica = False

        # deselect
        if self.tree_tagli.selection():
            self.tree_tagli.selection_remove(self.tree_tagli.selection())

        # sblocca
        self.entry_taglio.configure(state="normal")
        self.ent_merceologia.configure(state="normal")

        # checkbox
        self.ckbtn_in_inventario.configure(state="normal")

        # reset campi
        self.entry_taglio.delete(0, "end")
        self.ent_merceologia.set("")
        self.valori_in_inventario.set(0)

        # pulsanti
        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")
        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")

    def _modifica(self):
        if not self.tree_tagli.selection():
            messagebox.showinfo("Attenzione", "Seleziona un taglio dall'elenco per poterlo modificare.")
            return

        self.modalita_modifica = True
        self.modalita_inserimento = False

        self.entry_taglio.configure(state="normal")
        self.ent_merceologia.configure(state="normal")
        self.ckbtn_in_inventario.configure(state="normal")

        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")
        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")
        self.btn_elimina.configure(state="normal")

    def _disabilita_campi(self):
        self.modalita_inserimento = False
        self.modalita_modifica = False

        self.entry_taglio.configure(state="disabled")
        self.ent_merceologia.configure(state="disabled")
        self.ckbtn_in_inventario.configure(state="disabled")

        self.btn_nuovo.configure(state="normal")
        self.btn_modifica.configure(state="normal")
        self.btn_salva.configure(state="disabled")
        self.btn_annulla.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

    def _annulla(self):
        self.modalita_inserimento = False
        self.modalita_modifica = False

        sel = self.tree_tagli.selection()

        # Ripristina dati selezionati (se esiste)
        if sel:
            self.item = self.tree_tagli.item(sel[0], "values")
            id_selezionato = int(self.item[0])

            taglio = next((r for r in self.dati_tagli_totali if r.id == id_selezionato), None)
            if not taglio:
                taglio = Taglio.find_by_id(self.c, id_selezionato)

            if taglio:
                self.entry_taglio.delete(0, "end")
                self.entry_taglio.insert(0, getattr(taglio, "taglio", ""))

                # ripristino combobox merceologia: serve convertire id -> testo
                if hasattr(self, "_map_merceologia_id_to_name"):
                    name = self._map_merceologia_id_to_name.get(getattr(taglio, "id_merceologia", None), "")
                else:
                    name = ""
                self.ent_merceologia.set(name)

                # flag inventario non presente nel modello tagli.py -> lo lasciamo a 0 (compat)
                self.valori_in_inventario.set(0)

        # rimpone stato
        self._disabilita_campi()

    def _salva(self):
        taglio_desc = self.entry_taglio.get().strip()
        merceologia_sel = self.ent_merceologia.get().strip()

        if not taglio_desc:
            messagebox.showwarning("Attenzione", "Il campo Taglio è obbligatorio.")
            return

        if not merceologia_sel:
            messagebox.showwarning("Attenzione", "Seleziona una Merceologia.")
            return

        # mappa nome -> id
        if not hasattr(self, "_map_merceologia_name_to_id"):
            self._carica_merceologie()

        id_merceologia = self._map_merceologia_name_to_id.get(merceologia_sel)
        if not id_merceologia:
            messagebox.showerror("Errore", "Merceologia non valida.")
            return

        flag_inventario = int(getattr(self.valori_in_inventario, "get", lambda: 0)())

        try:
            if self.modalita_inserimento:
                nuovo = Taglio(id=None, taglio=taglio_desc, id_merceologia=id_merceologia)
                nuovo.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuovo taglio inserito con successo.")

            else:
                sel = self.tree_tagli.selection()
                if not sel:
                    messagebox.showinfo("Attenzione", "Nessun record selezionato per la modifica.")
                    return

                self.item = self.tree_tagli.item(sel[0], "values")
                id_selezionato = int(self.item[0])

                aggiornato = Taglio(id=id_selezionato, taglio=taglio_desc, id_merceologia=id_merceologia)
                aggiornato.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Dati del taglio aggiornati con successo.")

            # Aggiorna & blocca
            self.modalita_inserimento = False
            self.modalita_modifica = False
            self._aggiorna()
            self._disabilita_campi()

        except mysql.connector.Error as e:
            messagebox.showerror("Database", f"Errore durante l'operazione: {e}")

    def _aggiorna(self):
        # aggiorna combobox merceologie
        self._carica_merceologie()

        self.tree_tagli.delete(*self.tree_tagli.get_children())

        self.dati_tagli_totali = Taglio.fetch_all(self.c)

        for t in self.dati_tagli_totali:
            # per la colonna Merceologia usiamo nome (id -> nome)
            nome_merc = self._map_merceologia_id_to_name.get(getattr(t, "id_merceologia", None), "")
            self.tree_tagli.insert("", "end", values=(t.id, t.taglio, nome_merc))

    def _carica_merceologie(self):
        # popola combobox merceologie e costruisce mapping id<->name
        if not hasattr(self, "_map_merceologia_name_to_id"):
            self._map_merceologia_name_to_id = {}
            self._map_merceologia_id_to_name = {}

        # Non ricaricare in loop se già fatto, ma è ok ricaricare semplice
        self.c.execute("SELECT id, merceologia FROM merceologie")
        rows = self.c.fetchall()

        self._map_merceologia_name_to_id.clear()
        self._map_merceologia_id_to_name.clear()

        values = []
        for (mid, mname) in rows:
            self._map_merceologia_name_to_id[mname] = mid
            self._map_merceologia_id_to_name[mid] = mname
            values.append(mname)

        # imposta UI combobox
        if hasattr(self, "box_merceologia"):
            self.box_merceologia["values"] = values

    def _elimina(self):
        sel = self.tree_tagli.selection()
        if not sel:
            messagebox.showinfo("Attenzione", "Nessun record selezionato per l'eliminazione.")
            return

        self.item = self.tree_tagli.item(sel[0], "values")
        id_selezionato = int(self.item[0])

        taglio = next((r for r in self.dati_tagli_totali if r.id == id_selezionato), None)
        nome_taglio = getattr(taglio, "taglio", "questo taglio") if taglio else "questo taglio"

        if not messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente il taglio:\n'{nome_taglio}'?",
        ):
            return

        try:
            if not taglio:
                taglio = Taglio(id=id_selezionato)

            taglio.delete(self.c, self.conn)
            messagebox.showinfo("Successo", "Taglio eliminato con successo.")

            self._aggiorna()
            self._disabilita_campi()

            self.entry_taglio.configure(state="normal")
            self.entry_taglio.delete(0, "end")
            self.ent_merceologia.configure(state="normal")
            self.ent_merceologia.set("")
            self.ckbtn_in_inventario.configure(state="normal")
            self.valori_in_inventario.set(0)
            self._disabilita_campi()

        except mysql.connector.Error as e:
            messagebox.showerror("Errore Database", f"Impossibile eliminare il taglio: {e}")

    def _reset_ricerca(self):
        """Svuota il filtro e ripristina l'elenco completo dei tagli.

        Copiato come logica dal pattern presente in AnagIngredientiController.
        """
        # se l'utente sta inserendo/modificando, non cambiare la tabella
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        # deselect
        if self.tree_tagli.selection():
            self.tree_tagli.selection_remove(self.tree_tagli.selection())

        # reset testo filtro
        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        # reset tabella (usa la cache se disponibile, evitando roundtrip extra)
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        if hasattr(self, "dati_tagli_totali"):
            for t in self.dati_tagli_totali:
                nome_merc = self._map_merceologia_id_to_name.get(getattr(t, "id_merceologia", None), "")
                self.tree_tagli.insert("", "end", values=(t.id, t.taglio, nome_merc))

        # reset campi dettaglio
        self.entry_taglio.configure(state="normal")
        self.entry_taglio.delete(0, "end")
        self.ent_merceologia.configure(state="normal")
        self.ent_merceologia.delete(0, "end")
        self.valori_in_inventario.set(0)

        self._disabilita_campi()


    def _filtra_tagli(self, event=None):
        testo = self.entry_filtro.get().lower().strip()
        self.tree_tagli.delete(*self.tree_tagli.get_children())

        if not hasattr(self, "dati_tagli_totali"):
            return

        for t in self.dati_tagli_totali:
            nome_merc = self._map_merceologia_id_to_name.get(getattr(t, "id_merceologia", None), "")
            if (
                testo in str(t.id).lower()
                or testo in str(getattr(t, "taglio", "")).lower()
                or testo in str(nome_merc).lower()
            ):
                self.tree_tagli.insert("", "end", values=(t.id, t.taglio, nome_merc))


    def _onsingleclick(self, event):
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        sel = self.tree_tagli.selection()
        if not sel:
            return

        # sblocca temporaneamente per scrittura
        self.entry_taglio.configure(state="normal")
        self.ent_merceologia.configure(state="normal")
        self.ckbtn_in_inventario.configure(state="normal")

        self.entry_taglio.delete(0, "end")

        self.item = self.tree_tagli.item(sel[0], "values")
        id_selezionato = int(self.item[0])

        taglio = next((r for r in self.dati_tagli_totali if r.id == id_selezionato), None)
        if not taglio:
            taglio = Taglio.find_by_id(self.c, id_selezionato)
        if not taglio:
            return

        self.entry_taglio.insert(0, getattr(taglio, "taglio", ""))

        nome_merc = self._map_merceologia_id_to_name.get(getattr(taglio, "id_merceologia", None), "")
        self.ent_merceologia.set(nome_merc)

        # flag inventario non gestito dal modello: set default
        self.valori_in_inventario.set(0)

        self._disabilita_campi()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == "__main__":
    root = tk.Tk()
    AnagTagliController()
    root.mainloop()

