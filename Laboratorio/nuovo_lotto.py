import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector
from tkinter import messagebox
import configparser


class NuovoLotto(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Nuovo Lotto")
        # self.geometry('1024x540+0+0')
        self.data = dt.date.today()

        self.config = self.leggi_file_ini()

        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        self.nuova_produzione = tk.StringVar()
        self.peso_da_inserire = tk.StringVar()
        self.prog_lotto_ven = self.genera_prog_vendita()

        # DISPOSIZIONE FRAME
        self.frame_sx = tk.Frame(self)
        self.frame_sx_alto = tk.Frame(self.frame_sx)
        self.frame_sx_basso = tk.Frame(self.frame_sx, background='white')
        self.frame_dx = tk.Frame(self)
        self.frame_dx_r = tk.Frame(self)
        self.frame_dx_basso = tk.Frame(self)

        # TREEVIEW per riepilogo immissioni
        self.tree = ttk.Treeview(self.frame_sx_alto, height=20)
        self.tree['columns'] = ('data ingresso', 'fornitore', 'peso', 'residuo')

        self.tree.column("data ingresso", width=80)
        self.tree.column("fornitore", width=80)
        self.tree.column("peso", width=80)
        self.tree.column("residuo", width=60)

        self.tree.heading("data ingresso", text="data ingresso")
        self.tree.heading("fornitore", text="fornitore")
        self.tree.heading("peso", text="peso")
        self.tree.heading("residuo", text="residuo")

        self.tree.tag_configure('odd', background='light green')

        self.tree.bind("<Double-1>", self.ondoubleclick)

        # LABEL nuovo lotto vendita
        self.lbl_nuovo_lotto = ttk.Label(self.frame_dx, text='NUOVO LOTTO',
                                         foreground='blue', font=('Helvetica', 22))
        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_dx, text=str(self.prog_lotto_ven) + 'V',
                                                font=('Helvetica', 40))

        # LABEL quantita' prodotta
        self.lbl_qta_prodotto = ttk.Label(self.frame_dx, text='Quantita prodotta',
                                          foreground='blue', font=('Helvetica', 20))

        # TREEVIEW per lotti selezionati
        self.tree_lotti_selezionati = ttk.Treeview(self.frame_dx_r, height=8)
        self.tree_lotti_selezionati['columns'] = ('progressivo_v',
                                                  'data',
                                                  'lotto ingresso',
                                                  'nuova_produzione',
                                                  'peso',
                                                  'taglio')
        self.tree_lotti_selezionati['displaycolumns'] = ('lotto ingresso',
                                                         'taglio')

        self.tree_lotti_selezionati['show'] = 'headings'

        self.tree_lotti_selezionati.column("lotto ingresso", width=100)
        self.tree_lotti_selezionati.column("taglio", width=100)

        self.tree_lotti_selezionati.heading("lotto ingresso", text="lotto ingresso")
        self.tree_lotti_selezionati.heading("taglio", text="taglio")

        # LABELFRAME nuova produzione
        self.labelframe = ttk.Labelframe(self.frame_dx_basso, text="Nuova Produzione")

        # ENTRY per inserimento del peso
        self.entry_peso = ttk.Entry(self.frame_dx, font=('Helvetica', 20), width=7, textvariable=self.peso_da_inserire)
        self.entry_peso.focus()

        # BOTTONE ESCI E SALVA
        self.btn_elimina_riga = tk.Button(self.frame_dx_r,
                                          text='Elimina riga',
                                          command=self.rimuovi_riga_selezionata)
        self.btn_esci = tk.Button(self.frame_sx_basso,
                                  text="Chiudi finestra",
                                  font=('Helvetica', 20),
                                  width=14,
                                  command=self.esci_senza_salvare)

        self.btn_esci_salva = tk.Button(self.frame_sx_basso,
                                        text="Esci e salva",
                                        font=('Helvetica', 20),
                                        width=14,
                                        command=self.esci_salva)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, sticky='n')
        self.frame_sx_alto.grid()
        self.frame_sx_basso.grid(sticky='ew')
        self.frame_dx.grid(row=0, column=1, sticky='n')
        self.frame_dx_r.grid(row=0, column=2, sticky='n')
        self.frame_dx_basso.grid(row=0, column=1, columnspan=2, sticky='s')

        self.tree.grid(row=0, column=0, columnspan=2, sticky='w')

        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.lbl_prog_lotto_vendita.grid(row=1, column=0, sticky='w')

        self.lbl_qta_prodotto.grid(row=2, column=0)
        self.entry_peso.grid(row=3, column=0, sticky='w')

        self.tree_lotti_selezionati.grid(row=0, column=0)
        self.btn_elimina_riga.grid(row=1, column=0, sticky='we')

        self.labelframe.grid(row=4, column=0, columnspan=2, sticky='ew')

        self.btn_esci.grid(row=2, column=0, padx=10, pady=10)
        self.btn_esci_salva.grid(row=2, column=1, padx=10, pady=10)

        self.lotti_acq_aperti()
        self.riempi_lista_produzione()

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def rimuovi_riga_selezionata(self):
        curitem = self.tree_lotti_selezionati.selection()[0]
        self.tree_lotti_selezionati.delete(curitem)

    def genera_prog_vendita(self):
        self.c.execute("SELECT prog_ven FROM progressivi")
        prog = self.c.fetchone()[0]
        return prog

    def riempi_lista_produzione(self):
        # Lista articoli per nuova produzione
        self.c.execute("SELECT prodotto FROM prodotti WHERE reparto = 'Macelleria'")
        for row in self.c:
            self.lista_nuova_produzione.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_nuova_produzione)):
            if row % 9 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe,
                           text=str(self.lista_nuova_produzione[i]).upper(),
                           variable=self.nuova_produzione,
                           width=27,
                           indicatoron=0,
                           value=self.lista_nuova_produzione[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def lotti_acq_aperti(self):
        # Ciclo per inserire i lotti in acquisto da utilizzare
        self.c.execute("SELECT * from ingresso_merce WHERE lotto_chiuso = 'no'")
        for lista in self.c:
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[4],
                                 values=(dt.date.strftime(lista[1], '%d/%m/%y'), lista[3], lista[5]))
                self.tree.item(lista[0], open='true')

    def esci_salva(self):
        for child in self.tree_lotti_selezionati.get_children():
            self.lista_da_salvare.append(self.tree_lotti_selezionati.item(child)['values'])
        self.c.executemany('INSERT INTO lotti_vendita VALUES (%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.c.execute('UPDATE progressivi SET prog_ven = %s', (self.prog_lotto_ven + 1,))
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def esci_senza_salvare(self):
        if bool(self.tree_lotti_selezionati.get_children()):
            messagebox.showinfo('Attenzione', 'Ci sono dati inseriti non salvati')
        else:
            self.destroy()

    def ondoubleclick(self, event):
        if (self.nuova_produzione.get() != '') and (self.peso_da_inserire.get() != ''):
            item = self.tree.selection()[0]
            self.tree_lotti_selezionati.insert('', 'end', values=((str(self.prog_lotto_ven) + 'V'),
                                                                  self.data,
                                                                  self.tree.parent(item),
                                                                  (self.nuova_produzione.get()),
                                                                  (self.peso_da_inserire.get()),
                                                                  (self.tree.item(item, 'text'))))
        else:
            pass


if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLotto()
    root.mainloop()
