import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import datetime as dt
import mysql.connector
import shutil
import os

'''
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
		self.geometry("+0+0")
		self.title('Lotti in vendita Cucina')

		self.conn = mysql.connector.connect(host='192.168.0.100',
		                                    database='data',
		                                    user='root',
		                                    password='')
		self.c = self.conn.cursor()

		self.data = dt.date.today()
		self.item = ''

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
		self.tree = ttk.Treeview(self.frame_sx, height=16)
		self.tree['columns'] = 'peso'

		self.tree.heading('peso', text="peso")

		self.tree.column("peso", width=80)

		self.tree.tag_configure('odd', background='light green')
		self.tree.bind("<Double-1>", self.ondoubleclick)

		# Label
		self.label_selezionato = ttk.Label(self.frame_dx, text='Prodotto selezionato', font=('Helvetica', 20))
		# self.label_dettagli = ttk.Label(self.frame_dx, text='Dettagli prodotto selezionato', font=('Helvetica', 20))

		# LABELFRAME dettagli prodotto selezionato
		self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_dx,
		                                                     text='INGREDIENTI')

		# LABELFRAME plu prodotto selezionato
		self.lblfrm_plu_prod_sel = ttk.LabelFrame(self.frame_dx, text='PLU')

		# LABEL plu prodotto selezionato
		# self.lbl_plu_selezionato = ttk.Label(self.lblfrm_plu_prod_sel,
		                                     # borderwidth=3,
		                                     # relief='solid',
		                                     # text='PLU',
		                                     # font=('Helvetica', 20))
		self.lbl_txt_plu_selezionato = ttk.Label(self.lblfrm_plu_prod_sel,
		                                         text='---',
		                                         font=('Helvetica', 20))

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
		                                 font=('Helvetica', 20),
		                                 command=self.crea_file)

		# PROGRESS BAR
		self.progress_bar = ttk.Progressbar(self.frame_dx_basso, orient=tk.HORIZONTAL, mode='determinate')

		# LAYOUT
		self.frame_sx.grid(row=0, column=0, rowspan=2)
		self.frame_dx.grid(row=0, column=1)
		self.frame_dx_basso.grid(row=1, column=1)

		self.tree.grid(row=1, column=0)

		self.label_selezionato.grid(row=0, column=0, columnspan=2)
		self.tree_selezionato.grid(row=2, column=0, columnspan=2)

		# self.label_dettagli.grid(row=3, column=0, columnspan=2)
		self.lbl_frame_dettagli_selezionato.grid(row=3, column=0, columnspan=2, rowspan=2)

		self.lblfrm_plu_prod_sel.grid(row=3, column=3, sticky='n')
		# self.lbl_plu_selezionato.grid(row=0, column=0, padx=20)
		self.lbl_txt_plu_selezionato.grid(row=1, column=0, padx=20)

		self.btn_stp_etichetta.grid(row=4, column=3)

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
			# lbl = ttk.Label(self.lbl_frame_dettagli_selezionato, text=campo)
			# lbl.grid(row=r, column=c)
			# self.label[campo] = lbl

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
			self.lbl_txt_plu_selezionato['text'] = self.row[3][-3:]
			for campo in self.ingredienti:
				self.entry[campo].delete(0, 'end')

			i = 25
			while i != 29:
				for campo in self.ingredienti:
					self.entry[campo].insert(0, self.row[i])
					i += 1

	def stp_etichetta(self):
		pagesize = (54 * mm, 101 * mm)
		d = canvas.Canvas("Eti_anagrafica.pdf", pagesize=pagesize)
		d.rotate(90)
		d.setFont('Helvetica', 20)
		d.drawString(2 * mm, -8 * mm, (self.tree.item(self.item, 'text').upper()))
		self.c.execute("SELECT * FROM prodotti WHERE Prodotto = %s", (self.tree.item(self.item, 'text'),))
		for self.row in self.c:

			d.setFont('Helvetica', 15)
			d.drawString(2 * mm, -18 * mm, self.row[25])
			d.drawString(2 * mm, -23 * mm, self.row[26])
			d.drawString(2 * mm, -28 * mm, self.row[27])
			d.setFont('Helvetica', 10)
			# d.drawString(2 * mm, -33 * mm, self.tree.parent(self.item))
			d.drawString(2 * mm, -45 * mm, '€/Kg ')
			d.setFont('Helvetica', 25)
			d.drawString(20 * mm, -45 * mm, str("%.2f" % (float(self.row[4])/100)))
			d.setFont('Helvetica', 12)
			d.drawString(80 * mm, -45 * mm, 'PLU')
			d.setFont('Helvetica', 15)
			d.drawString(90 * mm, -45 * mm, self.row[3][-3:])

		d.showPage()
		d.save()
		win32api.ShellExecute(None, "print", "Eti_anagrafica.pdf", '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)

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
		campo3 = ('0' * (6 - (len(str(self.row[4])))) + str(self.row[4]))  # prezzo
		campo4 = (str(self.row[13]) + '000011')
		campo5 = ('40' + str(self.row[1] + ' ' * (41 - (len(self.row[1])))).upper())
		campo6 = ('0' * (4 - len(str(self.row[11]))) + str(self.row[11]))
		campo7 = ('0' * 6)
		campo8 = ('0' * 3)
		campo9 = '0'
		campo10 = '00'
		campo11 = '1'
		campo12 = '1'  # campo per la sovrascrittura prezzo
		campo13 = '0'
		campo14 = '@'
		campo15 = (self.data.strftime('%d%m%y'))
		campo16 = ('A' + '\n')
		stringa = (
				campo1 + campo2 + campo3 + campo4 + campo5 + campo6 + campo7 + campo8 + campo9 + campo10 + campo11 +
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
		campo3 = (str(self.row[1]).upper() + ' ' * (50 - (len(self.row[1]))))
		campo4 = '4'
		campo5 = ('Ingredienti' + ' ' * 39)
		campo6 = (str(self.row[29]))
		campo7 = (str(self.row[25]) + ' ' * (50 - (len(self.row[25]))))
		campo8 = (str(self.row[30]))
		campo9 = (str(self.row[26]) + ' ' * (50 - (len(self.row[26]))))
		campo10 = (str(self.row[31]))
		campo11 = (str(self.row[27]) + ' ' * (50 - (len(self.row[27]))))
		campo12 = (str(self.row[32]))
		campo13 = (str(self.row[28]) + ' ' + self.tree.parent(self.item) + ' ' * (45 - (len(self.row[28]))))
		campo14_15 = ('0' + ' ' * 50)
		campo16_17 = ('0' + ' ' * 50)
		campo18_19 = ('0' + ' ' * 50)
		campo20_21 = ('0' + ' ' * 50)
		campo22 = (self.data.strftime('%d%m%y') + '\n')
		stringa = (
				campo1 + campo2 + campo3 + campo4 + campo5 + campo6 + campo7 + campo8 + campo9 + campo10 + campo11 +
				campo12 + campo13 + campo14_15 + campo16_17 + campo18_19 + campo20_21 + campo22)
		f = open('../laboratorio/bz00vate.dat', "w")
		f.write(stringa)
		f.close()


if __name__ == "__main__":
	root = tk.Tk()
	new = LottiInVenditaCucina()
	root.mainloop()
