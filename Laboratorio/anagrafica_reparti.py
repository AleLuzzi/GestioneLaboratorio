import tkinter as tk
from tkinter import ttk
import sqlite3


class Reparti(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''

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
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)
        '''
        Treeview per tab Reparti
        '''
        self.tree_reparti = ttk.Treeview(self.frame_sx, height=23)
        self.tree_reparti['columns'] = ('Id', 'Reparto')
        self.tree_reparti['show'] = 'headings'
        self.tree_reparti.heading('Id', text="Id")
        self.tree_reparti.heading('Reparto', text="Reparto")

        self.tree_reparti.column("Id", width=10)
        self.tree_reparti.column("Reparto", width=150)

        self.tree_reparti.bind("<Double-1>", self.ondoubleclick)

        '''
        Lista campi del record
        '''
        self.campi = ['reparto']
        self.label = {}
        self.entry = {}
        '''
        Labelframe dettagli reparto selezionato
        '''
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_centrale, text='Dettagli reparto selezionato')
        '''
        Labelframe scegli prodotto
        '''
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_centrale, text='Azioni')
        self.btn_modifica = ttk.Button(self.lbl_frame_scegli, text='Modifica', command=self.modifica)
        self.btn_inserisci = ttk.Button(self.lbl_frame_scegli, text='Inserisci', command=self.inserisci)

        self.aggiorna()
        self.crea_label_entry()

        '''
        LAYOUT
        '''
        self.frame_sx.grid(row='1', column='0', sticky='n')
        self.frame_centrale.grid(row='1', column='1', sticky='n')
        self.frame_dx.grid(row='1', column='2', sticky='n')

        self.tree_reparti.grid(row='1', column='0', columnspan='3', sticky='we')
        self.lbl_frame_dettagli_selezionato.grid(row='1', column='0', sticky='n')
        self.lbl_frame_scegli.grid(row='2', column='0')
        self.btn_modifica.grid()
        self.btn_inserisci.grid()

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

    def modifica(self):
        for campo in self.campi:
            stringa = 'UPDATE reparti SET {}=? WHERE ID = ?'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()
        self.aggiorna()

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        self.c.execute('INSERT INTO reparti(reparto) VALUES (?)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_reparti.delete(*self.tree_reparti.get_children())
        for lista in self.c.execute("SELECT * From reparti "):
            self.tree_reparti.insert('', 'end', values=(lista[0], lista[1]))
        lista = []

        for row in self.c.execute("SELECT ID From reparti"):
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        self.item = (self.tree_reparti.item(self.tree_reparti.selection(), 'values'))

        i = 1
        for self.row in self.c.execute("SELECT * FROM reparti WHERE ID = ?", (self.item[0],)):
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Reparti(notebook)
    notebook.add(new, text='Reparti')
    root.mainloop()