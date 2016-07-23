import tkinter as tk
from tkinter import ttk
import datetime as dt
import sqlite3


class NuovoLottoCucina(tk.Toplevel):
    def __init__(self):
        super(NuovoLottoCucina, self).__init__()
        self.title("Nuovo Lotto Cucina")
        self.geometry("+0+0")

        self.data = dt.date.today()

        self.conn = sqlite3.connect('../laboratorio/data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        self.prog_lotto_ven = ''
        self.genera_progressivo()

        '''
        DISPOSIZIONE FRAME
        '''
        self.frame_treeview = tk.Frame(self, bd='3', relief='groove')
        self.frame_treeview.grid(row=0, column=0, padx='10', sticky='n')

        self.frame_nuovolotto = tk.Frame(self, bd='3', relief='groove')
        self.frame_nuovolotto.grid(row=0, column=1, sticky='n')

        self.frame_basso = tk.Frame(self, bd='3', relief='groove')
        self.frame_basso.grid(row=1, column=0, columnspan=3, sticky='w')
        '''
        Treeview per riepilogo immissioni
        '''
        self.tree = ttk.Treeview(self.frame_treeview, height=5)
        self.tree['columns'] = ('prodotto', 'peso')

        self.tree['show'] = 'headings'

        self.tree.column("prodotto", width=120)
        self.tree.column("peso", width=80)

        self.tree.heading("prodotto", text="prodotto")
        self.tree.heading("peso", text="peso")

        self.tree.tag_configure('odd', background='light green')

        self.tree.grid(row=3, column=0, sticky='we')
        '''
        LABEL nuovo lotto vendita
        '''
        self.lbl_nuovo_lotto = ttk.Label(self.frame_treeview, text='NUOVO LOTTO VENDITA', font=('Helvetica', 20))
        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_treeview, text=str(self.prog_lotto_ven) + 'V',
                                                font=('Helvetica', 40))
        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.lbl_prog_lotto_vendita.grid(row=1, column=0)
        '''
        LabelFrame nuova produzione
        '''
        self.labelframe = ttk.Labelframe(self.frame_nuovolotto, text="Nuova Produzione")
        self.labelframe.grid(row=2, column=0)

        for row in self.c.execute("SELECT prodotto FROM prodotti WHERE flag1_prod = 1 "):
            self.lista_nuova_produzione.extend(row)

        '''
        LABELFRAME per peso da inserire
        '''
        self.lblframe_peso = ttk.LabelFrame(self.frame_basso, text='Peso')
        self.lblframe_peso.grid(row=0, column=0, sticky='w')
        '''
        ENTRY per inserimento del peso
        '''
        self.peso_da_inserire = tk.StringVar()
        self.entry_peso = ttk.Entry(self.lblframe_peso, textvariable=self.peso_da_inserire)
        self.entry_peso.focus()
        self.entry_peso.grid()
        '''
        Lista articoli per nuova produzione
        '''
        self.nuova_produzione = tk.StringVar()
        '''
        BOTTONE ESCI E SALVA
        '''
        self.btn_invia = ttk.Button(self.frame_basso, text="Invio", command=self.invia)
        self.btn_esci = ttk.Button(self.frame_basso, text="Chiudi finestra", command=self.destroy)
        self.btn_esci_salva = ttk.Button(self.frame_basso, text="Esci e salva", command=self.esci_salva)

        self.btn_invia.grid(row=0, column=1, padx=10, pady=20)
        self.btn_esci.grid(row=0, column=2, padx=10, pady=20)
        self.btn_esci_salva.grid(row=0, column=3, padx=10, pady=20)

        self.crea_articoli_nuova_produzione()

    def crea_articoli_nuova_produzione(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_nuova_produzione)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe,
                           text=str(self.lista_nuova_produzione[i]).upper(),
                           variable=self.nuova_produzione,
                           width=20,
                           indicatoron=0,
                           value=self.lista_nuova_produzione[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def genera_progressivo(self):
        self.c.execute("SELECT prog_ven FROM progressivi")
        self.prog_lotto_ven = self.c.fetchone()[0]

    def invia(self):
        if (self.nuova_produzione.get() != '') and (self.peso_da_inserire.get() != ''):
            self.tree.insert('', 'end', values=(self.nuova_produzione.get(), self.peso_da_inserire.get()))
            self.lista_da_salvare.append(((str(self.prog_lotto_ven) + 'V'), self.data, '0', self.nuova_produzione.get(),
                                         self.peso_da_inserire.get(), '0'))

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

if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLottoCucina()
    root.mainloop()
