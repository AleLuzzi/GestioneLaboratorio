import tkinter as tk
from tkinter import messagebox

import mysql.connector

from anag_reparti.reparto import Reparto
from config import get_config

from anag_reparti.anag_reparti_TKinter import setup_window, build_ui
from db import get_connection, close_connection
from theme import COLORS


class Reparti(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.configure(bg=COLORS["bg_light"])
        self.item = ""
        self.modalita_inserimento = False
        self.modalita_modifica = False
        self.config = get_config()

        self.conn = get_connection()
        self.c = self.conn.cursor()

        build_ui(self)

    def _salva(self):
        nome_reparto = self.ent_reparto.get().strip()
        if not nome_reparto:
            messagebox.showwarning("Attenzione", "Il campo Reparto è obbligatorio.")
            return

        try:
            if self.modalita_inserimento:
                nuovo_reparto = Reparto(
                    id=None,
                    reparto=nome_reparto,
                    flag1_dip=self.valore_flag_dip.get(),
                    flag2_prod=self.valore_flag_prod.get(),
                )
                nuovo_reparto.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuovo reparto inserito con successo.")

            else:
                sel = self.tree_elenco.selection()
                if not sel:
                    messagebox.showinfo("Attenzione", "Nessun record selezionato per la modifica.")
                    return

                self.item = self.tree_elenco.item(sel[0], "values")
                id_reparto = int(self.item[0])

                reparto_modificato = Reparto(
                    id=id_reparto,
                    reparto=nome_reparto,
                    flag1_dip=self.valore_flag_dip.get(),
                    flag2_prod=self.valore_flag_prod.get(),
                )
                reparto_modificato.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Dati del reparto aggiornati con successo.")

            self.modalita_inserimento = False
            self._aggiorna()
            self._disabilita_campi()

        except mysql.connector.Error as e:
            messagebox.showerror("Database", f"Errore durante l'operazione: {e}")

    def _annulla(self):
        """Annulla le modifiche correnti ripristinando i dati originali e blocca la UI."""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        sel = self.tree_elenco.selection()

        if sel:
            self.ent_reparto.configure(state="normal")
            self.ckbtn_dip.configure(state="normal")
            self.ckbtn_prod.configure(state="normal")

            self.ent_reparto.delete(0, "end")
            self.valore_flag_dip.set(0)
            self.valore_flag_prod.set(0)

            self.item = self.tree_elenco.item(sel[0], "values")
            id_selezionato = int(self.item[0])

            reparto = next((r for r in self.dati_reparti_totali if r.id == id_selezionato), None)

            if reparto:
                self.ent_reparto.insert(0, reparto.reparto)
                if reparto.flag1_dip == 1:
                    self.valore_flag_dip.set(1)
                if reparto.flag2_prod == 1:
                    self.valore_flag_prod.set(1)

        else:
            self.ent_reparto.configure(state="normal")
            self.ent_reparto.delete(0, "end")
            self.valore_flag_dip.set(0)
            self.valore_flag_prod.set(0)

        self._disabilita_campi()

    def _elimina(self):
        """Elimina il reparto selezionato previa conferma dell'utente."""
        sel = self.tree_elenco.selection()
        if not sel:
            messagebox.showinfo("Attenzione", "Nessun record selezionato per l'eliminazione.")
            return

        self.item = self.tree_elenco.item(sel, "values")
        id_selezionato = int(self.item[0])

        reparto = next((r for r in self.dati_reparti_totali if r.id == id_selezionato), None)
        nome_reparto = reparto.reparto if reparto else "questo reparto"

        conferma = messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente il reparto:\n'{nome_reparto}'?",
        )

        if not conferma:
            return

        try:
            if not reparto:
                reparto = Reparto(id=id_selezionato)

            reparto.delete(self.c, self.conn)

            messagebox.showinfo("Successo", "Reparto eliminato con successo.")

            self._aggiorna()
            self._disabilita_campi()

            self.ent_reparto.configure(state="normal")
            self.ent_reparto.delete(0, "end")
            self.valore_flag_dip.set(0)
            self.valore_flag_prod.set(0)
            self.ent_reparto.configure(state="disabled")

        except mysql.connector.Error as e:
            messagebox.showerror("Errore Database", f"Impossibile eliminare il reparto: {e}")

    def _aggiorna(self):
        self.tree_elenco.delete(*self.tree_elenco.get_children())

        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        self.dati_reparti_totali = Reparto.fetch_all(self.c)

        for reparto in self.dati_reparti_totali:
            self.tree_elenco.insert("", "end", values=(reparto.id, reparto.reparto))

    def _nuovo(self):
        """Prepara l'interfaccia principale per l'inserimento di un nuovo reparto."""
        self.modalita_inserimento = True

        self.tree_elenco.selection_remove(self.tree_elenco.selection())

        self.ent_reparto.configure(state="normal")
        self.ckbtn_dip.configure(state="normal")
        self.ckbtn_prod.configure(state="normal")

        self.ent_reparto.delete(0, "end")
        self.valore_flag_dip.set(0)
        self.valore_flag_prod.set(0)

        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")

    def _modifica(self):
        """Abilita i campi di inserimento e i pulsanti di gestione dati."""
        if not self.tree_elenco.selection():
            messagebox.showinfo("Attenzione", "Seleziona un reparto dall'elenco per poterlo modificare.")
            return

        self.modalita_modifica = True

        self.ent_reparto.configure(state="normal")
        self.ckbtn_dip.configure(state="normal")
        self.ckbtn_prod.configure(state="normal")

        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")

        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")
        self.btn_elimina.configure(state="normal")

    def _disabilita_campi(self):
        """Riporta l'interfaccia allo stato iniziale di blocco (sola lettura)."""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        self.ent_reparto.configure(state="disabled")
        self.ckbtn_dip.configure(state="disabled")
        self.ckbtn_prod.configure(state="disabled")

        self.btn_nuovo.configure(state="normal")
        self.btn_modifica.configure(state="normal")

        self.btn_salva.configure(state="disabled")
        self.btn_annulla.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

    def _onsingleclick(self, event):
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        sel = self.tree_elenco.selection()
        if not sel:
            return

        self.ent_reparto.configure(state="normal")
        self.ckbtn_dip.configure(state="normal")
        self.ckbtn_prod.configure(state="normal")

        self.ent_reparto.delete(0, "end")
        self.valore_flag_dip.set(0)
        self.valore_flag_prod.set(0)

        self.item = self.tree_elenco.item(sel[0], "values")
        id_selezionato = int(self.item[0])

        reparto = next((r for r in self.dati_reparti_totali if r.id == id_selezionato), None)

        if not reparto:
            reparto = Reparto.find_by_id(self.c, id_selezionato)

        if not reparto:
            return

        self.ent_reparto.insert(0, reparto.reparto)
        if reparto.flag1_dip == 1:
            self.valore_flag_dip.set(1)
        if reparto.flag2_prod == 1:
            self.valore_flag_prod.set(1)

        self._disabilita_campi()

    def _filtra_reparto(self, event=None):
        """Filtra gli elementi della Treeview in base al testo digitato nella Entry."""
        testo_ricerca = self.entry_filtro.get().lower()

        self.tree_elenco.delete(*self.tree_elenco.get_children())

        if not hasattr(self, "dati_reparti_totali"):
            return

        for reparto in self.dati_reparti_totali:
            if testo_ricerca in str(reparto.reparto).lower() or testo_ricerca in str(reparto.id):
                self.tree_elenco.insert("", "end", values=(reparto.id, reparto.reparto))

    def _reset_ricerca(self):
        """Svuota il filtro, ripristina la lista completa e pulisce i dettagli."""
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        if self.tree_elenco.selection():
            self.tree_elenco.selection_remove(self.tree_elenco.selection())

        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        self.tree_elenco.delete(*self.tree_elenco.get_children())

        if hasattr(self, "dati_reparti_totali"):
            for reparto in self.dati_reparti_totali:
                self.tree_elenco.insert("", "end", values=(reparto.id, reparto.reparto))

        self.ent_reparto.configure(state="normal")
        self.ent_reparto.delete(0, "end")
        self.valore_flag_dip.set(0)
        self.valore_flag_prod.set(0)

        self._disabilita_campi()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == "__main__":
    root = tk.Tk()
    Reparti()
    root.mainloop()
