import tkinter as tk
from tkinter import ttk
import datetime as dt
import sqlite3
import random


class NuovoMenu(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Nuovo Lotto Cucina")
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())

        self.data = dt.date.today()

        self.conn = sqlite3.connect('data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione_primi_piatti = []
        self.lista_nuova_produzione_secondi_piatti = []
        self.lista_nuova_produzione_contorni = []
        self.prog_lotto_ven = ''
        self.nuova_produzione = tk.StringVar()
        self.genera_progressivo()

        '''
        DISPOSIZIONE FRAME
        '''
        self.frame_treeview = tk.Frame(self, bd='3', relief='groove')
        self.frame_treeview.grid(row='0', column='0', padx='10', sticky='n')

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
        self.labelframe_primi_piatti = ttk.Labelframe(self.frame_nuovolotto, text="Primi piatti")
        self.labelframe_primi_piatti.grid(row=2, column=0)

        self.labelframe_secondi_piatti = ttk.Labelframe(self.frame_nuovolotto, text="secondi piatti")
        self.labelframe_secondi_piatti.grid(row=2, column=1)

        self.labelframe_contorni = ttk.Labelframe(self.frame_nuovolotto, text="contorni")
        self.labelframe_contorni.grid(row=2, column=2)
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
        BOTTONE ESCI E SALVA
        '''
        self.btn_invia = ttk.Button(self.frame_basso, text="Invio", command=self.invia)
        self.btn_esci = ttk.Button(self.frame_basso, text="Chiudi finestra", command=self.destroy)
        self.btn_esci_salva = ttk.Button(self.frame_basso, text="Esci e salva", command=self.esci_salva)
        self.btn_nuovo_menu = ttk.Button(self.frame_basso, text="Nuovo Menu",
                                         command=self.crea_nuovo_menu)

        self.btn_invia.grid(row=0, column=1, padx=10, pady=20)
        self.btn_esci.grid(row=0, column=2, padx=10, pady=20)
        self.btn_esci_salva.grid(row=0, column=3, padx=10, pady=20)
        self.btn_nuovo_menu.grid(row=0, column=4, padx=10, pady=20)

        self.crea_nuovo_menu()

    def crea_nuovo_menu(self):
        self.crea_articoli_nuova_produzione_primi_piatti()
        self.crea_articoli_nuova_produzione_secondi_piatti()
        self.crea_articoli_nuova_produzione_contorni()

    def crea_articoli_nuova_produzione_primi_piatti(self):
        for label in self.labelframe_primi_piatti.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        for row in self.c.execute("SELECT prodotto FROM prodotti "
                                  "WHERE reparto = 'Gastronomia' AND merceologia = 'Primi piatti' "):
            self.lista_nuova_produzione_primi_piatti.extend(row)

        lista_primi_piatti = (random.sample(self.lista_nuova_produzione_primi_piatti, 3))

        row, col = 1, 0
        for i in range(0, len(lista_primi_piatti)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_primi_piatti,
                           text=str(lista_primi_piatti[i]).upper(),
                           variable=self.nuova_produzione,
                           width=35,
                           indicatoron=0,
                           value=lista_primi_piatti[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def crea_articoli_nuova_produzione_secondi_piatti(self):
        for label in self.labelframe_secondi_piatti.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        for row in self.c.execute("SELECT prodotto FROM prodotti "
                                  "WHERE reparto = 'Gastronomia' AND merceologia = 'Secondi piatti' "):
            self.lista_nuova_produzione_secondi_piatti.extend(row)

        lista_secondi_piatti = (random.sample(self.lista_nuova_produzione_secondi_piatti, 3))

        row, col = 1, 0
        for i in range(0, len(lista_secondi_piatti)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_secondi_piatti,
                           text=str(lista_secondi_piatti[i]).upper(),
                           variable=self.nuova_produzione,
                           width=35,
                           indicatoron=0,
                           value=lista_secondi_piatti[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def crea_articoli_nuova_produzione_contorni(self):
        for label in self.labelframe_contorni.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        for row in self.c.execute("SELECT prodotto FROM prodotti "
                                  "WHERE reparto = 'Gastronomia' AND merceologia = 'Contorni' "):
            self.lista_nuova_produzione_contorni.extend(row)

        lista_contorni = (random.sample(self.lista_nuova_produzione_contorni, 3))

        row, col = 1, 0
        for i in range(0, len(lista_contorni)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_contorni,
                           text=str(lista_contorni[i]).upper(),
                           variable=self.nuova_produzione,
                           width=35,
                           indicatoron=0,
                           value=lista_contorni[i],
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
    new = NuovoMenu()
    root.mainloop()
