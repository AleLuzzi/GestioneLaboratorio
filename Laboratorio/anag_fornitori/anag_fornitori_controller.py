import tkinter as tk
from tkinter import messagebox

import mysql.connector

from db import get_connection, close_connection
from anag_fornitori.anag_fornitori_TKinter import setup_window, build_ui
from anag_fornitori.fornitore import Fornitore


class AnagFornitoriController(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.item = ""
        self.modalita_inserimento = False
        self.modalita_modifica = False
        setup_window(self)
        
        self.conn = get_connection()
        self.c = self.conn.cursor()

        build_ui(self)
    
    def _nuovo(self):
        """Prepara l'interfaccia principale per l'inserimento di un nuovo fornitore."""
        self.modalita_inserimento = True  # Attiva lo stato di inserimento nuovo record
        
        # Deseleziona qualsiasi riga precedentemente cliccata nella tabella per chiarezza visiva
        self.tree_fornitori.selection_remove(self.tree_fornitori.selection())

        # Sblocca temporaneamente i campi per consentire la pulizia e la scrittura
        self.ent_azienda.configure(state="normal")
        self.ckbtn_ing_merce.configure(state="normal")
        self.ckbtn_inv.configure(state="normal")

        # Resetta completamente i campi grafici per accogliere il nuovo testo
        self.ent_azienda.delete(0, "end")
        self.valore_flag_ing_merce.set(0)
        self.valore_flag_inv.set(0)

        # Gestione Pulsanti: Spegne Nuovo, Modifica ed Elimina
        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

        # Gestione Pulsanti: Accende Salva e Annulla
        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")


    def _modifica(self):
        """Abilita i campi di inserimento e i pulsanti di gestione dati."""
        # Verifica di sicurezza: l'utente deve aver selezionato qualcosa prima di modificare
        if not self.tree_fornitori.selection():
            messagebox.showinfo("Attenzione", "Seleziona un fornitore dall'elenco per poterlo modificare.")
            return
        
        self.modalita_modifica = True

        # Abilita i campi di input grafici
        self.ent_azienda.configure(state="normal")
        self.ckbtn_ing_merce.configure(state="normal")
        self.ckbtn_inv.configure(state="normal")

        # Gestione Pulsanti: Disabilita la possibilità di fare altre azioni core
        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")

        # Gestione Pulsanti: Abilita i controlli di salvataggio/annullamento
        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")
        self.btn_elimina.configure(state="normal")

    def _disabilita_campi(self):
        """Riporta l'interfaccia allo stato iniziale di blocco (sola lettura)."""
        self.modalita_inserimento = False  # Reset sicurezza
        self.modalita_modifica = False     # Reset sicurezza

        # Disabilita i widget di testo e scelta
        self.ent_azienda.configure(state="disabled")
        self.ckbtn_ing_merce.configure(state="disabled")
        self.ckbtn_inv.configure(state="disabled")

        # Ripristina lo stato dei bottoni principali
        self.btn_nuovo.configure(state="normal")
        self.btn_modifica.configure(state="normal")
        
        # Blocca nuovamente i bottoni di gestione
        self.btn_salva.configure(state="disabled")
        self.btn_annulla.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

    def _annulla(self):
        """Annulla le modifiche correnti ripristinando i dati originali e blocca la UI."""
        self.modalita_inserimento = False  # Annulla l'operazione di creazione corrente
        self.modalita_modifica = False

        # Recupera la selezione corrente della tabella
        sel = self.tree_fornitori.selection()
        
        if sel:
            # Forziamo temporaneamente lo stato normal sui campi altrimenti 
            # i metodi .delete() e .insert() verrebbero ignorati da Tkinter
            self.ent_azienda.configure(state="normal")
            self.ckbtn_ing_merce.configure(state="normal")
            self.ckbtn_inv.configure(state="normal")

            # Svuota i campi grafici
            self.ent_azienda.delete(0, "end")
            self.valore_flag_ing_merce.set(0)
            self.valore_flag_inv.set(0)

            # Estrae l'ID dalla riga selezionata nel Treeview
            self.item = self.tree_fornitori.item(sel[0], "values")
            id_selezionato = int(self.item[0])

            # Recupera l'oggetto originale dalla cache in memoria (senza rieseguire la query SQL)
            fornitore = next((f for f in self.dati_fornitori_totali if f.id == id_selezionato), None)
            
            # Se presente ripopola i campi con lo stato originale pre-modifica
            if fornitore:
                self.ent_azienda.insert(0, fornitore.azienda)
                if fornitore.flag1_ing_merce == 1:
                    self.valore_flag_ing_merce.set(1)
                if fornitore.flag2_inventario == 1:
                    self.valore_flag_inv.set(1)

        else:
            # Se l'utente clicca Annulla senza una riga selezionata (es. dopo anomalie), pulisce e basta
            self.ent_azienda.configure(state="normal")
            self.ent_azienda.delete(0, "end")
            self.valore_flag_ing_merce.set(0)
            self.valore_flag_inv.set(0)

        # 2. Ripristina lo stato di blocco dei widget e l'attivazione dei pulsanti corretti
        self._disabilita_campi()

    def _salva(self):
        # Valida che il nome azienda sia stato digitato (Rimuove spazi vuoti iniziali/finali)
        nome_azienda = self.ent_azienda.get().strip()
        if not nome_azienda:
            messagebox.showwarning("Attenzione", "Il campo Ragione sociale è obbligatorio.")
            return

        try:
            if self.modalita_inserimento:
                # --- CASO A: INSERIMENTO NUOVO FORNITORE ---
                nuovo_fornitore = Fornitore(
                    id=None,  # L'ID viene autogenerato dal Database (Auto-increment)
                    azienda=nome_azienda,
                    flag1_ing_merce=self.valore_flag_ing_merce.get(),
                    flag2_inventario=self.valore_flag_inv.get()
                )
                nuovo_fornitore.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuovo fornitore inserito con successo.")
            
            else:
                # --- CASO B: MODIFICA FORNITORE ESISTENTE ---
                sel = self.tree_fornitori.selection()
                if not sel:
                    messagebox.showinfo("Attenzione", "Nessun record selezionato per la modifica.")
                    return
                
                self.item = self.tree_fornitori.item(sel[0], "values")
                id_fornitore = int(self.item[0])

                fornitore_modificato = Fornitore(
                    id=id_fornitore,
                    azienda=nome_azienda,
                    flag1_ing_merce=self.valore_flag_ing_merce.get(),
                    flag2_inventario=self.valore_flag_inv.get()
                )
                fornitore_modificato.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Dati del fornitore aggiornati con successo.")

            # --- OPERAZIONI DI CONCLUSIONE (COMUNI A ENTRAMBI I CASI) ---
            self.modalita_inserimento = False  # Resetta lo stato logico iniziale
            self._aggiorna()                   # Aggiorna la Treeview includendo le novità
            self._disabilita_campi()           # Ri-blocca l'interfaccia grafica in sola lettura

        except mysql.connector.Error as e:
            messagebox.showerror("Database", f"Errore durante l'operazione: {e}")

    def _aggiorna(self):
        # Svuota la Treeview usando self
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        
        # Svuota la barra di ricerca all'aggiornamento dei dati generali
        if hasattr(self, 'entry_filtro'):
            self.entry_filtro.delete(0, "end")
        
        # Richiamo del metodo centralizzato nella classe Fornitore
        self.dati_fornitori_totali = Fornitore.fetch_all(self.c)
        
        for fornitore in self.dati_fornitori_totali:
           self.tree_fornitori.insert("", "end", values=(fornitore.id, fornitore.azienda))

    def _elimina(self):
        """Elimina il fornitore selezionato previa conferma dell'utente."""
        # 1. Recupera la riga selezionata nel Treeview
        sel = self.tree_fornitori.selection()
        if not sel:
            messagebox.showinfo("Attenzione", "Nessun record selezionato per l'eliminazione.")
            return

        # 2. Estrae l'ID visibile nella riga
        self.item = self.tree_fornitori.item(sel, "values")
        id_selezionato = int(self.item[0])

        # 3. Recupera l'oggetto dalla cache in memoria per conoscerne il nome
        fornitore = next((f for f in self.dati_fornitori_totali if f.id == id_selezionato), None)
        nome_azienda = fornitore.azienda if fornitore else "questo fornitore"

        # 4. Finestra di dialogo per conferma di sicurezza (Evita cancellazioni accidentali)
        conferma = messagebox.askyesno(
            "Conferma Eliminazione", 
            f"Sei sicuro di voler eliminare definitivamente il fornitore:\n'{nome_azienda}'?"
        )
        
        if not conferma:
            return  # Se l'utente clicca 'No', interrompe l'operazione

        # 5. Se l'utente conferma, procede alla cancellazione tramite l'oggetto modello
        try:
            if not fornitore:
                # Fallback se non fosse presente in cache
                fornitore = Fornitore(id=id_selezionato)
                
            # Esegue la DELETE isolata nel modello
            fornitore.delete(self.c, self.conn)
            
            messagebox.showinfo("Successo", "Fornitore eliminato con successo.")
            
            # 6. Ripristino dello stato ottimale della UI
            self._aggiorna()          # Rinfresca la tabella svuotando il record cancellato
            self._disabilita_campi()  # Riporta i campi in sola lettura e resetta i pulsanti
            
            # Pulisce i campi di testo dai dati del fornitore appena rimosso
            self.ent_azienda.configure(state="normal")
            self.ent_azienda.delete(0, "end")
            self.valore_flag_ing_merce.set(0)
            self.valore_flag_inv.set(0)
            self.ent_azienda.configure(state="disabled")

        except mysql.connector.Error as e:
            messagebox.showerror("Errore Database", f"Impossibile eliminare il fornitore: {e}")


    def _filtra_aziende(self, event=None):
        """Filtra gli elementi della Treeview in base al testo digitato nella Entry."""
        # Recupera il testo digitato direttamente dalla Entry usando self
        testo_ricerca = self.entry_filtro.get().lower()
        
        # Svuota momentaneamente la Treeview per aggiornare l'elenco visivo
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        
        # Sicurezza: se la lista in memoria non esiste ancora, esce
        if not hasattr(self, 'dati_fornitori_totali'):
            return

        for fornitore in self.dati_fornitori_totali:
            if testo_ricerca in str(fornitore.azienda).lower() or testo_ricerca in str(fornitore.id):
                self.tree_fornitori.insert("", "end", values=(fornitore.id, fornitore.azienda))

    def _onsingleclick(self, event):
        # Se l'utente sta scrivendo (Nuovo o Modifica), blocca gli eventi della tabella ---
        if getattr(self, 'modalita_inserimento', False) or getattr(self, 'modalita_modifica', False):
            return

        # self.modalita_inserimento = False  # Se clicca una riga, interrompe lo stato di "Nuovo"
        # Recupera la riga selezionata nel Treeview
        sel = self.tree_fornitori.selection()
        if not sel:
            return

        # Sblocca temporaneamente i campi per consentire la scrittura via codice ---
        self.ent_azienda.configure(state="normal")
        self.ckbtn_ing_merce.configure(state="normal")
        self.ckbtn_inv.configure(state="normal")

        # Reset completo dei campi della UI grafica
        self.ent_azienda.delete(0, "end")
        self.valore_flag_ing_merce.set(0)
        self.valore_flag_inv.set(0)

        # Estrae i valori visibili della riga (il primo elemento è l'ID)
        self.item = self.tree_fornitori.item(sel[0], "values")
        id_selezionato = int(self.item[0])
        
        # Cerca l'oggetto direttamente nella cache locale 
        fornitore = next((f for f in self.dati_fornitori_totali if f.id == id_selezionato), None)
        
        # Se per qualsiasi motivo non è in cache, usa il metodo di classe sul DB
        if not fornitore:
            fornitore = Fornitore.find_by_id(self.c, id_selezionato)
            
        if not fornitore:
            return

        # Popola l'interfaccia grafica leggendo le proprietà dell'oggetto
        self.ent_azienda.insert(0, fornitore.azienda)
        if fornitore.flag1_ing_merce == 1:
            self.valore_flag_ing_merce.set(1)
        if fornitore.flag2_inventario == 1:
            self.valore_flag_inv.set(1)
        
        # Blocca nuovamente i campi in modalità sola lettura dopo il popolamento ---
        self._disabilita_campi()

    def _reset_ricerca(self):
        """Svuota il filtro, ripristina la lista completa e pulisce i dettagli."""
        # 1. Sicurezza: blocca l'azione se l'utente sta inserendo o modificando dati
        if getattr(self, 'modalita_inserimento', False) or getattr(self, 'modalita_modifica', False):
            return

        # 2. Rimuove la selezione visiva corrente dalla Treeview (se presente)
        if self.tree_fornitori.selection():
            self.tree_fornitori.selection_remove(self.tree_fornitori.selection())

        # 3. Cancella il testo all'interno della Entry del filtro
        if hasattr(self, 'entry_filtro'):
            self.entry_filtro.delete(0, "end")
            
        # 4. Svuota la Treeview visiva per rigenerarla da zero
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        
        # 5. Ripopola l'elenco completo sfruttando i dati già in memoria
        if hasattr(self, 'dati_fornitori_totali'):
            for fornitore in self.dati_fornitori_totali:
                self.tree_fornitori.insert("", "end", values=(fornitore.id, fornitore.azienda))

        # 6. Pulisce e azzera completamente i widget di dettaglio a destra
        self.ent_azienda.configure(state="normal")
        self.ent_azienda.delete(0, "end")
        self.valore_flag_ing_merce.set(0)
        self.valore_flag_inv.set(0)
        
        # 7. Riporta i campi puliti allo stato iniziale di protezione (sola lettura)
        self._disabilita_campi()



    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == "__main__":
    root = tk.Tk()
    AnagFornitoriController()
    root.mainloop()
