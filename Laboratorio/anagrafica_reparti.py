import tkinter as tk
from tkinter import ttk
import mysql.connector
import configparser


class Reparti(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''
        self.valore_flag = dict()
        self.config = self.leggi_file_ini()

        # Connessione al Database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        # Definizione Frame
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        # TREEVIEW per tab Reparti
        self.tree_reparti = ttk.Treeview(self.frame_sx, height=23)
        self.tree_reparti['columns'] = ('Id', 'Reparto')
        self.tree_reparti['show'] = 'headings'
        self.tree_reparti.heading('Id', text="Id")
        self.tree_reparti.heading('Reparto', text="Reparto")

        self.tree_reparti.column("Id", width=10)
        self.tree_reparti.column("Reparto", width=150)

        self.tree_reparti.bind("<Double-1>", self.ondoubleclick)

        # Lista campi del record
        self.campi = ['reparto']
        self.attributi = ['Mostra nel tab dipendenti', 'Mostra nel tab produzione']
        self.label = {}
        self.ckbutton = {}
        self.entry = {}

        # LABELFRAME dettagli reparto selezionato
        self.lbl_frame_dettagli_selezionato = tk.LabelFrame(self.frame_centrale,
                                                            font=('Verdana',15),
                                                            text='Dettagli reparto selezionato')

        self.lbl_frame_attributi_reparto = tk.LabelFrame(self.frame_centrale,
                                                         font=('Verdana',15),
                                                         text='Attributi reparto selezionato')

        # LABELFRAME scegli prodotto
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx, text='')
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Verdana',10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Verdana',10),
                                       command=self.inserisci)

        self.aggiorna()
        self.crea_label_entry()
        self.crea_attributi()

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.tree_reparti.grid(row=1, column=0, columnspan=3, sticky='we')

        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')

        self.lbl_frame_attributi_reparto.grid(row=2, column=0)

        self.lbl_frame_scegli.grid(row=3, column=0)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

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

    def crea_attributi(self):
        r = 1
        c = 0
        for attributo in self.attributi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_attributi_reparto, text=attributo)
            lbl.grid(row=r, column=c)
            self.label[attributo] = lbl

            self.valore_flag[attributo] = tk.IntVar()
            ckbtn = tk.Checkbutton(self.lbl_frame_attributi_reparto, variable=self.valore_flag[attributo])
            ckbtn.grid(row=r, column=c + 1)
            self.ckbutton[attributo] = ckbtn
            r += 1

    def modifica(self):
        valori_da_salvare = []
        for campo in self.campi:
            stringa = 'UPDATE reparti SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for attributo in self.attributi:
            valori_da_salvare.append(self.valore_flag[attributo].get())

        stringa = 'UPDATE reparti SET flag1_dip=%s , flag2_prod=%s WHERE ID = %s'
        self.c.execute(stringa, (valori_da_salvare[0], valori_da_salvare[1], (self.item[0])))
        self.conn.commit()
        self.aggiorna()

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        self.c.execute('INSERT INTO reparti(reparto) VALUES (%s)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_reparti.delete(*self.tree_reparti.get_children())
        self.c.execute("SELECT * From reparti ")
        for lista in self.c:
            self.tree_reparti.insert('', 'end', values=(lista[0], lista[1]))
        lista = []

        self.c.execute("SELECT ID From reparti")
        for row in self.c:
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        for attributo in self.attributi:
            self.ckbutton[attributo].deselect()

        self.item = (self.tree_reparti.item(self.tree_reparti.selection(), 'values'))

        i = 1
        self.c.execute("SELECT * FROM reparti WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1

            i = 2
            for attributo in self.attributi:
                if self.row[i] == 1:
                    self.ckbutton[attributo].select()
                i += 1


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Reparti(notebook)
    notebook.add(new, text='Reparti')
    root.mainloop()
