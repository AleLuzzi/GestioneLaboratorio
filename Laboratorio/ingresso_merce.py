import tkinter as tk
from tkinter import ttk
import datetime
import sqlite3


class IngressoMerce(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Ingresso Merce")
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())
        '''
        Connessione al database
        '''
        self.conn = sqlite3.connect('../Laboratorio/data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Lettura progressivo lotto acquisto da file
        '''
        self.c.execute("SELECT prog_acq FROM progressivi")
        self.prog_lotto_acq = self.c.fetchone()[0]
        '''
        Inizializzazione lista per valori da salvare sul database
        '''
        self.lista_da_salvare = []
        self.fornitore = tk.StringVar()
        self.taglio_s = tk.StringVar()
        self.peso = tk.StringVar()
        '''
        Creazione liste fornitori e tagli suino
        '''
        self.lista_fornitori = []
        for row in self.c.execute("SELECT azienda FROM fornitori WHERE flag1_ing_merce = 1"):
            self.lista_fornitori.extend(row)
        self.lista_tagli = ('Mezzena', 'Costarelle', 'Lombo', 'Carnetta', 'Collo', 'Busto',
                            'Sogna', 'Pancia', 'Maialino', 'Arista', 'Filetto', 'Spalla', 'Guanciale',
                            'Teste', 'Tronchetto', 'Corata')
        '''
        Layouto dei frame per impaginazione
        '''
        self.frame_alto = tk.Frame(self, bd=3, relief='groove')
        self.frame_sx = tk.Frame(self, bd=3, relief='groove')
        self.frame_dx = tk.Frame(self, bd=3, relief='groove')
        self.frame_basso = tk.Frame(self, background='white')
        self.frame_alto.grid(row=1, column=0, columnspan=2, sticky='we')
        self.frame_sx.grid(row=2, column=0)
        self.frame_dx.grid(row=2, column=1, sticky='n')
        self.frame_basso.grid(row=3, column=0, columnspan=2, sticky='we')
        '''
        Creazione TREEVIEW
        '''
        self.tree = ttk.Treeview(self.frame_alto, height=8)
        self.tree['columns'] = ('fornitore', 'prodotto', 'quantita')
        self.tree['show'] = 'headings'
        self.tree.column("fornitore", width=100)
        self.tree.column("prodotto", width=100)
        self.tree.column("quantita", width=100)
        self.tree.heading("fornitore", text="Fornitore")
        self.tree.heading("prodotto", text="Prodotto")
        self.tree.heading("quantita", text="quantita")
        self.tree.grid(row=0, column=2, rowspan=10, padx=10)
        '''
        Labelframe per creazione bottoni per scelta fornitore
        '''
        self.labelframe = ttk.Labelframe(self.frame_sx, text="Fornitore")
        self.labelframe.grid(row=2, column=0, sticky='n')
        '''
        Labelframe per creazione bottoni per i tagli suino
        '''
        self.labelframe_taglio = ttk.Labelframe(self.frame_dx, text="Taglio")
        self.labelframe_taglio.grid(row=1, column=0, columnspan=3)
        '''
        LABEL che mostra il progressivo lotto
        '''
        self.label_lotto = ttk.Label(self.frame_alto, text="Progressivo Lotto",
                                     foreground='blue', font=('Helvetica', 20))
        self.label_prog_lotto = ttk.Label(self.frame_alto, anchor='center',
                                          text=str(self.prog_lotto_acq)+'A', font=('Helvetica', 20))
        self.label_lotto.grid(row=1, column=0)
        self.label_prog_lotto.grid(row=1, column=1)
        '''
        LABEL che mostra la data ingresso merce
        '''
        # TODO: migliorare con data selezionabile
        self.data = datetime.date.today()
        self.label_data_ingresso = ttk.Label(self.frame_alto,
                                             text="Data Ingresso Merce", foreground='blue', font=('Helvetica', 20))
        self.label_data = ttk.Label(self.frame_alto, anchor='center',
                                    text=self.data.strftime('%d/%m/%y'), font=('Helvetica', 20))
        self.label_data_ingresso.grid(row=3, column=0)
        self.label_data.grid(row=3, column=1)
        '''
        ENTRY per immissione numero ddt/fattura
        '''
        self.label_num_ddt = ttk.Label(self.frame_alto,
                                       text='Numero DDT/Fattura', foreground='blue', font=('Helvetica', 15))
        self.label_num_ddt.grid(row=5, column=0)
        self.num_ddt = tk.StringVar()
        self.entry_ddt = ttk.Entry(self.frame_alto, textvariable=self.num_ddt, width=25)
        self.entry_ddt.focus()
        self.entry_ddt.grid(row=5, column=1)
        '''
        ENTRY per inserimento del peso
        '''
        self.label_peso = ttk.Label(self.frame_alto, text="Inserimento Peso", foreground='blue', font=('Helvetica', 15))
        self.label_peso.grid(row=7, column=0)
        self.entry = ttk.Entry(self.frame_alto, textvariable=self.peso, width=25)
        self.entry.grid(row=7, column=1)
        '''
        BOTTONI salva e chiudi finestra
        '''
        self.btn_invio = ttk.Button(self.frame_basso,
                                    text="Invio",
                                    command=self.invio).grid(row=2, column=0, padx=10, pady=10)
        self.btn_salva_esci = ttk.Button(self.frame_basso,
                                         text="Salva ed esci",
                                         command=self.salva_esci).grid(row=2, column=1, padx=10, pady=10)
        self.btn_chiudi_finestra = ttk.Button(self.frame_basso,
                                              text='Chiudi finestra',
                                              command=self.chiudi).grid(row=2, column=2, padx=10, pady=10)
        self.crea_bottoni_tagli()
        self.crea_bottoni_fornitori()

    def crea_bottoni_fornitori(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_fornitori)):
            if row % 6 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe, text=str(self.lista_fornitori[i]).upper(), variable=self.fornitore,
                           width=20, indicatoron=0, value=self.lista_fornitori[i],
                           font='Helvetica').grid(row=row, column=col, sticky='w')
            row += 1

    def crea_bottoni_tagli(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_tagli)):
            if row % 7 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_taglio, text=self.lista_tagli[i], indicatoron=0,
                           width=20, variable=self.taglio_s, value=self.lista_tagli[i],
                           font='Helvetica').grid(row=row, column=col, sticky='w')
            row += 1

    def invio(self):
        self.tree.insert("", 'end', values=(self.fornitore.get(), self.taglio_s.get(), self.peso.get()))
        self.lista_da_salvare.append(((str(self.prog_lotto_acq)+'A'), self.data, (self.num_ddt.get()),
                                      (self.fornitore.get()), (self.taglio_s.get()),
                                      (self.peso.get()), (self.peso.get()), 'no'))
        self.entry.delete(0, tk.END)

    def salva_esci(self):
        self.c.executemany('INSERT INTO ingresso_merce VALUES (?,?,?,?,?,?,?,?)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_acq = ?', (self.prog_lotto_acq + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def chiudi(self):
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()
