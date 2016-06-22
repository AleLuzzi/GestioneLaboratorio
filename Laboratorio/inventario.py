import tkinter as tk
from tkinter import ttk
# import datetime
import sqlite3


class Inventario(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Inventario")
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())
        '''
        Connessione al database
        '''
        self.conn = sqlite3.connect('../Laboratorio/data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Frame per impaginazione
        '''
        self.frame_alto = tk.Frame(self, background='yellow')
        self.frame_sx = tk.Frame(self, bd=3, relief='groove')
        self.frame_dx = tk.Frame(self, bd=3, relief='groove')
        self.frame_basso = tk.Frame(self)
        self.frame_classe = tk.Frame(self, bd=3, background='white', relief='groove')
        '''
        Creazione TREEVIEW
        '''
        self.tree = ttk.Treeview(self.frame_alto, height=8)
        self.tree['columns'] = ('fornitore', 'prodotto', 'quantita')
        self.tree['show'] = 'headings'
        self.tree.column("fornitore", width=100)
        self.tree.column("prodotto", width=100)
        self.tree.column("quantita", width=100)
        self.tree.heading("fornitore", text="Fornitore")
        self.tree.heading("prodotto", text="Prodotto")
        self.tree.heading("quantita", text="quantita")
        '''
        Labelframe per creazione bottoni scelta fornitore
        '''
        self.labelframe_fornitori = ttk.Labelframe(self.frame_sx, text="Fornitore")
        self.labelframe_tagli = ttk.Labelframe(self.frame_dx, text="Taglio")
        '''
        LAYOUT
        '''
        self.frame_alto.grid(row='1', column='0', columnspan='2')
        self.frame_sx.grid(row='2', column='0')
        self.frame_dx.grid(row='2', column='1', sticky='ns')
        self.frame_basso.grid(row='3', column='0', columnspan='2')
        self.frame_classe.grid(row=4, column=0, columnspan=2)

        self.tree.grid(row='1', column='0', columnspan='2', pady='5')
        self.labelframe_fornitori.grid(row='2', column='0', sticky='n')
        self.labelframe_tagli.grid(row='2', column='0')

        self.fornitore = tk.StringVar()
        self.classe = tk.StringVar()
        self.taglio = tk.StringVar()
        self.classe.set('Agnello')

        self.crea_bottoni_fornitori()
        self.crea_bottoni_tagli()
        self.crea_radiobtn_classe()

    def crea_bottoni_fornitori(self):
        lista_fornitori = []
        for row in self.c.execute("SELECT azienda FROM fornitori"):
            lista_fornitori.extend(row)

        row, col = 1, 0
        for i in range(0, len(lista_fornitori)):
            if row % 6 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_fornitori, text=str(lista_fornitori[i]).upper(), variable=self.fornitore,
                           width=20, indicatoron=0, value=lista_fornitori[i],
                           font='Helvetica').grid(row=row, column=col, sticky='w')
            row += 1

    def crea_bottoni_tagli(self):
        for label in self.labelframe_tagli.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()
        lista_tagli = []
        stringa = self.classe.get()
        for row in self.c.execute("SELECT taglio FROM tagli WHERE taglio like ?", ('%'+stringa+'%',)):
            lista_tagli.extend(row)

        row, col = 1, 0
        for i in range(0, len(lista_tagli)):
            if row % 6 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe_tagli, text=str(lista_tagli[i]).upper(), variable=self.taglio,
                           width=20, indicatoron=0, value=lista_tagli[i],
                           font='Helvetica').grid(row=row, column=col, sticky='w')
            row += 1

    def crea_radiobtn_classe(self):
        lista_classi = []
        for row in self.c.execute("SELECT merceologia FROM merceologie WHERE flag1_inv = '1'"):
            lista_classi.extend(row)

        lista_classi.sort()
        col = 0
        for i in range(0, len(lista_classi)):
            tk.Radiobutton(self.frame_classe, text=str(lista_classi[i]).upper(), variable=self.classe, indicatoron=0,
                           value=lista_classi[i], font='Helvetica',
                           command=self.crea_bottoni_tagli).grid(row=1, column=col, padx=10, pady=20, sticky='w')
            col += 1

if __name__ == '__main__':
    root = tk.Tk()
    new = Inventario()
    root.mainloop()
