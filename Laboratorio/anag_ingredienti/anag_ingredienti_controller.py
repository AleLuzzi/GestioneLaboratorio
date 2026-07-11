
import tkinter as tk
from tkinter import messagebox

import mysql.connector

from db import get_connection, close_connection
from anag_ingredienti.anag_ingredienti_Tkinter import setup_window, build_ui
from anag_ingredienti.ingrediente import Ingrediente

class AnagIngredientiController(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.item = ""
        self.valore_flag = dict()

        # Connessione al Database
        self.conn = get_connection()
        self.c = self.conn.cursor()

        build_ui(self)

        # FIX: popola la cache usata dal filtro (_filtra_ingrediente)
        if hasattr(self, "_aggiorna"):
            self._aggiorna()

        
        
    def _nuovo(self):
        """Prepara l'interfaccia principale per l'inserimento di un nuovo ingrediente."""
        self.modalita_inserimento = True

        self.tree_ingredienti.selection_remove(self.tree_ingredienti.selection())

        self.ent_ingrediente.configure(state="normal")
        self.ent_cod_ean.configure(state="normal")
        self.ent_merceologia.configure(state="normal")

        self.ent_ingrediente.delete(0, "end")
        self.ent_cod_ean.delete(0, "end")
        self.ent_merceologia.delete(0, "end")

        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")

        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")
        
    def _modifica(self):
        """Abilita i campi di inserimento e i pulsanti di gestione dati."""
        if not self.tree_ingredienti.selection():
            messagebox.showinfo("Attenzione", "Seleziona un ingrediente dall'elenco per poterlo modificare.")
            return

        self.modalita_modifica = True

        self.ent_ingrediente.configure(state="normal")
        self.ent_cod_ean.configure(state="normal")
        self.ent_merceologia.configure(state="normal")   

        self.btn_nuovo.configure(state="disabled")
        self.btn_modifica.configure(state="disabled")

        self.btn_salva.configure(state="normal")
        self.btn_annulla.configure(state="normal")
        self.btn_elimina.configure(state="normal")
        
    def _disabilita_campi(self):
        """Riporta l'interfaccia allo stato iniziale di blocco (sola lettura)."""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        self.ent_ingrediente.configure(state="disabled")
        self.ent_cod_ean.configure(state="disabled")
        self.ent_merceologia.configure(state="disabled")
        self.ckbtn_allergene.configure(state="disabled")

        self.btn_nuovo.configure(state="normal")
        self.btn_modifica.configure(state="normal")

        self.btn_salva.configure(state="disabled")
        self.btn_annulla.configure(state="disabled")
        self.btn_elimina.configure(state="disabled")
        
    def _annulla(self):
        """Annulla le modifiche correnti ripristinando i dati originali e blocca la UI."""
        self.modalita_inserimento = False
        self.modalita_modifica = False

        sel = self.tree_ingredienti.selection()

        if sel:
            self.ent_ingrediente.configure(state="normal")
            self.ent_cod_ean.configure(state="normal")
            self.ent_merceologia.configure(state="normal")
            self.ckbtn_allergene.configure(state="normal")
            self.valori_allergene.set(0)

            self.ent_ingrediente.delete(0, "end")
            self.ent_cod_ean.delete(0, "end")
            self.ent_merceologia.delete(0, "end")
            self.ckbtn_allergene.configure(state="normal")

            self.item = self.tree_ingredienti.item(sel[0], "values")
            id_selezionato = int(self.item[0])

            ingrediente = next((r for r in self.dati_ingredienti_totali if r.id == id_selezionato), None)

            if ingrediente:
                self.ent_ingrediente.insert(0, ingrediente.ingrediente_base)
                self.ent_cod_ean.insert(0, getattr(ingrediente, 'cod_ean', ''))
                self.ent_merceologia.insert(0, getattr(ingrediente, 'merceologia', ''))
                if ingrediente.flag1_allergene == 1:
                    self.valori_allergene.set(1)
                else:
                    self.valori_allergene.set(0)
                        
            self.ent_ingrediente.configure(state="normal")
            self.ent_cod_ean.configure(state="normal")
            self.ent_merceologia.configure(state="normal")
            
            self.ent_ingrediente.delete(0, "end")
            self.ent_cod_ean.delete(0, "end")
            self.ent_merceologia.delete(0, "end")
            self.ckbtn_allergene.configure(state="normal")

        self._disabilita_campi()
       
    def _salva(self):
        # Riferimenti corretti ai widget dell'ingrediente anziché del reparto
        ingrediente_nome = self.ent_ingrediente.get().strip()
        cod_ean = self.ent_cod_ean.get().strip()
        merceologia = self.ent_merceologia.get().strip()
        flag_allergene = self.valori_allergene.get()

        if not ingrediente_nome:
            messagebox.showwarning("Attenzione", "Il campo Ingrediente è obbligatorio.")
            return

        try:
            if self.modalita_inserimento:
                nuovo_ingrediente = Ingrediente(
                    id=None,
                    ingrediente_base=ingrediente_nome,
                    cod_ean=cod_ean,
                    flag1_allergene=int(flag_allergene), # Mappato correttamente
                    merceologia=merceologia
                )

                nuovo_ingrediente.insert(self.c, self.conn)
                messagebox.showinfo("Successo", "Nuovo ingrediente inserito con successo.")
            
            else:
                sel = self.tree_ingredienti.selection()
                if not sel:
                    messagebox.showinfo("Attenzione", "Nessun record selezionato per la modifica.")
                    return

                self.item = self.tree_ingredienti.item(sel[0], "values")
                id_selezionato = int(self.item[0])

                ingrediente_modificato = Ingrediente(
                    id=id_selezionato,
                    ingrediente_base=ingrediente_nome,
                    cod_ean=cod_ean,
                    flag1_allergene=int(flag_allergene),
                    merceologia=merceologia
                )

                ingrediente_modificato.save(self.c, self.conn)
                messagebox.showinfo("Successo", "Dati dell'ingrediente aggiornati con successo.")

            self.modalita_inserimento = False
            self._aggiorna()
            self._disabilita_campi()

        except mysql.connector.Error as e:
            messagebox.showerror("Database", f"Errore durante l'operazione: {e}")

    def _aggiorna(self):
        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())

        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        self.dati_ingredienti_totali = Ingrediente.fetch_all(self.c)

        for ingrediente in self.dati_ingredienti_totali:
            self.tree_ingredienti.insert(
                "", 
                "end", 
                values=(ingrediente.id, ingrediente.ingrediente_base, getattr(ingrediente, 'cod_ean', ''), getattr(ingrediente, 'merceologia', ''))
            )

    def _elimina(self):
        """Elimina l'ingrediente selezionato previa conferma dell'utente."""
        sel = self.tree_ingredienti.selection()
        if not sel:
            messagebox.showinfo("Attenzione", "Nessun record selezionato per l'eliminazione.")
            return

        self.item = self.tree_ingredienti.item(sel, "values")
        id_selezionato = int(self.item[0])

        ingrediente = next((r for r in self.dati_ingredienti_totali if r.id == id_selezionato), None)
        nome_ingrediente = ingrediente.ingrediente if ingrediente else "questo ingrediente"

        conferma = messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente l'ingrediente:\n'{nome_ingrediente}'?",
        )

        if not conferma:
            return

        try:
            if not ingrediente:
                ingrediente = Ingrediente(id=id_selezionato)

            ingrediente.delete(self.c, self.conn)
            messagebox.showinfo("Successo", "Ingrediente eliminato con successo.")

            self._aggiorna()
            self._disabilita_campi()

            self.ent_ingrediente.configure(state="normal")
            self.ent_cod_ean.configure(state="normal")
            self.ent_merceologia.configure(state="normal")
            self.ckbtn_allergene.configure(state="normal")
           
            self.ent_ingrediente.delete(0, "end")
            self.ent_cod_ean.delete(0, "end")
            self.ent_merceologia.delete(0, "end")
            self.ckbtn_allergene.configure(state="normal")
            self.valori_allergene.set(0)
            self.ent_ingrediente.delete(0, "end")
        except mysql.connector.Error as e:
            messagebox.showerror("Errore Database", f"Impossibile eliminare l'ingrediente: {e}")

    def _filtra_ingrediente(self, event=None):
        """Filtra gli ingredienti nella Treeview in base al testo inserito."""
        testo_ricerca = self.entry_filtro.get().lower()
        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())

        if not hasattr(self, "dati_ingredienti_totali"):
            return

        for r in self.dati_ingredienti_totali:
            if (testo_ricerca in str(r.ingrediente_base).lower() or 
                testo_ricerca in str(r.id) or 
                testo_ricerca in str(getattr(r, 'cod_ean', '')).lower()):
                
                self.tree_ingredienti.insert(
                    "", "end", 
                    values=(r.id, r.ingrediente_base, getattr(r, 'cod_ean', ''), getattr(r, 'merceologia', ''))
                )
    
    def _onsingleclick(self, event):
        # ------------------------------------------------------------------------------------------------
        # Se l'utente sta scrivendo (Nuovo o Modifica), blocca gli eventi della tabella ---
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return
        # ------------------------------------------------------------------------------------------------
        # Recupera la riga selezionata nel Treeview
        sel = self.tree_ingredienti.selection()
        if not sel:
            return
        # ------------------------------------------------------------------------------------------------
        self.ent_ingrediente.configure(state="normal")
        self.ent_cod_ean.configure(state="normal")
        self.ent_merceologia.configure(state="normal")
        self.ckbtn_allergene.configure(state="normal")

        # ------------------------------------------------------------------------------------------------
        # Reset completo dei campi della UI grafica
        self.ent_ingrediente.delete(0, "end")
        self.ent_cod_ean.delete(0, "end")
        self.ent_merceologia.delete(0, "end")
        self.valori_allergene.set(0)
        # ------------------------------------------------------------------------------------------------
        # Recupera l'ID dell'ingrediente selezionato
        self.item = self.tree_ingredienti.item(sel[0], "values")
        id_selezionato = int(self.item[0])
        # ------------------------------------------------------------------------------------------------
        # Recupera l'oggetto ingrediente selezionato
        ingrediente = next((r for r in self.dati_ingredienti_totali if r.id == id_selezionato), None)

        if not ingrediente:
            # ------------------------------------------------------------------------------------------------
            # Se l'oggetto ingrediente non è in cache, lo recupera dal database
            ingrediente = Ingrediente.find_by_id(self.c, id_selezionato)

        if not ingrediente:
            return

        # ------------------------------------------------------------------------------------------------
        # Popola l'interfaccia grafica leggendo le proprietà dell'oggetto
        self.ent_ingrediente.insert(0, ingrediente.ingrediente_base)
        self.ent_cod_ean.insert(0, getattr(ingrediente, 'cod_ean', ''))
        self.ent_merceologia.insert(0, getattr(ingrediente, 'merceologia', ''))
        # ------------------------------------------------------------------------------------------------
        # Popola il campo allergene
        if ingrediente.flag1_allergene == 1:
            self.valori_allergene.set(1)
        
        # ------------------------------------------------------------------------------------------------
        # Blocca nuovamente i campi in modalità sola lettura dopo il popolamento ---
        self._disabilita_campi()    

    def _reset_ricerca(self):
        """Svuota il filtro e ripristina l'elenco completo degli ingredienti."""
        if getattr(self, "modalita_inserimento", False) or getattr(self, "modalita_modifica", False):
            return

        if self.tree_ingredienti.selection():
            self.tree_ingredienti.selection_remove(self.tree_ingredienti.selection())

        if hasattr(self, "entry_filtro"):
            self.entry_filtro.delete(0, "end")

        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())

        if hasattr(self, "dati_ingredienti_totali"):
            for r in self.dati_ingredienti_totali:
                self.tree_ingredienti.insert(
                    "", "end", 
                    values=(r.id, r.ingrediente_base, getattr(r, 'cod_ean', ''), getattr(r, 'merceologia', ''))
                )

        self.ent_ingrediente.configure(state="normal")
        self.ent_ingrediente.delete(0, "end")
        self.ent_cod_ean.configure(state="normal")
        self.ent_cod_ean.delete(0, "end")
        self.ent_merceologia.configure(state="normal")
        self.ent_merceologia.delete(0, "end")
        self.valori_allergene.set(0)

        self._disabilita_campi()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == "__main__":
    root = tk.Tk()
    AnagIngredientiController()
    root.mainloop()
