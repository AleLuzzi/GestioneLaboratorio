import tkinter as tk
from tkinter import ttk
import sqlite3


class Ingredienti(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''
        self.valore_flag = dict()

        '''
        Connessione al Database
        '''
        self.conn = sqlite3.connect('../laboratorio/data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Definizione Frame
        '''
        self.frame_sx = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)
        '''
        Treeview per tab Ingredienti base
        '''
        self.tree_ingredienti = ttk.Treeview(self.frame_sx, height=23)
        self.tree_ingredienti['columns'] = ('Id', 'Ingrediente', 'cod_ean', 'merceologia')
        self.tree_ingredienti['show'] = 'headings'
        self.tree_ingredienti.heading('Id', text="Id")
        self.tree_ingredienti.heading('Ingrediente', text="Ingrediente")
        self.tree_ingredienti.heading('cod_ean', text="cod EAN")
        self.tree_ingredienti.heading('merceologia', text='Merceologia')

        self.tree_ingredienti.column("Id", width=10)
        self.tree_ingredienti.column("Ingrediente", width=200)
        self.tree_ingredienti.column("cod_ean", width=100)
        self.tree_ingredienti.column("merceologia", width=50)

        self.tree_ingredienti.bind("<Double-1>", self.ondoubleclick)

        '''
        Lista campi del record
        '''
        self.campi = ['ingrediente_base', 'cod_ean']
        self.attributi = ['Allergene']
        self.label = {}
        self.ckbutton = {}
        self.entry = {}

        '''
        Labelframe dettagli fornitore selezionato
        '''
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_dx, text='Dettagli ingrediente selezionato')
        self.lbl_frame_attributi_ingrediente = ttk.LabelFrame(self.frame_dx, text='Attributi ingrediente selezionato')
        '''
        Combobox per gestire merceologia prodotti
        '''
        self.box_merceologia = tk.StringVar()
        self.box = ttk.Combobox(self.lbl_frame_attributi_ingrediente, textvariable=self.box_merceologia)
        '''
        Labelframe scegli ingrediente
        '''
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx, text='Azioni')
        self.btn_modifica = ttk.Button(self.lbl_frame_scegli, text='Modifica', command=self.modifica)
        self.btn_inserisci = ttk.Button(self.lbl_frame_scegli, text='Inserisci', command=self.inserisci)
        '''
        LAYOUT
        '''
        self.frame_sx.grid(row='1', column='0', sticky='n')
        self.frame_dx.grid(row='1', column='1', sticky='n')

        self.tree_ingredienti.grid(row=1, column=0, columnspan=3, sticky='we')
        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_frame_attributi_ingrediente.grid(row=2, column=0)
        self.box.grid(columnspan=2)

        self.lbl_frame_scegli.grid(row=3, column=0)
        self.btn_modifica.grid()
        self.btn_inserisci.grid()

        self.aggiorna()
        self.crea_label_entry()
        self.crea_attributi()
        self.riempi_combo_merceologia()

    def riempi_combo_merceologia(self):
        lista_merceologie = []

        for row in self.c.execute("SELECT merceologia From merceologie WHERE flag3_ing_base = 1 "):
            lista_merceologie.extend(row)
        self.box['values'] = lista_merceologie

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
            lbl = ttk.Label(self.lbl_frame_attributi_ingrediente, text=attributo)
            lbl.grid(row=r, column=c)
            self.label[attributo] = lbl

            self.valore_flag[attributo] = tk.IntVar()
            ckbtn = tk.Checkbutton(self.lbl_frame_attributi_ingrediente, variable=self.valore_flag[attributo])
            ckbtn.grid(row=r, column=c + 1)
            self.ckbutton[attributo] = ckbtn
            r += 1

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        for attributo in self.attributi:
            lista_da_salvare.append(self.valore_flag[attributo].get())
        lista_da_salvare.append(self.box_merceologia.get())
        self.c.execute('INSERT INTO ingredienti_base(ingrediente_base,cod_ean,flag1_allergene,merceologia) '
                       'VALUES (?,?,?,?)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()
        del lista_da_salvare[0:]

    def modifica(self):
        valori_da_salvare = []
        for campo in self.campi:
            stringa = 'UPDATE ingredienti_base SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for attributo in self.attributi:
            valori_da_salvare.append(self.valore_flag[attributo].get())

        stringa = 'UPDATE ingredienti_base SET flag1_allergene=? WHERE ID = ?'
        self.c.execute(stringa, (valori_da_salvare[0], (self.item[0])))
        self.conn.commit()

        stringa = 'UPDATE ingredienti_base SET merceologia=? WHERE ID = ?'
        self.c.execute(stringa, (self.box_merceologia.get(), (self.item[0])))
        self.conn.commit()

        self.aggiorna()

    def aggiorna(self):
        self.tree_ingredienti.delete(*self.tree_ingredienti.get_children())
        for lista in self.c.execute("SELECT * FROM ingredienti_base "):
            self.tree_ingredienti.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[4]))

        lista = []

        for row in self.c.execute("SELECT ID From fornitori"):
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        for attributo in self.attributi:
            self.ckbutton[attributo].deselect()

        self.item = (self.tree_ingredienti.item(self.tree_ingredienti.selection(), 'values'))

        i = 1
        for self.row in self.c.execute("SELECT * FROM ingredienti_base WHERE ID = ?", (self.item[0],)):
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1

            i = 3
            for attributo in self.attributi:
                if self.row[i] == 1:
                    self.ckbutton[attributo].select()
                i += 1
            self.box_merceologia.set(self.row[i])


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Ingredienti(notebook)
    notebook.add(new, text='Ingredienti')
    root.mainloop()
