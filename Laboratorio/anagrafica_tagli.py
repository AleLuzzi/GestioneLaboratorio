import tkinter as tk
from tkinter import ttk
import sqlite3


class Tagli(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''
        # TODO aggiungere flag per produzione
        '''
        Connessione al Database
        '''
        self.conn = sqlite3.connect('data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Definizione Frame
        '''
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)
        '''
        Treeview per tab Tagli
        '''
        self.tree_tagli = ttk.Treeview(self.frame_sx, height=23)
        self.tree_tagli['columns'] = ('Id', 'Tagli')
        self.tree_tagli['show'] = 'headings'
        self.tree_tagli.heading('Id', text="Id")
        self.tree_tagli.heading('Tagli', text="Tagli")

        self.tree_tagli.column("Id", width=10)
        self.tree_tagli.column("Tagli", width=150)

        self.tree_tagli.bind("<Double-1>", self.ondoubleclick)
        '''
        Lista campi del record
        '''
        self.campi = ['taglio']
        self.label = {}
        self.entry = {}
        '''
        Labelframe dettagli taglio selezionato
        '''
        self.lbl_frame_taglio_selezionato = ttk.LabelFrame(self.frame_centrale, text='Dettagli taglio selezionato')
        '''
        Labelframe Azioni e filtra
        '''
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_centrale, text='Azioni')
        self.lbl_frame_filtra = ttk.Labelframe(self.frame_centrale, text='Filtra')
        '''
        Bottoni
        '''
        self.btn_modifica = ttk.Button(self.lbl_frame_scegli, text='Modifica', command=self.modifica)
        self.btn_inserisci = ttk.Button(self.lbl_frame_scegli, text='Inserisci', command=self.inserisci)
        self.btn_applica_filtro = ttk.Button(self.lbl_frame_filtra, text='Applica', command=self.filtra)
        '''
        Combobox per gestire rimpimento tramite classe prodotti
        '''
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.lbl_frame_filtra, textvariable=self.box_value)
        '''
        Labelframe Attributi Taglio
        '''
        self.lbl_frame_attributi_taglio = ttk.LabelFrame(self.frame_centrale,
                                                         text='Attributi taglio selezionato')
        self.flag1 = tk.Checkbutton(self.lbl_frame_attributi_taglio, text='Modulo Inventario')
        '''
        LAYOUT
        '''
        self.frame_sx.grid(row='1', column='0', sticky='n')
        self.frame_centrale.grid(row='1', column='1', sticky='n')
        self.frame_dx.grid(row='1', column='2', sticky='n')

        self.tree_tagli.grid(row='1', column='0', columnspan='3', sticky='we')
        self.lbl_frame_taglio_selezionato.grid(row='1', column='0', sticky='n')
        self.lbl_frame_attributi_taglio.grid(row=2, column=0)
        self.flag1.grid()
        self.lbl_frame_scegli.grid(row='4', column='0')
        self.lbl_frame_filtra.grid(row=3, column=0)
        self.btn_modifica.grid()
        self.btn_inserisci.grid()
        self.box.grid()
        self.btn_applica_filtro.grid()

        self.aggiorna()
        self.crea_label_entry()
        self.riempi_combo()

    def filtra(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        stringa = self.box_value.get()
        for lista in self.c.execute("SELECT * FROM tagli WHERE taglio like ?", ('%'+stringa+'%',)):
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1]))

    def riempi_combo(self):
        lista = []

        for row in self.c.execute("SELECT merceologia From merceologie WHERE flag2_taglio == '1' "):
            lista.extend(row)
        self.box['values'] = lista

        self.box.current(0)

    def crea_label_entry(self):
        r = 1
        c = 0
        for campo in self.campi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_taglio_selezionato, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.lbl_frame_taglio_selezionato)
            ent.grid(row=r, column=c+1)
            self.entry[campo] = ent
            r += 1

    def modifica(self):
        for campo in self.campi:
            stringa = 'UPDATE tagli SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()
        self.aggiorna()

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        self.c.execute('INSERT INTO tagli(taglio) VALUES (?)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        for lista in self.c.execute("SELECT * From tagli "):
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1]))

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        self.item = (self.tree_tagli.item(self.tree_tagli.selection(), 'values'))

        i = 1
        for self.row in self.c.execute("SELECT * FROM tagli WHERE ID = ?", (self.item[0],)):
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Tagli(notebook)
    notebook.add(new, text='Tagli')
    root.mainloop()