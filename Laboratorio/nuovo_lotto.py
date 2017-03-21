import tkinter as tk
from tkinter import ttk
import datetime as dt
import sqlite3


class NuovoLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Nuovo Lotto")
        self.geometry("900x680+5+5")

        self.data = dt.date.today()

        self.conn = sqlite3.connect('data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()

        self.c.execute("SELECT prog_ven FROM progressivi")
        self.prog_lotto_ven = self.c.fetchone()[0]

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        '''
        DISPOSIZIONE FRAME
        '''
        self.frame_treeview = ttk.Frame(self)
        self.frame_treeview.grid(row='0', column='0', sticky='n')

        self.frame_nuovolotto = ttk.Frame(self)
        self.frame_nuovolotto.grid(row='0', column='1', sticky='n')
        '''
        Treeview per riepilogo immissioni
        '''
        self.tree = ttk.Treeview(self.frame_treeview, height=25)
        self.tree['columns'] = ('data ingresso', 'fornitore', 'peso', 'residuo')

        self.tree.column("data ingresso", width=80)
        self.tree.column("fornitore", width=80)
        self.tree.column("peso", width=80)
        self.tree.column("residuo", width=60)

        self.tree.heading("data ingresso", text="data ingresso")
        self.tree.heading("fornitore", text="fornitore")
        self.tree.heading("peso", text="peso")
        self.tree.heading("residuo", text="residuo")

        self.tree.tag_configure('odd', background='light green')

        self.tree.bind("<Double-1>", self.ondoubleclick)

        self.tree.grid(row='1', column='0', columnspan=2, sticky='w')
        '''
        LABEL nuovo lotto vendita
        '''
        self.lbl_nuovo_lotto = ttk.Label(self.frame_nuovolotto, text='NUOVO LOTTO VENDITA', font=('Helvetica', 20))
        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_nuovolotto, text=str(self.prog_lotto_ven) + 'V',
                                                font=('Helvetica', 40))
        self.lbl_nuovo_lotto.grid(row='1', column='0')
        self.lbl_prog_lotto_vendita.grid(row='2', column='0')
        '''
        Treeview per lotti selezionati
        '''
        self.tree_lotti_selezionati = ttk.Treeview(self.frame_nuovolotto, height=5)
        self.tree_lotti_selezionati['columns'] = 'taglio'
        self.tree_lotti_selezionati.column("taglio", width=70)
        self.tree_lotti_selezionati.heading("taglio", text="taglio")
        self.tree_lotti_selezionati.grid(row='3', column='0')
        '''
        LabelFrame nuova produzione
        '''
        self.labelframe = ttk.Labelframe(self.frame_nuovolotto, text="Nuova Produzione")
        self.labelframe.grid(row='4', column='0')

        for row in self.c.execute("SELECT prodotto FROM prodotti WHERE reparto = 'Macelleria'"):
            self.lista_nuova_produzione.extend(row)

        '''
        Lista articoli per nuova produzione
        '''
        self.nuova_produzione = tk.StringVar()
        self.row, self.col = 1, 0
        for i in range(0, len(self.lista_nuova_produzione)):
            if self.row % 8 == 0:
                self.col += 1
                self.row = 1
            tk.Radiobutton(self.labelframe,
                           text=str(self.lista_nuova_produzione[i]).upper(),
                           variable=self.nuova_produzione,
                           width=20,
                           indicatoron=0,
                           value=self.lista_nuova_produzione[i],
                           font='Helvetica').grid(row=self.row, column=self.col, sticky="w", pady=2)
            self.row += 1
        '''
        SEPARATORE
        '''
        self.sep = ttk.Separator(self.frame_nuovolotto, orient='horizontal')
        self.sep.grid(row='5', column='0', columnspan='1', sticky='ew', pady=10)
        '''
        LABELFRAME per peso da inserire
        '''
        self.lblframe_peso = ttk.LabelFrame(self.frame_nuovolotto, text='Peso')
        self.lblframe_peso.grid(row='6', column='0')
        '''
        ENTRY per inserimento del peso
        '''
        self.peso_da_inserire = tk.StringVar()
        self.entry_peso = ttk.Entry(self.lblframe_peso, textvariable=self.peso_da_inserire)
        self.entry_peso.focus()
        self.entry_peso.grid()
        '''
        Ciclo per inserire i lotti in acquisto da utilizzare
        '''
        for lista in self.c.execute("SELECT * from ingresso_merce WHERE lotto_chiuso = 'no'"):
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')
        '''
        BOTTONE ESCI E SALVA
        '''
        self.btn_esci = ttk.Button(self.frame_treeview, text="Chiudi finestra", command=self.destroy)
        self.btn_esci_salva = ttk.Button(self.frame_treeview, text="Esci e salva", command=self.esci_salva)

        self.btn_esci.grid(row='2', column='0', padx='10', pady=20)
        self.btn_esci_salva.grid(row='2', column='1', padx='10', pady=20)

    def esci_salva(self):
        if (self.nuova_produzione.get() != '') \
                and (self.peso_da_inserire.get() != '') \
                and (self.lista_da_salvare != []):
            self.c.executemany('INSERT INTO lotti_vendita VALUES (?,?,?,?,?,?)', self.lista_da_salvare)
            self.conn.commit()
            self.c.execute('UPDATE progressivi SET prog_ven = ?', (self.prog_lotto_ven + 1,))
            self.conn.commit()
            self.conn.close()
            self.destroy()
        else:
            pass

    def ondoubleclick(self, event):
        if (self.nuova_produzione.get() != '') and (self.peso_da_inserire.get() != ''):
            item = self.tree.selection()[0]
            self.tree_lotti_selezionati.insert('', 'end', text=self.tree.parent(item),
                                               values=(self.tree.item(item, 'text')))
            self.lista_da_salvare.append(((str(self.prog_lotto_ven) + 'V'),
                                         self.data, (self.tree.parent(item)),
                                         (self.nuova_produzione.get()),
                                         (self.peso_da_inserire.get()),
                                         (self.tree.item(item, 'text'))))
        else:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLotto()
    root.mainloop()
