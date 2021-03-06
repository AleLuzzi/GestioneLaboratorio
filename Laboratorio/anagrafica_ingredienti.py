import tkinter as tk
from tkinter import ttk
import mysql.connector
import configparser


class Ingredienti(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)

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
        self.frame_dx = ttk.Frame(self)

        # TREEVIEW per tab Ingredienti base
        self.tree_ingredienti = ttk.Treeview(self.frame_sx, height=23)
        self.tree_ingredienti['columns'] = ('Id', 'Ingrediente', 'cod_ean', 'merceologia')
        self.tree_ingredienti['show'] = 'headings'
        self.tree_ingredienti.heading('Id', text="Id")
        self.tree_ingredienti.heading('Ingrediente', text="Ingrediente")
        self.tree_ingredienti.heading('cod_ean', text="cod EAN")
        self.tree_ingredienti.heading('merceologia', text='Merceologia')

        self.tree_ingredienti.column("Id", width=30)
        self.tree_ingredienti.column("Ingrediente", width=150)
        self.tree_ingredienti.column("cod_ean", width=100)
        self.tree_ingredienti.column("merceologia", width=100)

        self.tree_ingredienti.bind("<Double-1>", self.ondoubleclick)

        # Lista campi del record
        self.campi = ['ingrediente_base', 'cod_ean']
        self.attributi = ['Allergene']
        self.label = {}
        self.ckbutton = {}
        self.entry = {}

        # LABELFRAME dettagli ingrediente selezionato
        self.lbl_frame_dettagli_selezionato = tk.LabelFrame(self.frame_dx, text='Dettagli ingrediente selezionato',
                                                             font=('Verdana', 15))
        self.lbl_frame_attributi_ingrediente = tk.LabelFrame(self.frame_dx, text='Attributi ingrediente selezionato',
                                                              font=('Verdana', 15))

        # COMBOBOX per gestire merceologia prodotti
        self.box_merceologia = tk.StringVar()
        self.box = ttk.Combobox(self.lbl_frame_attributi_ingrediente, textvariable=self.box_merceologia)

        # LABELFRAME per filtro
        self.lbl_frame_filtro = tk.LabelFrame(self.frame_dx,
                                               text='Filtra Lista Ingredienti',
                                               font=('Verdana', 15))

        # COMBOBOX e BOTTONE per filtro
        self.box_filtro = ttk.Combobox(self.lbl_frame_filtro)
        self.btn_applica_filtro = tk.Button(self.lbl_frame_filtro,
                                            text='Applica',
                                            font=('Helvetica', 10),
                                            command=self.filtra)

        # BOTTONE per reset filtro
        self.btn_reset_filtro = tk.Button(self.lbl_frame_filtro,
                                          text='Reset Lista ingredienti',
                                          font=('Helvetica', 10),
                                          command=self.aggiorna)

        # LABELFRAME scegli ingrediente
        self.lbl_frame_scegli = tk.LabelFrame(self.frame_dx, text='')

        # crea Label ENTRY
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

        # Crea Attributi
        r = 1
        c = 0
        for attributo in self.attributi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_attributi_ingrediente, text=attributo)
            lbl.grid(row=r, column=c)
            self.label[attributo] = lbl

            self.valore_flag[attributo] = tk.IntVar()
            ckbtn = tk.Checkbutton(self.lbl_frame_attributi_ingrediente, variable=self.valore_flag[attributo])
            ckbtn.grid(row=r, column=c + 1)
            self.ckbutton[attributo] = ckbtn
            r += 1

        # Riempi COMBO Merceologia e Filtro
        lista_merceologie = []

        self.c.execute("SELECT merceologia From merceologie WHERE flag3_ing_base = 1 ")
        for row in self.c:
            lista_merceologie.extend(row)
        self.box['values'] = lista_merceologie
        self.box_filtro['values'] = lista_merceologie

        # BOTTONI per azioni
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Helvetica', 10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self.inserisci)

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_dx.grid(row=1, column=1, sticky='n')

        self.tree_ingredienti.grid(row=1, column=0, columnspan=3, sticky='we')
        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_frame_attributi_ingrediente.grid(row=2, column=0)

        ttk.Separator(self.frame_dx, orient='horizontal').grid(row=3, sticky='we', pady=5)

        self.lbl_frame_filtro.grid(row=4, column=0, sticky='we')
        self.box_filtro.grid()
        self.btn_applica_filtro.grid(row=5, column=0, sticky='we')
        self.btn_reset_filtro.grid(row=6, column=0, sticky='we')
        self.box.grid(columnspan=2)

        self.lbl_frame_scegli.grid(row=1, column=1)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

        self.aggiorna()

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        for attributo in self.attributi:
            lista_da_salvare.append(self.valore_flag[attributo].get())
        lista_da_salvare.append(self.box_merceologia.get())
        self.c.execute('INSERT INTO ingredienti_base(ingrediente_base,cod_ean,flag1_allergene,merceologia) '
                       'VALUES (%s,%s,%s,%s)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()
        del lista_da_salvare[0:]

    def modifica(self):
        valori_da_salvare = []
        for campo in self.campi:
            stringa = 'UPDATE ingredienti_base SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for attributo in self.attributi:
            valori_da_salvare.append(self.valore_flag[attributo].get())

        stringa = 'UPDATE ingredienti_base SET flag1_allergene=%s WHERE ID = %s'
        self.c.execute(stringa, (valori_da_salvare[0], (self.item[0])))
        self.conn.commit()

        stringa = 'UPDATE ingredienti_base SET merceologia=%s WHERE ID = %s'
        self.c.execute(stringa, (self.box_merceologia.get(), (self.item[0])))
        self.conn.commit()

        self.aggiorna()

    def aggiorna(self):
        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())
        self.c.execute("SELECT * FROM ingredienti_base ")
        for lista in self.c:
            self.tree_ingredienti.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[4]))

        lista = []

        self.c.execute("SELECT ID From fornitori")
        for row in self.c:
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        for attributo in self.attributi:
            self.ckbutton[attributo].deselect()

        self.item = event.widget.item(self.tree_ingredienti.selection(), 'values')

        i = 1
        self.c.execute("SELECT * FROM ingredienti_base WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1

            i = 3
            for attributo in self.attributi:
                if self.row[i] == 1:
                    self.ckbutton[attributo].select()
                i += 1
            self.box_merceologia.set(self.row[i])

    def filtra(self):
        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())
        stringa = self.box_filtro.get()
        self.c.execute("SELECT * FROM ingredienti_base WHERE merceologia like %s", ('%' + stringa + '%',))
        for lista in self.c:
            self.tree_ingredienti.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[4]))


if __name__ == '__main__':
    root = tk.Tk()
    new = Ingredienti()
    root.mainloop()
