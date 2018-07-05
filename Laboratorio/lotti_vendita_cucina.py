import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import mysql.connector
'''
import shutil
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Spacer,
                                Table, TableStyle, Paragraph)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
'''
import win32api
import win32print
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
# from tkinter import messagebox


class LottiInVenditaCucina(tk.Toplevel):
    def __init__(self):
        super(LottiInVenditaCucina, self).__init__()
        self.geometry("1024x525+0+0")
        self.title('Lotti in vendita Cucina')

        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.data = dt.date.today()

        self.campi = ['plu', 'prezzo1', 'prezzo2', 'prezzo3', 'prezzo4', 'prezzo_straord', 'gruppo_merc', 'tara',
                      'gg_cons_1', 'gg_cons_2', 'ean', 'testo_agg_1', 'testo_agg_2', 'testo_agg_3', 'testo_agg_4',
                      'pz_x_scatola', 'peso_fisso', 'num_offerta', 'art_in_pubblic', 'sovrascritt_prezzo',
                      'stile_tracc', 'rich_stm_traccia']
        self.formati = ['formato_1', 'formato_2', 'formato_3', 'formato_4']
        self.ingredienti = ['riga_1', 'riga_2', 'riga_3', 'riga_4']
        self.label = {}
        self.entry = {}

        # Disposizione Frame e LabelFrame
        self.frame_sx = tk.Frame(self)
        self.frame_dx = tk.Frame(self)
        self.frame_dx_basso = tk.Frame(self, background='white')

        # Treeview con lotti disponibili
        self.tree = ttk.Treeview(self.frame_sx, height=23)
        self.tree['columns'] = 'peso'

        self.tree.heading('peso', text="peso")

        self.tree.column("peso", width=80)

        self.tree.tag_configure('odd', background='light green')
        self.tree.bind("<Double-1>", self.ondoubleclick)

        # Label
        self.label_selezionato = ttk.Label(self.frame_dx, text='Prodotto selezionato', font=('Helvetica', 20))
        self.label_dettagli = ttk.Label(self.frame_dx, text='Dettagli prodotto selezionato', font=('Helvetica', 20))

        # LABELFRAME dettagli prodotto selezionato
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_dx,
                                                             text='Dettagli prodotto selezionato')

        # Treeview con prodotto selezionato
        self.tree_selezionato = ttk.Treeview(self.frame_dx, height=1)
        self.tree_selezionato['columns'] = ('lotto', 'prodotto')
        self.tree_selezionato['show'] = 'headings'
        self.tree_selezionato.heading('lotto', text="lotto")
        self.tree_selezionato.heading('prodotto', text="prodotto")

        self.tree_selezionato.column("lotto", width='90')
        self.tree_selezionato.column("prodotto", width='180')

        # Button stampa etichetta
        self.btn_stp_etichetta = tk.Button(self.frame_dx,
                                           text='Stampa Etichetta',
                                           state='disabled',
                                           font=('Helvetica', 10),
                                           command=self.stp_etichetta)

        # BUTTON uscita
        self.btn_uscita = tk.Button(self.frame_dx_basso,
                                    text='Chiudi finestra',
                                    font=('Helvetica', 20),
                                    command=self.destroy)

        # BUTTON manda in bilancia
        self.btn_in_bilancia = tk.Button(self.frame_dx_basso,
                                         text='Invia in bilancia',
                                         font=('Helvetica', 20))

        # PROGRESS BAR
        self.progress_bar = ttk.Progressbar(self.frame_dx_basso, orient=tk.HORIZONTAL, mode='determinate')

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, rowspan=2)
        self.frame_dx.grid(row=0, column=1)
        self.frame_dx_basso.grid(row=1, column=1)

        self.tree.grid(row=1, column=0)

        self.label_selezionato.grid(row=0, column=0, columnspan=2)
        self.tree_selezionato.grid(row=2, column=0, columnspan=2)

        self.label_dettagli.grid(row=3, column=0, columnspan=2)
        self.lbl_frame_dettagli_selezionato.grid(row=3, column=0, columnspan=2)

        self.btn_stp_etichetta.grid(row=4, column=0)

        self.btn_in_bilancia.grid(row='0', column='0', padx='20', pady='20')
        self.btn_uscita.grid(row='0', column='1', padx='20', pady='20')
        self.progress_bar.grid(row='1', column='0', columnspan='2', sticky='we')

        self.riempi_tutti()
        self.crea_label_formato_ingredienti()

    def crea_label_formato_ingredienti(self):
        r = 2
        c = 0
        for campo in self.ingredienti:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_dettagli_selezionato, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.lbl_frame_dettagli_selezionato, width='50')
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

    def riempi_tutti(self):
        self.tree.delete(*self.tree.get_children())

        self.c.execute("SELECT DISTINCT progressivo_ven_c,prodotto,quantita,data_prod "
                       "FROM lotti_vendita_cucina "
                       "ORDER BY data_prod DESC")
        for lista in self.c:
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(lista[2]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(lista[2]))
                self.tree.item(lista[0], open='true')

    def ondoubleclick(self, event):
        self.btn_stp_etichetta['state'] = 'normal'
        self.tree_selezionato.delete(*self.tree_selezionato.get_children())
        self.item = self.tree.selection()[0]
        self.tree_selezionato.insert('', 'end',
                                     values=(self.tree.parent(self.item), (self.tree.item(self.item, 'text'))))

        self.c.execute("SELECT * FROM prodotti WHERE Prodotto = %s", (self.tree.item(self.item, 'text'),))
        for self.row in self.c:
            print(self.row)

            for campo in self.ingredienti:
                self.entry[campo].delete(0, 'end')

            i = 25
            while i != 29:
                for campo in self.ingredienti:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1

    def stp_etichetta(self):
        pagesize = (54*mm, 101*mm)
        d = canvas.Canvas("Eti_anagrafica.pdf", pagesize=pagesize)
        d.rotate(90)
        d.drawString(2*mm, -8*mm, (self.tree.item(self.item, 'text').upper()))
        self.c.execute("SELECT * FROM prodotti WHERE Prodotto = %s", (self.tree.item(self.item, 'text'),))
        for self.row in self.c:
            d.drawString(2*mm, -18*mm, self.row[25])
            d.drawString(2*mm, -23*mm, self.row[26])
            d.drawString(2*mm, -28*mm, self.row[27])
            d.drawString(2*mm, -33*mm, self.tree.parent(self.item))
        d.showPage()
        d.save()
        win32api.ShellExecute(None, "print", "Eti_anagrafica.pdf", '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)


if __name__ == "__main__":
    root = tk.Tk()
    new = LottiInVenditaCucina()
    root.mainloop()
