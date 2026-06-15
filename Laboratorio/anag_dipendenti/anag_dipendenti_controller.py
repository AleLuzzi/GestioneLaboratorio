import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from dipendente import Dipendente
from config import get_config

from anag_dipendenti_TKinter import setup_window, build_ui
from db import get_connection, close_connection
from theme import COLORS, get_font


class Dipendenti(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.configure(bg=COLORS["bg_light"])
        self.item = ''
        self.modalita_inserimento = False
        self.modalita_modifica = False
        self.config = get_config()

        # Connessione al Database
        self.conn = get_connection()
        self.c = self.conn.cursor()

        build_ui(self)
       
    def _salva(self):
        # Valida che il nome dipendente sia stato digitato (Rimuove spazi vuoti iniziali/finali)
        nome_dipendente = self.ent_dipendente.get().strip()
        if not nome_dipendente:
            messagebox.showwarning("Attenzione", "Il campo Nome è obbligatorio.")
            return

        try:
            if self.modalita_inserimento:
                # --- CASO A: INSERIMENTO NUOVO DIPENDENTE ---
                nuovo_dipendente = Dipendente(
                    id=None,  # L'ID viene autogenerato dal Database (Auto-increment)
                    nome=nome_dipendente,
                   
                )
                nuovo_dipendente.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuovo dipendente inserito con successo.")
            
            else:
                # --- CASO B: MODIFICA DIPENDENTE ESISTENTE ---
                sel = self.tree_dipendenti.selection()
                if not sel:
                    messagebox.showinfo("Attenzione", "Nessun record selezionato per la modifica.")
                    return
                
                self.item = self.tree_dipendenti.item(sel[0], "values")
                id_dipendente = int(self.item[0])

                dipendente_modificato = Dipendente(
                    id=id_dipendente,
                    nome=nome_dipendente,
                   
                )
                dipendente_modificato.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Dati del dipendente aggiornati con successo.")

            # --- OPERAZIONI DI CONCLUSIONE (COMUNI A ENTRAMBI I CASI) ---
            self.modalita_inserimento = False  # Resetta lo stato logico iniziale
            self._aggiorna()                   # Aggiorna la Treeview includendo le novità
            self._disabilita_campi()           # Ri-blocca l'interfaccia grafica in sola lettura

        except mysql.connector.Error as e:
            messagebox.showerror("Database", f"Errore durante l'operazione: {e}")

    def _annulla(self):
        """Annulla le modifiche correnti ripristinando i dati originali e blocca la UI."""
        self.modalita_inserimento = False  # Annulla l'operazione di creazione corrente
        self.modalita_modifica = False

        # Recupera la selezione corrente della tabella
        sel = self.tree_dipendenti.selection()
        
        if sel:
            # Forziamo temporaneamente lo stato normal sui campi altrimenti 
            # i metodi .delete() e .insert() verrebbero ignorati da Tkinter
            self.ent_dipendente.configure(state="normal")
           

            # Svuota i campi grafici
            self.ent_dipendente.delete(0, "end")
          

            # Estrae l'ID dalla riga selezionata nel Treeview
            self.item = self.tree_dipendenti.item(sel[0], "values")
            id_selezionato = int(self.item[0])

            # Recupera l'oggetto originale dalla cache in memoria (senza rieseguire la query SQL)
            dipendente = next((f for f in self.dati_dipendenti_totali if f.id == id_selezionato), None)
            
            # Se presente ripopola i campi con lo stato originale pre-modifica
            if dipendente:
                self.ent_dipendente.insert(0, dipendente.nome)
                

        else:
            # Se l'utente clicca Annulla senza una riga selezionata (es. dopo anomalie), pulisce e basta
            self.ent_dipendente.configure(state="normal")
            self.ent_dipendente.delete(0, "end")
           

        # 2. Ripristina lo stato di blocco dei widget e l'attivazione dei pulsanti corretti
        self._disabilita_campi()

    def _elimina(self):
        """Elimina il dipendente selezionato previa conferma dell'utente."""
        # 1. Recupera la riga selezionata nel Treeview
        sel = self.tree_dipendenti.selection()
        if not sel:
            messagebox.showinfo("Attenzione", "Nessun record selezionato per l'eliminazione.")
            return

        # 2. Estrae l'ID visibile nella riga
        self.item = self.tree_dipendenti.item(sel, "values")
        id_selezionato = int(self.item[0])

        # 3. Recupera l'oggetto dalla cache in memoria per conoscerne il nome
        dipendente = next((f for f in self.dati_dipendenti_totali if f.id == id_selezionato), None)
        nome_dipendente = dipendente.nome if dipendente else "questo dipendente"

        # 4. Finestra di dialogo per conferma di sicurezza (Evita cancellazioni accidentali)
        conferma = messagebox.askyesno(
            "Conferma Eliminazione", 
            f"Sei sicuro di voler eliminare definitivamente il dipendente:\n'{nome_dipendente}'?"
        )
        
        if not conferma:
            return  # Se l'utente clicca 'No', interrompe l'operazione

        # 5. Se l'utente conferma, procede alla cancellazione tramite l'oggetto modello
        try:
            if not dipendente:
                # Fallback se non fosse presente in cache
                dipendente = dipendente(id=id_selezionato)
                
            # Esegue la DELETE isolata nel modello
            dipendente.delete(self.c, self.conn)
            
            messagebox.showinfo("Successo", "dipendente eliminato con successo.")
            
            # 6. Ripristino dello stato ottimale della UI
            self._aggiorna()          # Rinfresca la tabella svuotando il record cancellato
            self._disabilita_campi()  # Riporta i campi in sola lettura e resetta i pulsanti
            
            # Pulisce i campi di testo dai dati del dipendente appena rimosso
            self.ent_dipendente.configure(state="normal")
            self.ent_dipendente.delete(0, "end")
            self.ent_dipendente.configure(state="disabled")

        except mysql.connector.Error as e:
            messagebox.showerror("Errore Database", f"Impossibile eliminare il dipendente: {e}")
        
    def _aggiorna(self):
        # Svuota la Treeview usando self
        self.tree_dipendenti.delete(*self.tree_dipendenti.get_children())
        
        # Svuota la barra di ricerca all'aggiornamento dei dati generali
        if hasattr(self, 'entry_filtro'):
            self.entry_filtro.delete(0, "end")
        
        # Richiamo del metodo centralizzato nella classe dipendente
        self.dati_dipendenti_totali = Dipendente.fetch_all(self.c)
        
        for dipendente in self.dati_dipendenti_totali:
           self.tree_dipendenti.insert("", "end", values=(dipendente.id, dipendente.nome))

    def _nuovo(self):
        """Prepara l'interfaccia principale per l'inserimento di un nuovo dipendente."""
        self.modalita_inserimento = True  # Attiva lo stato di inserimento nuovo record
        
        # Deseleziona qualsiasi riga precedentemente cliccata nella tabella per chiarezza visiva
        self.tree_dipendenti.selection_remove(self.tree_dipendenti.selection())

        # Sblocca temporaneamente i campi per consentire la pulizia e la scrittura
        self.ent_dipendente.configure(state="normal")
        
        # Resetta completamente i campi grafici per accogliere il nuovo testo
        self.ent_dipendente.delete(0, "end")
        
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
        if not self.tree_dipendenti.selection():
            messagebox.showinfo("Attenzione", "Seleziona un dipendente dall'elenco per poterlo modificare.")
            return
        
        self.modalita_modifica = True

        # Abilita i campi di input grafici
        self.ent_dipendente.configure(state="normal")
      
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
        self.ent_dipendente.configure(state="disabled")

        # Ripristina lo stato dei bottoni principali
        self.btn_nuovo.configure(state="normal")
        self.btn_modifica.configure(state="normal")
        
        # Blocca nuovamente i bottoni di gestione
        self.btn_salva.configure(state="disabled")
        self.btn_annulla.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

    def _onsingleclick(self, event):
        # Se l'utente sta scrivendo (Nuovo o Modifica), blocca gli eventi della tabella ---
        if getattr(self, 'modalita_inserimento', False) or getattr(self, 'modalita_modifica', False):
            return

        # self.modalita_inserimento = False  # Se clicca una riga, interrompe lo stato di "Nuovo"
        # Recupera la riga selezionata nel Treeview
        sel = self.tree_dipendenti.selection()
        if not sel:
            return

        # Sblocca temporaneamente i campi per consentire la scrittura via codice ---
        self.ent_dipendente.configure(state="normal")
        
        # Reset completo dei campi della UI grafica
        self.ent_dipendente.delete(0, "end")
        
        # Estrae i valori visibili della riga (il primo elemento è l'ID)
        self.item = self.tree_dipendenti.item(sel[0], "values")
        id_selezionato = int(self.item[0])
        
        # Cerca l'oggetto direttamente nella cache locale 
        dipendente = next((f for f in self.dati_dipendenti_totali if f.id == id_selezionato), None)
        
        # Se per qualsiasi motivo non è in cache, usa il metodo di classe sul DB
        if not dipendente:
            dipendente = Dipendente.find_by_id(self.c, id_selezionato)
            
        if not dipendente:
            return

        # Popola l'interfaccia grafica leggendo le proprietà dell'oggetto
        self.ent_dipendente.insert(0, dipendente.nome)
        '''
        if dipendente.flag1_ing_merce == 1:
            self.valore_flag_ing_merce.set(1)
        if dipendente.flag2_inventario == 1:
            self.valore_flag_inv.set(1)
        '''
        # Blocca nuovamente i campi in modalità sola lettura dopo il popolamento ---
        self._disabilita_campi()

    def _filtra_dipendente(self, event=None):
        """Filtra gli elementi della Treeview in base al testo digitato nella Entry."""
        # Recupera il testo digitato direttamente dalla Entry usando self
        testo_ricerca = self.entry_filtro.get().lower()
        
        # Svuota momentaneamente la Treeview per aggiornare l'elenco visivo
        self.tree_dipendenti.delete(*self.tree_dipendenti.get_children())
        
        # Sicurezza: se la lista in memoria non esiste ancora, esce
        if not hasattr(self, 'dati_dipendenti_totali'):
            return

        for dipendente in self.dati_dipendenti_totali:
            if testo_ricerca in str(dipendente.nome).lower() or testo_ricerca in str(dipendente.id):
                self.tree_dipendenti.insert("", "end", values=(dipendente.id, dipendente.nome))

    def _reset_ricerca(self):
        """Svuota il filtro, ripristina la lista completa e pulisce i dettagli."""
        # 1. Sicurezza: blocca l'azione se l'utente sta inserendo o modificando dati
        if getattr(self, 'modalita_inserimento', False) or getattr(self, 'modalita_modifica', False):
            return

        # 2. Rimuove la selezione visiva corrente dalla Treeview (se presente)
        if self.tree_dipendenti.selection():
            self.tree_dipendenti.selection_remove(self.tree_dipendenti.selection())

        # 3. Cancella il testo all'interno della Entry del filtro
        if hasattr(self, 'entry_filtro'):
            self.entry_filtro.delete(0, "end")
            
        # 4. Svuota la Treeview visiva per rigenerarla da zero
        self.tree_dipendenti.delete(*self.tree_dipendenti.get_children())
        
        # 5. Ripopola l'elenco completo sfruttando i dati già in memoria
        if hasattr(self, 'dati_dipendenti_totali'):
            for dipendente in self.dati_dipendenti_totali:
                self.tree_dipendenti.insert("", "end", values=(dipendente.id, dipendente.nome))

        # 6. Pulisce e azzera completamente i widget di dettaglio a destra
        self.ent_dipendente.configure(state="normal")
        self.ent_dipendente.delete(0, "end")
        
        # 7. Riporta i campi puliti allo stato iniziale di protezione (sola lettura)
        self._disabilita_campi()
    
    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = Dipendenti()
    root.mainloop()
