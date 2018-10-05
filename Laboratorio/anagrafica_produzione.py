import tkinter as tk
from tkinter import ttk
import mysql.connector
import os
import shutil
from tkinter import messagebox
import datetime as dt
import win32api
import win32print
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class Produzione(tk.Frame):
    def __init__(self, parent):
        super(Produzione, self).__init__(parent)

        self.item = ''
        self.lista_da_salvare = []
        self.data = dt.date.today()
        self.campi = ['plu', 'prezzo1', 'prezzo2', 'prezzo3', 'prezzo4', 'prezzo_straord', 'gruppo_merc', 'tara',
                      'gg_cons_1', 'gg_cons_2', 'ean', 'testo_agg_1', 'testo_agg_2', 'testo_agg_3', 'testo_agg_4',
                      'pz_x_scatola', 'peso_fisso', 'num_offerta', 'art_in_pubblic', 'sovrascritt_prezzo',
                      'stile_tracc', 'rich_stm_traccia']
        self.formati = ['formato_1', 'formato_2', 'formato_3', 'formato_4']
        self.ingredienti = ['riga_1', 'riga_2', 'riga_3', 'riga_4']
        self.label = {}
        self.entry = {}
        self.box_reparto_value = tk.StringVar()
        self.box_merceologia_value = tk.StringVar()
        self.filtro_merceologia = tk.StringVar()
        self.valore_ckb_flag1 = tk.StringVar()
        self.valore_ckb_flag1.set(0)

        # Connessione al Database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        # Definizione Frame
        self.frame_sx = tk.Frame(self, bd=1, relief="raised")
        self.frame_centrale_alto = tk.Frame(self, bd=1, relief="raised")
        self.frame_centrale_basso = tk.Frame(self, bd=1, relief="raised")
        self.frame_dx = tk.Frame(self, bd=1, relief="raised")

        self.lbl_lista_prodotti = ttk.LabelFrame(self.frame_sx, text='Lista Prodotti')

        # TRREVIEW per tab lista prodotti
        self.tree_produzione = ttk.Treeview(self.lbl_lista_prodotti, height=23)
        self.tree_produzione['columns'] = ('Id', 'Prodotto')
        self.tree_produzione['show'] = 'headings'
        self.tree_produzione.heading('Id', text="Id")
        self.tree_produzione.heading('Prodotto', text="Prodotto")

        self.tree_produzione.column("Id", width=40)
        self.tree_produzione.column("Prodotto", width=150)

        self.tree_produzione.bind("<Double-1>", self.ondoubleclick)

        # LABELFRAME nome prodotto
        self.lbl_frame_nome_prodotto = ttk.Labelframe(self.frame_centrale_alto, text='Prodotto')
        self.ent_nome_prodotto = ttk.Entry(self.lbl_frame_nome_prodotto, width=30)

        # LABELFRAME e COMBOBOX reparto prodotto
        self.lbl_frame_reparto_prodotto = ttk.Labelframe(self.frame_centrale_alto, text='Reparto')
        self.box_reparto = ttk.Combobox(self.lbl_frame_reparto_prodotto, textvariable=self.box_reparto_value)

        # LABELFRAME e COMBOBOX merceologia
        self.lbl_frame_merceologia = ttk.Labelframe(self.frame_centrale_alto, text='Merceologia')
        self.box_merceologia = ttk.Combobox(self.lbl_frame_merceologia, textvariable=self.box_merceologia_value)

        # CHECKBOX
        self.ckb_flag1 = tk.Checkbutton(self.lbl_frame_merceologia, text='Usa in produzione',
                                        variable=self.valore_ckb_flag1)

        # LABELFRAME dettagli prodotto selezionato
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_centrale_alto,
                                                             text='Dettagli prodotto selezionato')

        # LABEL ingredienti
        self.lbl_ingredienti = ttk.Label(self.frame_centrale_basso, text='INGREDIENTI')

        # LABELFRAME
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx, text='')
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Helvetica', 10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self.inserisci)
        self.btn_stp_etichetta = tk.Button(self.lbl_frame_scegli,
                                           text='Stampa Etichetta',
                                           state='disabled',
                                           font=('Helvetica', 10),
                                           command=self.stp_etichetta)

        # LABELFRAME filtro
        self.lbl_frame_filtro = ttk.LabelFrame(self.frame_dx, text='Filtro Articoli')

        # COMBOBOX filtro merceologia
        self.box_merceologia_filtro = ttk.Combobox(self.lbl_frame_filtro, textvariable=self.filtro_merceologia)

        # BOTTONI per filtro
        self.btn_filtra = tk.Button(self.lbl_frame_filtro,
                                    text='Filtra',
                                    font=('Helvetica', 10),
                                    command=self.filtra)
        self.btn_reset = tk.Button(self.lbl_frame_filtro,
                                   text='Reset Lista Prodotti',
                                   font=('Helvetica', 10),
                                   command=self.aggiorna)

        # BUTTON manda in bilancia
        self.btn_in_bilancia = tk.Button(self.lbl_frame_scegli,
                                         text='Invia in bilancia',
                                         font=('Helvetica', 20),
                                         command=self.crea_file)

        # PROGRESS BAR
        self.progress_bar = ttk.Progressbar(self.lbl_frame_scegli, orient=tk.HORIZONTAL, mode='determinate')

        self.crea_layout()
        self.aggiorna()
        self.riempi_combo_reparto()
        self.riempi_combo_merceologie()
        self.crea_label_entry()
        self.crea_label_formato_ingredienti()

    def crea_layout(self):
        self.frame_sx.grid(row=1, column=0, rowspan=2, sticky='n')
        self.frame_centrale_alto.grid(row=1, column=1, sticky='n')
        self.frame_centrale_basso.grid(row=2, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')
        self.lbl_lista_prodotti.grid(row=1, column=0, sticky='n')

        self.tree_produzione.grid(row=1, column=0, columnspan=3, sticky='we')

        self.lbl_frame_nome_prodotto.grid(row=1, column=0, columnspan=3)
        self.ent_nome_prodotto.grid(row=1, column=0)
        self.lbl_frame_reparto_prodotto.grid(row=2, column=0)
        self.lbl_frame_merceologia.grid(row=2, column=1)

        self.box_reparto.grid(row=1, column=0)
        self.box_merceologia.grid(row=1, column=1)
        self.ckb_flag1.grid(row=1, column=2)

        self.lbl_frame_dettagli_selezionato.grid(row=3, column=0, columnspan=2, sticky='n')
        self.lbl_ingredienti.grid(row=1, column=0, columnspan=4, pady=10)

        self.lbl_frame_scegli.grid(row=1, column=0)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')
        self.btn_stp_etichetta.grid(sticky='we')
        self.btn_in_bilancia.grid(sticky='we')
        self.progress_bar.grid(sticky='we')

        self.lbl_frame_filtro.grid(row=2, column=0)
        self.box_merceologia_filtro.grid()
        self.btn_filtra.grid(sticky='we')
        self.btn_reset.grid(sticky='we')

    def crea_label_entry(self):
        r = 1
        c = 0
        for campo in self.campi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_dettagli_selezionato, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.lbl_frame_dettagli_selezionato)
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

    def crea_label_formato_ingredienti(self):
        r = 2
        c = 0
        for campo in self.formati:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.frame_centrale_basso, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.frame_centrale_basso, width='5')
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

        r = 2
        c = 2
        for campo in self.ingredienti:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.frame_centrale_basso, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.frame_centrale_basso, width='50')
            ent.grid(row=r, column=c + 1)
            self.entry[campo] = ent
            r += 1

    def riempi_combo_reparto(self):
        lista_rep = []

        self.c.execute("SELECT reparto From reparti WHERE flag2_prod = 1 ")
        for row in self.c:
            lista_rep.extend(row)
        self.box_reparto['values'] = lista_rep

    def riempi_combo_merceologie(self):
        lista_merc = []

        self.c.execute("SELECT merceologia From merceologie")
        for row in self.c:
            lista_merc.extend(row)
        self.box_merceologia['values'] = lista_merc
        self.box_merceologia_filtro['values'] = lista_merc

    def modifica(self):
        stringa = 'UPDATE prodotti SET prodotto = %s WHERE ID = %s'
        self.c.execute(stringa, (self.ent_nome_prodotto.get(), (self.item[0])))
        self.conn.commit()
        stringa = 'UPDATE prodotti SET reparto = %s WHERE ID = %s'
        self.c.execute(stringa, (self.box_reparto_value.get(), (self.item[0])))
        self.conn.commit()
        stringa = 'UPDATE prodotti SET merceologia = %s WHERE ID = %s'
        self.c.execute(stringa, (self.box_merceologia_value.get(), (self.item[0])))
        self.conn.commit()

        for campo in self.campi:
            stringa = 'UPDATE prodotti SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for campo in self.ingredienti:
            stringa = 'UPDATE prodotti SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for campo in self.formati:
            stringa = 'UPDATE prodotti SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        self.c.execute('UPDATE prodotti SET flag1_prod=%s WHERE ID = %s', (self.valore_ckb_flag1.get(), (self.item[0])))
        self.conn.commit()
        self.aggiorna()

    def inserisci(self):

        self.lista_da_salvare.append(self.ent_nome_prodotto.get())
        self.lista_da_salvare.append(self.box_reparto_value.get())
        for campo in self.campi:
            self.lista_da_salvare.append(self.entry[campo].get())
        for campo in self.ingredienti:
            self.lista_da_salvare.append(self.entry[campo].get())
        for campo in self.formati:
            self.lista_da_salvare.append(self.entry[campo].get())
        self.lista_da_salvare.append(self.box_merceologia_value.get())
        self.lista_da_salvare.append(self.valore_ckb_flag1.get())

        self.c.execute('INSERT INTO prodotti(prodotto, reparto, plu, prezzo1, prezzo2, prezzo3, prezzo4, '
                       'prezzo_straord,gruppo_merc, tara, gg_cons_1, gg_cons_2, ean, testo_agg_1, testo_agg_2, '
                       'testo_agg_3, testo_agg_4, pz_x_scatola, peso_fisso, num_offerta, art_in_pubblic, '
                       'sovrascritt_prezzo, stile_tracc, rich_stm_traccia, riga_1, riga_2, riga_3, riga_4, '
                       'formato_1, formato_2, formato_3, formato_4, merceologia, flag1_prod ) '
                       'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       self.lista_da_salvare)
        self.conn.commit()
        self.aggiorna()
        del self.lista_da_salvare[0:]

    def aggiorna(self):
        self.tree_produzione.delete(*self.tree_produzione.get_children())
        self.c.execute("SELECT * From prodotti ")
        for lista in self.c:
            self.tree_produzione.insert('', 'end', values=(lista[0], lista[1]))

        lista = []

        self.c.execute("SELECT ID From prodotti")
        for row in self.c:
            lista.extend(row)

    def ondoubleclick(self, event):
        self.btn_stp_etichetta['state'] = 'normal'
        self.ckb_flag1.deselect()
        self.ent_nome_prodotto.delete(0, 'end')
        self.item = (self.tree_produzione.item(self.tree_produzione.selection(), 'values'))
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')
        for campo in self.ingredienti:
            self.entry[campo].delete(0, 'end')
        for campo in self.formati:
            self.entry[campo].delete(0, 'end')
        i = 1

        self.c.execute("SELECT * FROM prodotti WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            print(self.row)

            self.ent_nome_prodotto.insert(0, self.row[i])
            i += 1
            self.box_reparto.set(self.row[i])
            i += 1
            while i != 25:
                for campo in self.campi:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            while i != 29:
                for campo in self.ingredienti:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            while i != 33:
                for campo in self.formati:
                    self.entry[campo].insert(0, self.row[i])
                    i += 1
            self.box_merceologia_value.set(self.row[i])
        i += 1
        if self.row[i] == 1:
            self.ckb_flag1.select()

    def stp_etichetta(self):
        pagesize = (54 * mm, 101 * mm)
        d = canvas.Canvas("Eti_anagrafica.pdf", pagesize=pagesize)
        d.rotate(90)
        d.drawString(2*mm, -8*mm, self.item[1].upper())
        self.c.execute("SELECT * FROM prodotti WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            d.drawString(80 * mm, -8 * mm, 'PLU')
            d.drawString(90 * mm, -8 * mm, self.row[3][-3:])
            d.drawString(2*mm, -15*mm, self.row[25])
            d.drawString(2*mm, -20*mm, self.row[26])
            d.drawString(2*mm, -25*mm, self.row[27])
            d.drawString(2 * mm, -45 * mm, '€/Kg ')
            d.drawString(20 * mm, -45 * mm, str("%.2f" % (float(self.row[4]) / 100)))
        d.showPage()
        d.save()
        win32api.ShellExecute(None, "print", "Eti_anagrafica.pdf", '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)

    def filtra(self):
        self.tree_produzione.delete(*self.tree_produzione.get_children())
        self.c.execute("SELECT * FROM prodotti WHERE merceologia = %s", (self.filtro_merceologia.get(),))
        for lista in self.c:
            self.tree_produzione.insert('', 'end', values=(lista[0], lista[1]))

    def crea_file(self):
        path = '//192.168.0.224/c/WinSwGx-NET//bizvar/LABORATORIO/'
        print(self.item[1])
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
                       "WHERE prodotto = %s", (self.item[1],))
        for self.row in self.c:
            pass
        campo1 = ('0' + str(self.row[3]))
        campo2 = ('000' + str(self.row[9]))
        campo3 = ('0'*(6-(len(str(self.row[4])))) + str(self.row[4]))  # prezzo
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
                       "WHERE prodotto = %s", (self.item[1],))
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
        campo13 = (str(self.row[28]) + ' '*(50-(len(self.row[28]))))
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


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Produzione(notebook)
    notebook.add(new, text='Produzione')
    root.mainloop()
