import tkinter as tk
from tkinter import ttk
import mysql.connector


class Fornitori(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''
        self.valore_flag = dict()

        # Connessione al Database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        # Definizione FRAME
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        # TREEVIEW per tab Fornitori
        self.tree_fornitori = ttk.Treeview(self.frame_sx, height=23)
        self.tree_fornitori['columns'] = ('Id', 'Azienda')
        self.tree_fornitori['show'] = 'headings'
        self.tree_fornitori.heading('Id', text="Id")
        self.tree_fornitori.heading('Azienda', text="Azienda")

        self.tree_fornitori.column("Id", width=20)
        self.tree_fornitori.column("Azienda", width=150)

        self.tree_fornitori.bind("<Double-1>", self.ondoubleclick)

        # Lista campi del record
        self.campi = ['azienda']
        self.attributi = ['Ingresso Merce']
        self.label = {}
        self.ckbutton = {}
        self.entry = {}

        # LABELFRAME dettagli fornitore selezionato
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_centrale, text='Dettagli fornitore selezionato')
        self.lbl_frame_attributi_fornitori = ttk.LabelFrame(self.frame_centrale, text='Attributi fornitore selezionato')

        # LABELFRAME scegli prodotto
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx)
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva modifiche',
                                      font=('Helvetica', 10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self.inserisci)

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.tree_fornitori.grid(row=1, column=0, columnspan=3, sticky='we')
        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_frame_attributi_fornitori.grid(row=2, column=0)
        self.lbl_frame_scegli.grid(row=3, column=0)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

        self.aggiorna()
        self.crea_label_entry()
        self.crea_attributi()

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
            lbl = ttk.Label(self.lbl_frame_attributi_fornitori, text=attributo)
            lbl.grid(row=r, column=c)
            self.label[attributo] = lbl

            self.valore_flag[attributo] = tk.IntVar()
            ckbtn = tk.Checkbutton(self.lbl_frame_attributi_fornitori, variable=self.valore_flag[attributo])
            ckbtn.grid(row=r, column=c + 1)
            self.ckbutton[attributo] = ckbtn
            r += 1

    def modifica(self):
        valori_da_salvare = []
        for campo in self.campi:
            stringa = 'UPDATE fornitori SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()

        for attributo in self.attributi:
            valori_da_salvare.append(self.valore_flag[attributo].get())

        stringa = 'UPDATE fornitori SET flag1_ing_merce=%s WHERE ID = %s'
        self.c.execute(stringa, (valori_da_salvare[0], (self.item[0])))
        self.conn.commit()
        self.aggiorna()

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        for attributo in self.attributi:
            lista_da_salvare.append(self.valore_flag[attributo].get())
        self.c.execute('INSERT INTO fornitori(azienda,flag1_ing_merce) VALUES (%s,%s)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        self.c.execute("SELECT * From fornitori ")
        for lista in self.c:
            self.tree_fornitori.insert('', 'end', values=(lista[0], lista[1]))

        lista = []

        self.c.execute("SELECT ID From fornitori")
        for row in self.c:
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        for attributo in self.attributi:
            self.ckbutton[attributo].deselect()

        self.item = (self.tree_fornitori.item(self.tree_fornitori.selection(), 'values'))

        self.c.execute("SELECT * FROM fornitori WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[1])

            i = 2
            for attributo in self.attributi:
                if self.row[i] == 1:
                    self.ckbutton[attributo].select()
                i += 1

if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Fornitori(notebook)
    notebook.add(new, text='Fornitori')
    root.mainloop()
