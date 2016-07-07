import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import sqlite3
import shutil
# import os


class LottiInVendita(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())
        self.title('Lotti in vendita')

        self.conn_v = sqlite3.connect('../laboratorio/data.db',
                                      detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c_v = self.conn_v.cursor()

        self.data = dt.date.today()

        self.item = ''

        '''
        Disposizione Frame e LabelFrame
        '''
        self.frame_sx = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)
        self.frame_sx.grid(row=0, column=0)
        self.frame_dx.grid(row=0, column=1)

        self.lblframe_box = ttk.LabelFrame(self.frame_dx, text='visualizza lotti per articolo')
        self.lblframe_box.grid(row=5, column=0, columnspan='2')
        '''
        Treeview con lotti disponibili
        '''
        self.tree = ttk.Treeview(self.frame_sx, height=25)
        self.tree['columns'] = ('data', 'peso')

        self.tree.heading('data', text="data")
        self.tree.heading('peso', text="peso")

        self.tree.column("data", width=80)
        self.tree.column("peso", width=80)

        self.tree.tag_configure('odd', background='light green')

        self.tree.bind("<Double-1>", self.ondoubleclick)

        '''
        Label
        '''
        self.label = ttk.Label(self.frame_sx, text='Lotti disponibili alla vendita', font="Helvetica,40")
        self.label_selezionato = ttk.Label(self.frame_dx, text='Lotto selezionato', font='Helvetica')
        self.label_dettagli = ttk.Label(self.frame_dx, text='Dettagli lotto selezionato', font='Helvetica')
        '''
        Posizionamento Label
        '''
        self.label.grid(row='0', column='0')
        self.label_selezionato.grid(row='1', column='0', columnspan=2)
        self.label_dettagli.grid(row='3', column='0', columnspan='2')
        '''
        Treeview con lotto selezionato
        '''
        self.tree_selezionato = ttk.Treeview(self.frame_dx, height=1)
        self.tree_selezionato['columns'] = ('lotto', 'prodotto')
        self.tree_selezionato['show'] = 'headings'
        self.tree_selezionato.heading('lotto', text="lotto")
        self.tree_selezionato.heading('prodotto', text="prodotto")
        '''
        Treeview con DETTAGLI lotto selezionato
        '''
        self.tree_dettagli = ttk.Treeview(self.frame_dx, height=5)
        self.tree_dettagli['columns'] = ('prod_origine', 'lotto_acq', 'fornitore', 'documento', 'data_acq')
        self.tree_dettagli['show'] = 'headings'
        self.tree_dettagli.heading('prod_origine', text="taglio")
        self.tree_dettagli.heading('lotto_acq', text="prog acquisto")
        self.tree_dettagli.heading('fornitore', text="fornitore")
        self.tree_dettagli.heading('documento', text="DDT/Fattura")
        self.tree_dettagli.heading('data_acq', text="data")

        self.tree_dettagli.column("prod_origine", width=90)
        self.tree_dettagli.column("lotto_acq", width=90)
        self.tree_dettagli.column("fornitore", width=90)
        self.tree_dettagli.column("documento", width=90)
        self.tree_dettagli.column("data_acq", width=90)

        '''
        Posizionamento Treeview
        '''
        self.tree.grid(row='1', column='0')
        self.tree_selezionato.grid(row='2', column='0', columnspan=2)
        self.tree_dettagli.grid(row='4', column='0', columnspan='2')

        '''
        Bottone uscita
        '''
        self.btn_uscita = ttk.Button(self.frame_dx, text='Chiudi finestra', command=self.destroy)
        self.btn_uscita.grid(row='6', column='1', pady='20')
        '''
        Bottone manda in bilancia
        '''
        self.btn_in_bilancia = ttk.Button(self.frame_dx, text='Invia in bilancia', command=self.crea_file)
        self.btn_in_bilancia.grid(row=6, column=0)
        '''
        RADIOBUTTON
        '''
        self.filtro = tk.StringVar()
        self.filtro.set('Macelleria')
        self.rdbtn_macelleria = tk.Radiobutton(self.lblframe_box, text='Macelleria',
                                               variable=self.filtro, value='Macelleria', command=self.riempi_combo)
        self.rdbtn_gastronomia = tk.Radiobutton(self.lblframe_box, text='Gastronomia',
                                                variable=self.filtro, value='Gastronomia', command=self.riempi_combo)
        self.rdbtn_macelleria.grid(row=0, column=0, padx=5, sticky='w')
        self.rdbtn_gastronomia.grid(row=0, column=1, padx=5, sticky='w')

        self.filtro_mese = tk.StringVar()
        self.filtro_mese.set(1)

        self.rdbtn_1mese = tk.Radiobutton(self.lblframe_box, text='Ultimi 30 giorni',
                                          variable=self.filtro_mese, value=1)
        self.rdbtn_2mesi = tk.Radiobutton(self.lblframe_box, text='Ultimi 60 giorni',
                                          variable=self.filtro_mese, value=2)
        self.rdbtn_3mesi = tk.Radiobutton(self.lblframe_box, text='Ultimi 90 giorni',
                                          variable=self.filtro_mese, value=3)
        self.rdbtn_1mese.grid(row=1, column=0, padx=5)
        self.rdbtn_2mesi.grid(row=1, column=1, padx=5)
        self.rdbtn_3mesi.grid(row=1, column=2, padx=5)
        '''
        Combobox per gestire rimpimento tramite lista prodotti
        '''
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.lblframe_box, textvariable=self.box_value)

        self.box.grid(row=0, column=2)
        '''
        BOTTONE Filtra
        '''
        self.btn_filtra = ttk.Button(self.lblframe_box, text='Filtra', command=self.filtra)
        self.btn_filtra.grid(row=0, column=3, padx=20)

        self.riempi_combo()
        self.riempi_tutti()

    def riempi_combo(self):
        lista = []

        for row in self.c_v.execute("SELECT prodotto From prodotti WHERE reparto = ?", (self.filtro.get(),)):
            lista.extend(row)
        self.box['values'] = lista

        self.box.current(0)

    def filtra(self):
        self.tree.delete(*self.tree.get_children())
        giorni = self.data - dt.timedelta(days=31*int(self.filtro_mese.get()))
        for lista in self.c_v.execute("SELECT DISTINCT progressivo_ven,prodotto,data_ven,quantita "
                                      "FROM lotti_vendita "
                                      "WHERE prodotto = ?"
                                      "AND lotti_vendita.data_ven > ?"
                                      "ORDER BY progressivo_ven DESC", (self.box_value.get(), giorni)):
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')

    def riempi_tutti(self):
        self.tree.delete(*self.tree.get_children())
        for lista in self.c_v.execute("SELECT DISTINCT progressivo_ven,prodotto,data_ven,quantita "
                                      "FROM lotti_vendita "
                                      "ORDER BY progressivo_ven DESC"):
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')

    def ondoubleclick(self, event):
        self.tree_selezionato.delete(*self.tree_selezionato.get_children())
        self.tree_dettagli.delete(*self.tree_dettagli.get_children())
        self.item = self.tree.selection()[0]
        self.tree_selezionato.insert('', 'end',
                                     values=(self.tree.parent(self.item), (self.tree.item(self.item, 'text'))))

        for lista in self.c_v.execute("SELECT DISTINCT prod_origine, lotto_acq,fornitore,documento,data_acq "
                                      "FROM lotti_vendita  JOIN ingresso_merce "
                                      "WHERE progressivo_ven = ? "
                                      "AND lotti_vendita.lotto_acq = ingresso_merce.progressivo_acq",
                                      (self.tree.parent(self.item),)):
            self.tree_dettagli.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[3],
                                                         dt.date.strftime(lista[4], '%d/%m/%y')))

    def crea_file(self):
        self.crea_bz00varp()
        self.crea_bz00vate()
        shutil.move('../laboratorio/bz00varp.dat', '//192.168.0.224/c/WinSwGx-NET//bizvar/LABORATORIO/')
        shutil.move('../laboratorio/bz00vate.dat', '//192.168.0.224/c/WinSwGx-NET//bizvar/LABORATORIO/')
        # os.startfile("//192.168.0.224/C/WinSwGx-NET/cofraggpscon.exe")

    def crea_bz00varp(self):
        for self.row in self.c_v.execute("SELECT * FROM prodotti "
                                         "WHERE prodotto = ?", (self.tree.item(self.item, 'text'),)):
            pass
        campo1 = ('0' + str(self.row[3]))
        campo2 = ('000' + str(self.row[9]))
        campo3 = ('0'*6)
        campo4 = (str(self.row[13]) + '000011')
        campo5 = ('40' + str(self.row[1] + ' '*(41-(len(self.row[1])))).upper())
        campo6 = ('0'*(4-len(str(self.row[11]))) + str(self.row[11]))
        campo7 = ('0'*6)
        campo8 = ('0'*3)
        campo9 = ('0')
        campo10 = ('00')
        campo11 = ('1')
        campo12 = ('0')
        campo13 = ('0')
        campo14 = ('@')
        campo15 = (self.data.strftime('%d%m%y'))
        campo16 = ('A' + '\n')
        stringa = (campo1 + campo2 + campo3 + campo4 + campo5 + campo6 + campo7 + campo8 + campo9 + campo10 + campo11 +
                   campo12 + campo13 + campo14 + campo15 + campo16)
        f = open('../laboratorio/bz00varp.dat', "w")
        f.write(stringa)
        f.close()

    def crea_bz00vate(self):
        for self.row in self.c_v.execute("SELECT * FROM prodotti "
                                         "WHERE prodotto = ?", (self.tree.item(self.item, 'text'),)):
            pass
        campo1 = ('0' + str(self.row[3]))
        campo2 = ('4')
        campo3 = (str(self.row[1]).upper() + ' '*(50-(len(self.row[1]))))
        campo4 = ('4')
        campo5 = ('Ingredienti' + ' '*39)
        campo6 = (str(self.row[29]))
        campo7 = (str(self.row[25]) + ' '*(50-(len(self.row[25]))))
        campo8 = (str(self.row[30]))
        campo9 = (str(self.row[26]) + ' '*(50-(len(self.row[26]))))
        campo10 = (str(self.row[31]))
        campo11 = (str(self.row[27]) + ' '*(50-(len(self.row[27]))))
        campo12 = (str(self.row[32]))
        campo13 = (str(self.row[28]) + ' ' + self.tree.parent(self.item) + ' '*(45-(len(self.row[28]))))
        campo14_15 = ('0' + ' '*50)
        campo16_17 = ('0' + ' '*50)
        campo18_19 = ('0' + ' '*50)
        campo20_21 = ('0' + ' '*50)
        campo22 = (self.data.strftime('%d%m%y') + '\n')
        stringa = (campo1 + campo2 + campo3 + campo4 + campo5 + campo6 + campo7 + campo8 + campo9 + campo10 + campo11 +
                   campo12 + campo13 + campo14_15 + campo16_17 + campo18_19 + campo20_21 + campo22)
        f = open('../laboratorio/bz00vate.dat', "w")
        f.write(stringa)
        f.close()

if __name__ == "__main__":
    root = tk.Tk()
    new = LottiInVendita()
    root.mainloop()
