import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import mysql.connector
import shutil
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Spacer,
                                Table, TableStyle, Paragraph)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import win32api
from tkinter import messagebox


class LottiInVendita(tk.Toplevel):
    def __init__(self):
        super(LottiInVendita, self).__init__()
        self.geometry("1024x525+0+0")
        self.title('Lotti in vendita')

        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.data = dt.date.today()

        self.item = ''
        self.tot_qta = 0

        # Disposizione Frame e LabelFrame
        self.frame_sx = tk.Frame(self)
        self.frame_dx = tk.Frame(self)
        self.frame_dx_basso = tk.Frame(self, background='white')

        self.lblframe_box = ttk.LabelFrame(self.frame_dx, text='visualizza lotti per articolo')

        # Treeview con lotti disponibili
        self.tree = ttk.Treeview(self.frame_sx, height=23)
        self.tree['columns'] = ('data', 'peso')

        self.tree.heading('data', text="data")
        self.tree.heading('peso', text="peso")

        self.tree.column("data", width=80)
        self.tree.column("peso", width=80)

        self.tree.tag_configure('odd', background='light green')

        self.tree.bind("<Double-1>", self.ondoubleclick)

        # Label
        self.label = ttk.Label(self.frame_sx, text='Lotti disponibili alla vendita', font=('Helvetica', 20))
        self.label_selezionato = ttk.Label(self.frame_dx, text='Lotto selezionato', font=('Helvetica', 20))
        self.label_dettagli = ttk.Label(self.frame_dx, text='Dettagli lotto selezionato', font=('Helvetica', 20))

        # Posizionamento Label

        self.label_selezionato.grid(row='1', column='0', columnspan='2')
        self.label_dettagli.grid(row='3', column='0', columnspan='2')

        # Treeview con lotto selezionato
        self.tree_selezionato = ttk.Treeview(self.frame_dx, height=1)
        self.tree_selezionato['columns'] = ('lotto', 'prodotto')
        self.tree_selezionato['show'] = 'headings'
        self.tree_selezionato.heading('lotto', text="lotto")
        self.tree_selezionato.heading('prodotto', text="prodotto")

        self.tree_selezionato.column("lotto", width='90')
        self.tree_selezionato.column("prodotto", width='180')

        # BUTTON per stampare pdf del lotto selezionato
        self.btn_stampa_pdf = ttk.Button(self.frame_dx,
                                         text='Stampa PDF',
                                         command=self.crea_pdf)

        # Treeview con DETTAGLI lotto selezionato
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

        # LABEL quantita totale
        self.lbl_txt_quantita = ttk.Label(self.frame_dx,
                                          text='Quantita prodotta nel periodo selezionato KG :',
                                          font=('Helvetica', 15))
        self.lbl_peso_totale = ttk.Label(self.frame_dx,
                                         text='0',
                                         font=('Helvetica', 20))

        self.lbl_txt_quantita.grid(row=6, column=0, pady=5, padx=20)
        self.lbl_peso_totale.grid(row=7, column=0, padx=20)

        # BUTTON uscita
        self.btn_uscita = tk.Button(self.frame_dx_basso,
                                    text='Chiudi finestra',
                                    font=('Helvetica', 20),
                                    command=self.destroy)

        # BUTTON manda in bilancia
        self.btn_in_bilancia = tk.Button(self.frame_dx_basso,
                                         text='Invia in bilancia',
                                         font=('Helvetica', 20),
                                         command=self.crea_file)

        # RADIOBUTTON
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
        self.rdbtn_6mesi = tk.Radiobutton(self.lblframe_box, text='Ultimi 180 giorni',
                                          variable=self.filtro_mese, value=6)
        self.rdbtn_1mese.grid(row=1, column=0, padx=5)
        self.rdbtn_2mesi.grid(row=1, column=1, padx=5)
        self.rdbtn_3mesi.grid(row=1, column=2, padx=5)
        self.rdbtn_6mesi.grid(row=1, column=3, padx=5)

        # Combobox per gestire rimpimento tramite lista prodotti
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.lblframe_box, textvariable=self.box_value)

        self.box.grid(row=0, column=2)

        # BOTTONE Filtra
        self.btn_filtra = ttk.Button(self.lblframe_box, text='Filtra', command=self.filtra)
        self.btn_filtra.grid(row=0, column=3, padx=20)

        # PROGRESS BAR
        self.progress_bar = ttk.Progressbar(self.frame_dx_basso, orient=tk.HORIZONTAL, mode='determinate')

        # LAYOUT
        self.frame_sx.grid(row='0', column='0', rowspan='2')
        self.frame_dx.grid(row='0', column='1')
        self.frame_dx_basso.grid(row='1', column='1')
        self.lblframe_box.grid(row='5', column='0', columnspan='2')

        self.label.grid(row='0', column='0')
        self.tree.grid(row='1', column='0')

        self.tree_selezionato.grid(row='2', column='0', columnspan='2')
        self.btn_stampa_pdf.grid(row='2', column='1', sticky='we')
        self.tree_dettagli.grid(row='4', column='0', columnspan='2')

        self.btn_in_bilancia.grid(row='0', column='0', padx='20', pady='20')
        self.btn_uscita.grid(row='0', column='1', padx='20', pady='20')
        self.progress_bar.grid(row='1', column='0', columnspan='2', sticky='we')

        self.riempi_combo()
        self.riempi_tutti()

    def riempi_combo(self):
        lista = []

        self.c.execute("SELECT prodotto From prodotti WHERE reparto = %s", (self.filtro.get(),))
        for row in self.c:
            lista.extend(row)
        self.box['values'] = lista

        self.box.current(0)

    def filtra(self):
        self.tot_qta = 0
        self.tree.delete(*self.tree.get_children())
        giorni = self.data - dt.timedelta(days=31*int(self.filtro_mese.get()))

        self.c.execute("SELECT DISTINCT progressivo_ven,prodotto,data_ven,quantita "
                       "FROM lotti_vendita "
                       "WHERE prodotto = %s"
                       "AND lotti_vendita.data_ven > %s"
                       "ORDER BY data_ven DESC", (self.box_value.get(), giorni))
        for lista in self.c:
            self.tot_qta += float(lista[3])
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(dt.date.strftime(lista[2], '%d/%m/%y'), lista[3]))
                self.tree.item(lista[0], open='true')
        self.lbl_peso_totale['text'] = "{0:.2f}".format(round(self.tot_qta, 2))

    def riempi_tutti(self):
        self.tree.delete(*self.tree.get_children())

        self.c.execute("SELECT DISTINCT progressivo_ven,prodotto,data_ven,quantita "
                       "FROM lotti_vendita "
                       "ORDER BY data_ven DESC, progressivo_ven DESC")
        for lista in self.c:
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

        self.c.execute("SELECT DISTINCT prod_origine, lotto_acq,fornitore,documento,data_acq "
                       "FROM lotti_vendita  JOIN ingresso_merce "
                       "WHERE progressivo_ven = %s "
                       "AND lotti_vendita.lotto_acq = ingresso_merce.progressivo_acq",
                       (self.tree.parent(self.item),))
        for lista in self.c:
            self.tree_dettagli.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[3],
                                                         dt.date.strftime(lista[4], '%d/%m/%y')))

    def crea_file(self):
        path = '//192.168.0.224/c/WinSwGx-NET//bizvar/LABORATORIO/'
        if not os.listdir(path):
            self.crea_bz00varp()
            self.progress_bar['value'] = 25
            self.crea_bz00vate()
            self.progress_bar['value'] = 50
            shutil.move('../laboratorio/bz00varp.dat', path)
            self.progress_bar['value'] = 75
            shutil.move('../laboratorio/bz00vate.dat', path)
            self.progress_bar['value'] = 100
            # os.startfile("//192.168.0.224/C/WinSwGx-NET/cofraggpscon.exe")
        else:
            messagebox.showinfo('Attenzione', 'Ci sono file di variazioni presenti nella cartella \n '
                                              'fare un invio in bilancia ')

    def crea_bz00varp(self):
        self.c.execute("SELECT * FROM prodotti "
                       "WHERE prodotto = %s", (self.tree.item(self.item, 'text'),))
        for self.row in self.c:
            pass
        campo1 = ('0' + str(self.row[3]))
        campo2 = ('000' + str(self.row[9]))
        campo3 = ('0'*6)
        campo4 = (str(self.row[13]) + '000011')
        campo5 = ('40' + str(self.row[1] + ' '*(41-(len(self.row[1])))).upper())
        campo6 = ('0'*(4-len(str(self.row[11]))) + str(self.row[11]))
        campo7 = ('0'*6)
        campo8 = ('0'*3)
        campo9 = '0'
        campo10 = '00'
        campo11 = '1'
        campo12 = '1'  # campo per la sovrascrittura prezzo
        campo13 = '0'
        campo14 = '@'
        campo15 = (self.data.strftime('%d%m%y'))
        campo16 = ('A' + '\n')
        stringa = (campo1 + campo2 + campo3 + campo4 + campo5 + campo6 + campo7 + campo8 + campo9 + campo10 + campo11 +
                   campo12 + campo13 + campo14 + campo15 + campo16)
        f = open('../laboratorio/bz00varp.dat', "w")
        f.write(stringa)
        f.close()

    def crea_bz00vate(self):
        self.c.execute("SELECT * FROM prodotti "
                       "WHERE prodotto = %s", (self.tree.item(self.item, 'text'),))
        for self.row in self.c:
            pass
        campo1 = ('0' + str(self.row[3]))
        campo2 = '4'
        campo3 = (str(self.row[1]).upper() + ' '*(50-(len(self.row[1]))))
        campo4 = '4'
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

    def crea_pdf(self):
        titolo = "Dettagli lotto numero " + self.tree.parent(self.item) + " " + self.tree.item(self.item, 'text')
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        data = [('Taglio', 'Lotto Ingresso', 'Fornitore', 'Documento', 'Data Acquisto')]

        self.c.execute("SELECT DISTINCT prod_origine, lotto_acq,fornitore,documento,data_acq "
                       "FROM lotti_vendita  JOIN ingresso_merce "
                       "WHERE progressivo_ven = %s "
                       "AND lotti_vendita.lotto_acq = ingresso_merce.progressivo_acq",
                       (self.tree.parent(self.item),))
        for lista in self.c:
            data.append(lista)

        doc = SimpleDocTemplate("./traccia.pdf", pagesize=A4)

        parts = []
        table_with_style = Table(data, [1 * inch, 1.7 * inch, inch])
        table_with_style.hAlign = "LEFT"

        table_with_style.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, 0), 0.25, colors.green),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'), ]))

        parts.append(Paragraph(titolo, styles["Center"]))
        parts.append(Spacer(1, 0.5 * inch))
        parts.append(table_with_style)
        doc.build(parts)
        if messagebox.askyesno('STAMPA', 'Vuoi stampare il pdf?'):
            win32api.ShellExecute(None, "print", "traccia.pdf", None, ".", 0)


if __name__ == "__main__":
    root = tk.Tk()
    new = LottiInVendita()
    root.mainloop()
