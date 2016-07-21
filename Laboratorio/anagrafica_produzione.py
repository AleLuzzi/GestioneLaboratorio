import tkinter as tk
from tkinter import ttk
import sqlite3


class Produzione(tk.Frame):
    def __init__(self, parent):
        super(Produzione, self).__init__(parent)

        self.item = ''
        self.lista_da_salvare = []
        self.campi = ['plu', 'prezzo1', 'prezzo2', 'prezzo3', 'prezzo4', 'prezzo_straord', 'gruppo_merc', 'tara',
                      'gg_cons_1', 'gg_cons_2', 'ean', 'testo_agg_1', 'testo_agg_2', 'testo_agg_3', 'testo_agg_4',
                      'pz_x_scatola', 'peso_fisso', 'num_offerta', 'art_in_pubblic', 'sovrascritt_prezzo',
                      'stile_tracc', 'rich_stm_traccia']
        self.formati = ['formato_1', 'formato_2', 'formato_3', 'formato_4']
        self.ingredienti = ['riga_1', 'riga_2', 'riga_3', 'riga_4']
        self.label = {}
        self.entry = {}
        self.box_reparto_value = tk.StringVar()
        self.box_merceologia_value = tk.StringVar()
        self.filtro_merceologia = tk.StringVar()
        self.valore_ckb_flag1 = tk.StringVar()
        self.valore_ckb_flag1.set(0)
        '''
        Connessione al Database
        '''
        self.conn = sqlite3.connect('../laboratorio/data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Definizione Frame
        '''
        self.frame_sx = tk.Frame(self, bd=1, relief="raised")
        self.frame_centrale_alto = tk.Frame(self, bd=1, relief="raised")
        self.frame_centrale_basso = tk.Frame(self, bd=1, relief="raised")
        self.frame_dx = tk.Frame(self, bd=1, relief="raised")

        self.lbl_lista_prodotti = ttk.LabelFrame(self.frame_sx, text='Lista Prodotti')
        '''
        Treeview per tab lista prodotti
        '''
        self.tree_produzione = ttk.Treeview(self.lbl_lista_prodotti, height=23)
        self.tree_produzione['columns'] = ('Id', 'Prodotto')
        self.tree_produzione['show'] = 'headings'
        self.tree_produzione.heading('Id', text="Id")
        self.tree_produzione.heading('Prodotto', text="Prodotto")

        self.tree_produzione.column("Id", width=20)
        self.tree_produzione.column("Prodotto", width=150)

        self.tree_produzione.bind("<Double-1>", self.ondoubleclick)

        self.lbl_frame_nome_prodotto = ttk.Labelframe(self.frame_centrale_alto, text='Prodotto')
        self.ent_nome_prodotto = ttk.Entry(self.lbl_frame_nome_prodotto, width=30)
        self.lbl_frame_reparto_prodotto = ttk.Labelframe(self.frame_centrale_alto, text='Reparto')
        self.lbl_frame_merceologia = ttk.Labelframe(self.frame_centrale_alto, text='Merceologia')
        self.box_reparto = ttk.Combobox(self.lbl_frame_reparto_prodotto, textvariable=self.box_reparto_value)
        self.box_merceologia = ttk.Combobox(self.lbl_frame_merceologia, textvariable=self.box_merceologia_value)
        self.ckb_flag1 = tk.Checkbutton(self.lbl_frame_merceologia, text='Usa in produzione',
                                        variable=self.valore_ckb_flag1)
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_centrale_alto,
                                                             text='Dettagli prodotto selezionato')
        self.lbl_ingredienti = ttk.Label(self.frame_centrale_basso, text='INGREDIENTI')
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx, text='Seleziona prodotto')
        self.btn_modifica = ttk.Button(self.lbl_frame_scegli, text='Modifica', command=self.modifica)
        self.btn_inserisci = ttk.Button(self.lbl_frame_scegli, text='Inserisci', command=self.inserisci)
        self.box_merceologia_filtro = ttk.Combobox(self.lbl_frame_scegli, textvariable=self.filtro_merceologia)
        self.btn_filtra = ttk.Button(self.lbl_frame_scegli, text='Filtra', command=self.filtra)
        self.btn_reset = ttk.Button(self.lbl_frame_scegli, text='Reset Lista Prodotti', command=self.aggiorna)

        self.crea_layout()
        self.aggiorna()
        self.riempi_combo_reparto()
        self.riempi_combo_merceologie()
        self.crea_label_entry()
        self.crea_label_formato_ingredienti()

    def crea_layout(self):
        self.frame_sx.grid(row=1, column=0, rowspan=2, sticky='n')
        self.frame_centrale_alto.grid(row=1, column=1, sticky='n')
        self.frame_centrale_basso.grid(row=2, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')
        self.lbl_lista_prodotti.grid(row=1, column=0, sticky='n')

        self.tree_produzione.grid(row=1, column=0, columnspan=3, sticky='we')

        self.lbl_frame_nome_prodotto.grid(row=1, column=0, columnspan=3)
        self.ent_nome_prodotto.grid(row=1, column=0)
        self.lbl_frame_reparto_prodotto.grid(row=2, column=0)
        self.lbl_frame_merceologia.grid(row=2, column=1)

        self.box_reparto.grid(row=1, column=0)
        self.box_merceologia.grid(row=1, column=1)
        self.ckb_flag1.grid(row=1, column=2)

        self.lbl_frame_dettagli_selezionato.grid(row=3, column=0, columnspan=2, sticky='n')
        self.lbl_ingredienti.grid(row=1, column=0, columnspan=4, pady=10)

        self.lbl_frame_scegli.grid(row=1, column=0)
        self.btn_modifica.grid(row=1, column=0, columnspan=2)
        self.btn_inserisci.grid(row=2, column=0, columnspan=2)

        self.box_merceologia_filtro.grid(row=3, column=0)
        self.btn_filtra.grid(row=4, column=0)
        self.btn_reset.grid(row=5, column=0)

    def crea_label_entry(self):
        r = 1
        c = 0
        for campo in self.campi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_dettagli_selezionato, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.lbl_frame_dettagli_selezionato)
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

    def crea_label_formato_ingredienti(self):
        r = 2
        c = 0
        for campo in self.formati:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.frame_centrale_basso, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.frame_centrale_basso, width='5')
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

        r = 2
        c = 2
        for campo in self.ingredienti:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.frame_centrale_basso, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.frame_centrale_basso, width='50')
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

    def riempi_combo_reparto(self):
        lista_rep = []

        for row in self.conn.execute("SELECT reparto From reparti WHERE flag2_prod = 1 "):
            lista_rep.extend(row)
        self.box_reparto['values'] = lista_rep

    def riempi_combo_merceologie(self):
        lista_merc = []

        for row in self.conn.execute("SELECT merceologia From merceologie"):
            lista_merc.extend(row)
        self.box_merceologia['values'] = lista_merc
        self.box_merceologia_filtro['values'] = lista_merc

    def modifica(self):
        stringa = 'UPDATE prodotti SET prodotto = ? WHERE ID = ?'
        self.c.execute(stringa, (self.ent_nome_prodotto.get(), (self.item[0])))
        self.conn.commit()
        stringa = 'UPDATE prodotti SET reparto = ? WHERE ID = ?'
        self.c.execute(stringa, (self.box_reparto_value.get(), (self.item[0])))
        self.conn.commit()
        stringa = 'UPDATE prodotti SET merceologia = ? WHERE ID = ?'
        self.c.execute(stringa, (self.box_merceologia_value.get(), (self.item[0])))
        self.conn.commit()

        for campo in self.campi:
            stringa = 'UPDATE prodotti SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for campo in self.ingredienti:
            stringa = 'UPDATE prodotti SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for campo in self.formati:
            stringa = 'UPDATE prodotti SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        self.c.execute('UPDATE prodotti SET flag1_prod=? WHERE ID = ?', (self.valore_ckb_flag1.get(), (self.item[0])))
        self.conn.commit()
        self.aggiorna()

    def inserisci(self):

        self.lista_da_salvare.append(self.ent_nome_prodotto.get())
        self.lista_da_salvare.append(self.box_reparto_value.get())
        for campo in self.campi:
            self.lista_da_salvare.append(self.entry[campo].get())
        for campo in self.ingredienti:
            self.lista_da_salvare.append(self.entry[campo].get())
        for campo in self.formati:
            self.lista_da_salvare.append(self.entry[campo].get())
        self.lista_da_salvare.append(self.box_merceologia_value.get())
        self.lista_da_salvare.append(self.valore_ckb_flag1.get())

        self.c.execute('INSERT INTO prodotti(prodotto, reparto, plu, prezzo1, prezzo2, prezzo3, prezzo4, '
                       'prezzo_straord,gruppo_merc, tara, gg_cons_1, gg_cons_2, ean, testo_agg_1, testo_agg_2, '
                       'testo_agg_3, testo_agg_4, pz_x_scatola, peso_fisso, num_offerta, art_in_pubblic, '
                       'sovrascritt_prezzo, stile_tracc, rich_stm_traccia, riga_1, riga_2, riga_3, riga_4, '
                       'formato_1, formato_2, formato_3, formato_4, merceologia, flag1_prod ) '
                       'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       self.lista_da_salvare)
        self.conn.commit()
        self.aggiorna()
        del self.lista_da_salvare[0:]

    def aggiorna(self):
        self.tree_produzione.delete(*self.tree_produzione.get_children())
        for lista in self.c.execute("SELECT * From prodotti "):
            self.tree_produzione.insert('', 'end', values=(lista[0], lista[1]))

        lista = []

        for row in self.c.execute("SELECT ID From prodotti"):
            lista.extend(row)

    def ondoubleclick(self, event):
        self.ckb_flag1.deselect()
        self.ent_nome_prodotto.delete(0, 'end')
        self.item = (self.tree_produzione.item(self.tree_produzione.selection(), 'values'))
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')
        for campo in self.ingredienti:
            self.entry[campo].delete(0, 'end')
        for campo in self.formati:
            self.entry[campo].delete(0, 'end')
        i = 1

        for self.row in self.c.execute("SELECT * FROM prodotti WHERE ID = ?", ((self.item[0],))):

            self.ent_nome_prodotto.insert(0, self.row[i])
            i += 1
            self.box_reparto.set(self.row[i])
            i += 1
            while i != 25:
                for campo in self.campi:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            while i != 29:
                for campo in self.ingredienti:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            while i != 33:
                for campo in self.formati:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            self.box_merceologia_value.set(self.row[i])
        i += 1
        if self.row[i] == 1:
            self.ckb_flag1.select()

    def filtra(self):
        self.tree_produzione.delete(*self.tree_produzione.get_children())
        for lista in self.c.execute("SELECT * FROM prodotti WHERE merceologia = ?", (self.filtro_merceologia.get(),)):
            self.tree_produzione.insert('', 'end', values=(lista[0], lista[1]))


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Produzione(notebook)
    notebook.add(new, text='Produzione')
    root.mainloop()
