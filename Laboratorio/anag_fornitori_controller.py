import tkinter as tk
from tkinter import messagebox

import mysql.connector

from db import get_connection, close_connection
from anag_fornitori_TKinter import setup_window, build_ui, show_insert_fornitore_dialog


class AnagFornitoriController(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.item = ""

        setup_window(self)

        self.conn = get_connection()
        self.c = self.conn.cursor()

        build_ui(self)

    def _inserisci(self):
        show_insert_fornitore_dialog(self)

    def _salva(self):
        sel = self.tree_fornitori.selection()
        if not sel:
            messagebox.showinfo("ATTENZIONE", "Non hai selezionato nessun record")
            return
        self.item = self.tree_fornitori.item(sel[0], "values")
        lista = [
            self.ent_azienda.get(),
            self.valore_flag_ing_merce.get(),
            self.valore_flag_inv.get(),
            self.item[0],
        ]
        try:
            self.c.execute(
                "UPDATE fornitori SET azienda = %s, flag1_ing_merce = %s, flag2_inventario = %s WHERE ID = %s",
                lista,
            )
            self.conn.commit()
            self._aggiorna()
        except mysql.connector.Error as e:
            messagebox.showerror("Database", str(e))

    '''
    def _aggiorna(self):
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        self.c.execute("SELECT ID, azienda FROM fornitori")
        for fid, azienda in self.c.fetchall():
            self.tree_fornitori.insert("", "end", values=(fid, azienda))
    '''
    def _aggiorna(self):
        # Svuota la Treeview usando self
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        
        # Svuota la barra di ricerca all'aggiornamento dei dati generali
        if hasattr(self, 'entry_filtro'):
            self.entry_filtro.delete(0, "end")
        
        # Esegue la query sul database
        self.c.execute("SELECT ID, azienda FROM fornitori")
        
        # Salva i record in una lista interna a questa istanza
        self.dati_fornitori_totali = self.c.fetchall()
        
        # Inserisce i dati estratti nella Treeview
        for fid, azienda in self.dati_fornitori_totali:
            self.tree_fornitori.insert("", "end", values=(fid, azienda))

    def _filtra_aziende(self, event=None):
        """Filtra gli elementi della Treeview in base al testo digitato nella Entry."""
        # Recupera il testo digitato direttamente dalla Entry usando self
        testo_ricerca = self.entry_filtro.get().lower()
        
        # Svuota momentaneamente la Treeview per aggiornare l'elenco visivo
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        
        # Sicurezza: se la lista in memoria non esiste ancora, esce
        if not hasattr(self, 'dati_fornitori_totali'):
            return

        # Cicla sulla lista salvata in memoria per ripopolare la Treeview
        for fid, azienda in self.dati_fornitori_totali:
            if testo_ricerca in str(azienda).lower() or testo_ricerca in str(fid):
                self.tree_fornitori.insert("", "end", values=(fid, azienda))


    def _onsingleclick(self, event):
        sel = self.tree_fornitori.selection()
        if not sel:
            return

        self.ent_azienda.delete(0, "end")
        self.valore_flag_ing_merce.set(0)
        self.valore_flag_inv.set(0)

        self.item = self.tree_fornitori.item(sel[0], "values")

        self.c.execute("SELECT * FROM fornitori WHERE ID = %s", (self.item[0],))
        row = self.c.fetchone()
        if not row:
            return
        self.ent_azienda.insert(0, row[1])
        if row[2] == 1:
            self.valore_flag_ing_merce.set(1)
        if row[3] == 1:
            self.valore_flag_inv.set(1)
    
    

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == "__main__":
    root = tk.Tk()
    AnagFornitoriController()
    root.mainloop()
