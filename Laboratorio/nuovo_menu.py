import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector
import random
import os
# import facebook
import configparser


class NuovoMenu(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Nuovo Lotto Cucina")
        self.geometry("1024x525+0+0")

        self.data = dt.date.today()
        self.config = self.leggi_file_ini()

        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione_primi_piatti = []
        self.lista_nuova_produzione_secondi_piatti = []
        self.lista_nuova_produzione_contorni = []
        self.lista_nuova_produzione_piatti_freddi = []
        self.prog_lotto_ven = self.genera_progressivo()
        self.nuova_produzione = tk.StringVar()

        # DISPOSIZIONE FRAME
        self.frame_treeview = tk.Frame(self, bd='3', relief='groove')
        self.frame_nuovolotto = tk.Frame(self, bd='3', relief='groove')
        self.frame_basso = tk.Frame(self, bd='3', background='white', relief='groove')

        # IMMAGINI
        self.img_sync = tk.PhotoImage(file=os.path.join('immagini', 'sync.gif'))

        # TREEVIEW per riepilogo immissioni
        self.tree = ttk.Treeview(self.frame_treeview, height=5)
        self.tree['columns'] = ('prog_ven', 'data', 'lotto_acq',
                                'prodotto', 'peso', 'origine')

        self.tree['displaycolumns'] = ('prodotto', 'peso')
        self.tree['show'] = 'headings'

        self.tree.column("prodotto", width=120)
        self.tree.column("peso", width=80)

        self.tree.heading("prodotto", text="prodotto")
        self.tree.heading("peso", text="peso")

        self.tree.tag_configure('odd', background='light green')

        # LABEL nuovo lotto vendita
        self.lbl_nuovo_lotto = ttk.Label(self.frame_treeview,
                                         text='NUOVO LOTTO VENDITA',
                                         font=('Helvetica', 20))

        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_treeview,
                                                text=str(self.prog_lotto_ven) + 'V',
                                                font=('Helvetica', 40))

        # LABELFRAME nuova produzione
        self.labelframe_primi_piatti = tk.LabelFrame(self.frame_nuovolotto,
                                                     text="PRIMI",
                                                     font=('Verdana', 15),
                                                     foreground='blue',
                                                     labelanchor='n')
        self.labelframe_secondi_piatti = tk.LabelFrame(self.frame_nuovolotto,
                                                       text="SECONDI",
                                                       font=('Verdana', 15),
                                                       foreground='blue',
                                                       labelanchor='n')
        self.labelframe_contorni = tk.LabelFrame(self.frame_nuovolotto,
                                                 text="CONTORNI",
                                                 font=('Verdana', 15),
                                                 foreground='blue',
                                                 labelanchor='n')
        self.labelframe_piatti_freddi = tk.LabelFrame(self.frame_nuovolotto,
                                                      text='PIATTI FREDDI',
                                                      font=('Verdana', 15),
                                                      foreground='blue',
                                                      labelanchor='n')

        # LABELFRAME per peso da inserire
        self.lblframe_peso = ttk.LabelFrame(self.frame_basso,
                                            text='Peso')

        # ENTRY per inserimento del peso
        self.peso_da_inserire = tk.StringVar()
        self.entry_peso = ttk.Entry(self.lblframe_peso,
                                    font=('Helvetica', 10),
                                    textvariable=self.peso_da_inserire)
        self.entry_peso.focus()

        # BOTTONE ESCI E SALVA
        self.btn_invia = tk.Button(self.frame_basso,
                                   text="Invio",
                                   font=('Helvetica', 20),
                                   command=self.invia)
        self.btn_esci = tk.Button(self.frame_basso,
                                  text="Chiudi",
                                  font=('Helvetica', 20),
                                  command=self.destroy)
        self.btn_esci_salva = tk.Button(self.frame_basso,
                                        text="Esci e salva",
                                        font=('Helvetica', 20),
                                        command=self.esci_salva)
        self.btn_pubblica = tk.Button(self.frame_treeview,
                                      text='Pubblica su FB',
                                      font=('Helvetica', 20),
                                      command=self.pubblica)
        self.btn_rigenera_primi = tk.Button(self.frame_nuovolotto,
                                            image=self.img_sync,
                                            command=self.crea_articoli_nuova_produzione_primi_piatti)
        self.btn_rigenera_secondi = tk.Button(self.frame_nuovolotto,
                                              image=self.img_sync,
                                              command=self.crea_articoli_nuova_produzione_secondi_piatti)
        self.btn_rigenera_contorni = tk.Button(self.frame_nuovolotto,
                                               image=self.img_sync,
                                               command=self.crea_articoli_nuova_produzione_contorni)
        self.btn_rigenera_piatti_freddi = tk.Button(self.frame_nuovolotto,
                                                    image=self.img_sync,
                                                    command=self.crea_articoli_nuova_produzione_piatti_freddi)

        # BOTTONE rimuovi riga dal treeview riepilogativo
        self.btn_rimuovi_riga = tk.Button(self.frame_treeview,
                                          text="Rimuovi riga",
                                          command=self.rimuovi_riga_selezionata)

        # LAYOUT
        self.frame_nuovolotto.grid(row=0, column=0, rowspan=2, sticky='n')
        self.frame_treeview.grid(row=0, column=1, padx=10, sticky='n')
        self.frame_basso.grid(row=1, column=1, sticky='w')

        self.btn_rigenera_primi.grid(row=0, column=1, padx=15)
        self.btn_rigenera_secondi.grid(row=1, column=1, padx=15)
        self.btn_rigenera_contorni.grid(row=2, column=1, padx=15)
        self.btn_rigenera_piatti_freddi.grid(row=3, column=1, padx=15)

        self.labelframe_primi_piatti.grid(row=0, column=0)
        self.labelframe_secondi_piatti.grid(row=1, column=0)
        self.labelframe_contorni.grid(row=2, column=0)
        self.labelframe_piatti_freddi.grid(row=3, column=0)

        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.lbl_prog_lotto_vendita.grid(row=1, column=0)
        self.tree.grid(row=2, column=0, sticky='we')
        self.btn_rimuovi_riga.grid(row=2, column=1, sticky='n')

        self.btn_pubblica.grid(row=3, column=0)

        self.lblframe_peso.grid(row=0, column=0, sticky='w')
        self.entry_peso.grid()

        self.btn_invia.grid(row=0, column=1, padx=10, pady=20)
        self.btn_esci_salva.grid(row=0, column=3, padx=10, pady=20)
        self.btn_esci.grid(row=0, column=4, padx=10, pady=20)

        self.crea_nuovo_menu()

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def rimuovi_riga_selezionata(self):
        curitem = self.tree.selection()[0]
        self.tree.delete(curitem)

    def crea_nuovo_menu(self):
        self.crea_articoli_nuova_produzione_primi_piatti()
        self.crea_articoli_nuova_produzione_secondi_piatti()
        self.crea_articoli_nuova_produzione_contorni()
        self.crea_articoli_nuova_produzione_piatti_freddi()

    def crea_articoli_nuova_produzione_primi_piatti(self):
        for label in self.labelframe_primi_piatti.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        self.c.execute("SELECT prodotto FROM prodotti "
                       "WHERE reparto = 'Gastronomia' AND merceologia = 'Primi piatti' ")
        for row in self.c:
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

        return lista_primi_piatti

    def crea_articoli_nuova_produzione_secondi_piatti(self):
        for label in self.labelframe_secondi_piatti.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        self.c.execute("SELECT prodotto FROM prodotti "
                       "WHERE reparto = 'Gastronomia' AND merceologia = 'Secondi piatti' ")
        for row in self.c:
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

        self.c.execute("SELECT prodotto FROM prodotti "
                       "WHERE reparto = 'Gastronomia' AND merceologia = 'Contorni' ")
        for row in self.c:
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

    def crea_articoli_nuova_produzione_piatti_freddi(self):
        for label in self.labelframe_piatti_freddi.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()

        self.c.execute("SELECT prodotto FROM prodotti "
                       "WHERE reparto = 'Gastronomia' AND merceologia = 'Piatti freddi' ")
        for row in self.c:
            self.lista_nuova_produzione_piatti_freddi.extend(row)

        lista_freddi = (random.sample(self.lista_nuova_produzione_piatti_freddi, 3))

        row, col = 1, 0
        for i in range(0, len(lista_freddi)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_piatti_freddi,
                           text=str(lista_freddi[i]).upper(),
                           variable=self.nuova_produzione,
                           width=35,
                           indicatoron=0,
                           value=lista_freddi[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def genera_progressivo(self):
        self.c.execute("SELECT prog_ven FROM progressivi")
        prog_lotto_ven = self.c.fetchone()[0]
        return prog_lotto_ven

    def invia(self):

        self.tree.insert('', 'end', values=((str(self.prog_lotto_ven) + 'V'),
                                            self.data,
                                            '0',
                                            self.nuova_produzione.get(),
                                            self.peso_da_inserire.get(),
                                            '0'))
        self.entry_peso.delete(0, tk.END)

    def esci_salva(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        self.c.executemany('INSERT INTO lotti_vendita VALUES (%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_ven = %s', (self.prog_lotto_ven + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def pubblica(self):
        pass
        # graph = facebook.GraphAPI(access_token='token', version='2.7')
        # graph.put_wall_post(message=self.primi)


if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoMenu()
    root.mainloop()
