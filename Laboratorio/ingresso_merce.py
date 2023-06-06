import tkinter as tk
from tkinter import ttk
from datepicker import Datepicker
import datetime
import mysql.connector
from tastiera_num import Tast_num
import configparser


class IngressoMerce(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)

        self.geometry("+125+125")

        self.title("Ingresso Merce")

        self.config = self.leggi_file_ini()

        # Connessione al database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        # Lettura progressivo lotto acquisto da db
        self.c.execute("SELECT prog_acq FROM progressivi")
        self.prog_lotto_acq = self.c.fetchone()[0]

        # Inizializzazione lista per valori da salvare sul database
        self.lista_da_salvare = []
        self.fornitore = tk.StringVar()
        self.taglio_s = tk.StringVar()
        self.peso = tk.StringVar()
        self.data = tk.StringVar()
        self.data.set(datetime.date.today().strftime('%d-%m-%Y'))

        self.img_btn = tk.PhotoImage(file=".//immagini//modifica.gif")

        # Creazione liste fornitori
        self.lista_fornitori = []
        self.c.execute("SELECT azienda FROM fornitori WHERE flag1_ing_merce = 1")

        for row in self.c:
            self.lista_fornitori.extend(row)
            
        # Creazione lista tagli suino
        self.lista_tagli = []
        self.c.execute("SELECT taglio FROM tagli WHERE id_merceologia = 11")

        for row in self.c:
            self.lista_tagli.extend(row)

        # LAYOUT dei frame per impaginazione
        self.frame_alto = tk.Frame(self, bd=3)
        self.frame_centrale = tk.Frame(self, bd=3)
        self.frame_basso = tk.Frame(self)

        # TREEVIEW per riepilogo inserimenti
        self.tree = ttk.Treeview(self.frame_alto, height=8)

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

        # LABELFRAME contiene bottoni per scelta fornitore
        self.labelframe_fornitori = tk.LabelFrame(self.frame_centrale,
                                                  text="FORNITORE",
                                                  font=('Verdana', 15),
                                                  labelanchor='n')

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

        # LABELFRAME contiene bottoni per i tagli suino

        
        self.labelframe_taglio = tk.LabelFrame(self.frame_centrale,
                                               text="TAGLIO",
                                               font=('Verdana', 15),
                                               labelanchor='n')

        self.notebook = ttk.Notebook(self.labelframe_taglio)

        # TAB 1 AGNELLO
        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='AGNELLO', state='disabled',
                          compound='left', image=self.img_btn1)

        lst_agnello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 12")
        for row in self.c:
            lst_agnello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_agnello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab1,
                text=lst_agnello[i].upper(),
                indicatoron=0,
                variable=self.taglio_s,
                font='Verdana',
                width=20,
                value=lst_agnello[i]).grid(row=r, column=c)
            r += 1

        # TAB 2 BOVINO
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='BOVINO', state='disabled',
                          compound='left', image=self.img_btn1)

        lst_bovino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 10")
        for row in self.c:
            lst_bovino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_bovino)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab2,
                text=lst_bovino[i].upper(),
                indicatoron=0,
                variable=self.taglio_s,
                font='Verdana',
                width=20,
                value=lst_bovino[i]).grid(row=r, column=c)
            r += 1

        # TAB 3 SUINO
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='SUINO',
                          compound='left', image=self.img_btn1)

        lst_suino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 11")
        for row in self.c:
            lst_suino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_suino)):
            if r % 8 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab3,
                text=lst_suino[i].upper(),
                indicatoron=0,
                variable=self.taglio_s,
                font='Verdana',
                width=20,
                value=lst_suino[i]).grid(row=r, column=c)
            r += 1

        # TAB 4 VITELLO
        self.tab4 = tk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='VITELLO', state='disabled',
                          compound='left', image=self.img_btn1)

        lst_vitello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 13")
        for row in self.c:
            lst_vitello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_vitello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab4,
                text=lst_vitello[i].upper(),
                indicatoron=0,
                variable=self.taglio_s,
                font='Verdana',
                width=20,
                value=lst_vitello[i]).grid(row=r, column=c)
            r += 1

        # LABEL che mostra il progressivo lotto
        self.label_lotto = tk.Label(self.frame_alto,
                                    text="PROGRESSIVO LOTTO",
                                    foreground='blue',
                                    font=('Verdana', 15))

        self.label_prog_lotto = tk.Label(self.frame_alto,
                                         anchor='center',
                                         relief='ridge',
                                         bg='white',
                                         text=str(self.prog_lotto_acq)+'A',
                                         font=('Verdana', 15),
                                         padx=35)

        # LABEL che mostra la data ingresso merce
        self.label_data_ingresso = tk.Label(self.frame_alto,
                                            text="DATA INGRESSO MERCE",
                                            foreground='blue',
                                            font=('Verdana', 15))
        # DATEPICKER
        self.picker = Datepicker(self.frame_alto, datevar=self.data, dateformat='%d-%m-%Y',)

        # ENTRY per immissione numero ddt/fattura
        self.label_num_ddt = tk.Label(self.frame_alto,
                                      text='NUMERO DDT/FATTURA',
                                      foreground='blue',
                                      font=('Verdana', 15))

        self.num_ddt = tk.StringVar()
        self.entry_ddt = ttk.Entry(self.frame_alto,
                                   textvariable=self.num_ddt,
                                   width=25)

        self.btn_ins_num_ddt = ttk.Button(self.frame_alto, image=self.img_btn, command=self._ins_num_ddt)

        self.entry_ddt.focus()

        # ENTRY per inserimento del peso
        self.label_peso = tk.Label(self.frame_alto,
                                    text="INSERIMENTO PESO",
                                    foreground='blue',
                                    font=('Verdana', 15))

        self.entry = tk.Entry(self.frame_alto,
                               textvariable=self.peso,
                               width=25)

        self.btn_ins_peso = tk.Button(self.frame_alto, image=self.img_btn, command=self._ins_peso)

        # BOTTONI salva e chiudi finestra
        self.btn_invio = tk.Button(self.frame_basso,
                                   text="INVIO",
                                   font=('Verdana', 15),
                                   width=18,
                                   command=self._invio)

        self.btn_salva_esci = tk.Button(self.frame_basso,
                                        text="SALVA ed ESCI",
                                        font=('Verdana', 15),
                                        width=18,
                                        command=self._salva_esci)

        self.btn_chiudi_finestra = tk.Button(self.frame_basso,
                                             text='CHIUDI FINESTRA',
                                             font=('Verdana', 15),
                                             width=18,
                                             command=self._chiudi)

        # BOTTONE rimuovi riga dal treeview riepilogativo
        self.btn_rimuovi_riga = tk.Button(self.frame_alto,
                                          text="RIMUOVI RIGA",
                                          command=self._rimuovi_riga_selezionata)

        # LAYOUT
        self.frame_alto.grid(row=0, column=1)
        self.frame_centrale.grid(row=1, column=1)
        self.frame_basso.grid(row=2, column=1, columnspan=2)

        self.tree.grid(row=1, column=3, rowspan=4, padx=10)

        self.labelframe_fornitori.grid(row=1, column=0, sticky='n')
        self.labelframe_taglio.grid(row=1, column=1)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky='we')

        self.label_lotto.grid(row=1, column=0, sticky='w')
        self.label_prog_lotto.grid(row=1, column=1)
        self.label_data_ingresso.grid(row=2, column=0, sticky='w')
        self.picker.grid(row=2, column=1)

        self.label_num_ddt.grid(row=3, column=0, sticky='w')
        self.entry_ddt.grid(row=3, column=1)
        self.btn_ins_num_ddt.grid(row=3, column=2)

        self.label_peso.grid(row=4, column=0, sticky='w')
        self.entry.grid(row=4, column=1)
        self.btn_ins_peso.grid(row=4, column=2)

        self.btn_invio.grid(row=0, column=0, sticky='we')
        self.btn_salva_esci.grid(row=0, column=1, sticky='we')
        self.btn_chiudi_finestra.grid(row=0, column=2, sticky='we')
        self.btn_rimuovi_riga.grid(row=5, column=3, sticky='we')

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def _rimuovi_riga_selezionata(self):
            curitem = self.tree.selection()[0]
            self.tree.delete(curitem)

    def _invio(self):
        self.tree.insert("", 'end', values=((str(self.prog_lotto_acq)+'A'),
                                            datetime.datetime.strptime(self.data.get(), "%d-%m-%Y").date(),
                                            self.num_ddt.get(),
                                            self.fornitore.get(),
                                            self.taglio_s.get(),
                                            self.peso.get(),
                                            self.peso.get(),
                                            'no'))
        self.entry.delete(0, tk.END)

    def _salva_esci(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        self.c.executemany('INSERT INTO ingresso_merce VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_acq = %s', (self.prog_lotto_acq + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def _ins_peso(self):
        peso = Tast_num(self)
        val = peso.value.get()
        self.peso.set(val)

    def _ins_num_ddt(self):
        ddt_num = Tast_num(self)
        val = ddt_num.value.get()
        self.num_ddt.set(val)

    def _chiudi(self):
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = IngressoMerce()
    root.mainloop()
