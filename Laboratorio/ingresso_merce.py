import tkinter as tk
from tkinter import ttk
from datepicker import Datepicker
import datetime
import mysql.connector


class IngressoMerce(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Ingresso Merce")
        self.geometry("1024x525+0+0")

        # Connessione al database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            port='3306',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        # Lettura progressivo lotto acquisto da file
        self.c.execute("SELECT prog_acq FROM progressivi")
        self.prog_lotto_acq = self.c.fetchone()[0]

        # Inizializzazione lista per valori da salvare sul database
        self.lista_da_salvare = []
        self.fornitore = tk.StringVar()
        self.taglio_s = tk.StringVar()
        self.peso = tk.StringVar()
        self.data = tk.StringVar()
        self.data.set(datetime.date.today().strftime('%d-%m-%Y'))

        # Creazione liste fornitori
        self.lista_fornitori = []
        self.c.execute("SELECT azienda FROM fornitori WHERE flag1_ing_merce = 1")

        for row in self.c:
            self.lista_fornitori.extend(row)
        # Creazione lista tagli suino
        self.lista_tagli = []
        self.c.execute("SELECT taglio FROM tagli WHERE taglio LIKE '%Suino'")

        for row in self.c:
            self.lista_tagli.extend(row)

        # LAYOUT dei frame per impaginazione
        self.frame_alto_sx = tk.Frame(self, bd=3)
        self.frame_alto_dx = tk.Frame(self, bd=3)
        self.frame_sx = tk.Frame(self, bd=3)
        self.frame_dx = tk.Frame(self, bd=3)
        self.frame_basso = tk.Frame(self, background='white')

        # TREEVIEW per riepilogo inserimenti
        self.tree = ttk.Treeview(self.frame_alto_dx, height=8)

        self.tree['columns'] = ('prog_acq', 'data', 'num_ddt', 'fornitore',
                                'taglio', 'peso_i', 'peso_f', 'lotto_chiuso')

        self.tree['displaycolumns'] = ('data', 'fornitore', 'taglio', 'peso_i')
        self.tree['show'] = 'headings'
        self.tree.column("data", width=100)
        self.tree.column("fornitore", width=100)
        self.tree.column("taglio", width=100)
        self.tree.column("peso_i", width=100)
        self.tree.heading("data", text='Data')
        self.tree.heading("fornitore", text="Fornitore")
        self.tree.heading("taglio", text="Prodotto")
        self.tree.heading("peso_i", text="Quantità")

        # LABELFRAME per creazione bottoni per scelta fornitore
        self.labelframe_fornitori = tk.LabelFrame(self.frame_sx,
                                                  text="FORNITORE",
                                                  font=('Verdana', 15),
                                                  labelanchor='n')

        # LABELFRAME per creazione bottoni per i tagli suino
        self.labelframe_taglio = tk.LabelFrame(self.frame_dx,
                                               text="TAGLIO",
                                               font=('Verdana', 15),
                                               labelanchor='n')

        # LABEL che mostra il progressivo lotto
        self.label_lotto = tk.Label(self.frame_alto_sx,
                                    text="PROGRESSIVO LOTTO",
                                    foreground='blue',
                                    font=('Verdana', 15))

        self.label_prog_lotto = tk.Label(self.frame_alto_sx,
                                         anchor='center',
                                         relief='ridge',
                                         bg='white',
                                         text=str(self.prog_lotto_acq)+'A',
                                         font=('Verdana', 15),
                                         padx=35)

        # LABEL che mostra la data ingresso merce
        self.label_data_ingresso = tk.Label(self.frame_alto_sx,
                                            text="DATA INGRESSO MERCE",
                                            foreground='blue',
                                            font=('Verdana', 15))
        # DATEPICKER
        self.picker = Datepicker(self.frame_alto_sx, datevar=self.data, dateformat='%d-%m-%Y',)

        # ENTRY per immissione numero ddt/fattura
        self.label_num_ddt = tk.Label(self.frame_alto_sx,
                                      text='NUMERO DDT/FATTURA',
                                      foreground='blue',
                                      font=('Verdana', 15))

        self.num_ddt = tk.StringVar()
        self.entry_ddt = ttk.Entry(self.frame_alto_sx,
                                   textvariable=self.num_ddt,
                                   width=25)
        self.entry_ddt.focus()

        # ENTRY per inserimento del peso
        self.label_peso = ttk.Label(self.frame_alto_sx,
                                    text="INSERIMENTO PESO",
                                    foreground='blue',
                                    font=('Verdana', 15))

        self.entry = ttk.Entry(self.frame_alto_sx,
                               textvariable=self.peso,
                               width=25)

        # BOTTONI salva e chiudi finestra
        self.btn_invio = tk.Button(self.frame_basso,
                                   text="Invio",
                                   font=('Verdana', 20),
                                   width=18,
                                   command=self.invio)

        self.btn_salva_esci = tk.Button(self.frame_basso,
                                        text="Salva ed esci",
                                        font=('Verdana', 20),
                                        width=18,
                                        command=self.salva_esci)

        self.btn_chiudi_finestra = tk.Button(self.frame_basso,
                                             text='Chiudi finestra',
                                             font=('Verdana', 20),
                                             width=18,
                                             command=self.chiudi)

        # BOTTONE rimuovi riga dal treeview riepilogativo
        self.btn_rimuovi_riga = tk.Button(self.frame_alto_dx,
                                          text="Rimuovi riga",
                                          command=self.rimuovi_riga_selezionata)

        # LAYOUT
        self.frame_alto_sx.grid(row=0, column=1)
        self.frame_alto_dx.grid(row=0, column=2)
        self.frame_sx.grid(row=1, column=1)
        self.frame_dx.grid(row=1, column=2)
        self.frame_basso.grid(row=2, column=1, columnspan=2)

        self.tree.grid(row=1, column=2, rowspan=4, padx=10)

        self.labelframe_fornitori.grid(row=2, column=0, sticky='n')
        self.labelframe_taglio.grid(row=1, column=0)

        self.label_lotto.grid(row=1, column=0, sticky='w')
        self.label_prog_lotto.grid(row=1, column=1)
        self.label_data_ingresso.grid(row=2, column=0, sticky='w')
        self.picker.grid(row=2, column=1)

        self.label_num_ddt.grid(row=3, column=0, sticky='w')
        self.entry_ddt.grid(row=3, column=1)

        self.label_peso.grid(row=4, column=0, sticky='w')
        self.entry.grid(row=4, column=1)

        self.btn_invio.grid(row=2, column=0, padx=5, pady=10)
        self.btn_salva_esci.grid(row=2, column=1, padx=5, pady=10)
        self.btn_chiudi_finestra.grid(row=2, column=2, padx=5, pady=10)
        self.btn_rimuovi_riga.grid(row=5, column=2, sticky='we')

        self.crea_bottoni_tagli()
        self.crea_bottoni_fornitori()

    def rimuovi_riga_selezionata(self):
            curitem = self.tree.selection()[0]
            self.tree.delete(curitem)

    def crea_bottoni_fornitori(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_fornitori)):
            if row % 6 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_fornitori,
                           text=str(self.lista_fornitori[i]).upper(),
                           variable=self.fornitore,
                           width=20,
                           indicatoron=0,
                           value=self.lista_fornitori[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

    def crea_bottoni_tagli(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_tagli)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_taglio,
                           text=self.lista_tagli[i],
                           indicatoron=0,
                           width=15,
                           variable=self.taglio_s,
                           value=self.lista_tagli[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

    def invio(self):
        self.tree.insert("", 'end', values=((str(self.prog_lotto_acq)+'A'),
                                            datetime.datetime.strptime(self.data.get(), "%d-%m-%Y").date(),
                                            self.num_ddt.get(),
                                            self.fornitore.get(),
                                            self.taglio_s.get(),
                                            self.peso.get(),
                                            self.peso.get(),
                                            'no'))
        self.entry.delete(0, tk.END)

    def salva_esci(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        self.c.executemany('INSERT INTO ingresso_merce VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_acq = %s', (self.prog_lotto_acq + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def chiudi(self):
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()
