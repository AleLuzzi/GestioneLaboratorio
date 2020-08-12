import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import configparser


class Fornitori(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)

        self.item = ''
        self.valore_flag = dict()
        self.config = self._leggi_file_ini()

        # Connessione al Database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
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

        self.tree_fornitori.bind("<Double-1>", self._ondoubleclick)

        # LABELFRAME dettagli fornitore selezionato
        self.lbl_frame_dettagli_selezionato = tk.LabelFrame(self.frame_centrale, text='Dettagli fornitore selezionato',
                                                            font=('Verdana', 15))
        self.lbl_frame_attributi_fornitori = tk.LabelFrame(self.frame_centrale, text='Attributi fornitore selezionato',
                                                           font=('Verdana', 15))

        # Label ed Entry per mostrare dettagli fornitore selezionato
        self.lbl_azienda = tk.Label(self.lbl_frame_dettagli_selezionato, text='Fornitore')
        self.ent_azienda = tk.Entry(self.lbl_frame_dettagli_selezionato, width=25)

        # Label e flag per mostrare attributi del fornitore
        self.lbl_flag_ing_merce = tk.Label(self.lbl_frame_attributi_fornitori, text='Ingresso Merce')
        self.valore_flag_ing_merce = tk.IntVar()
        self.ckbtn_ing_merce = tk.Checkbutton(self.lbl_frame_attributi_fornitori, variable=self.valore_flag_ing_merce)

        self.lbl_flag_inv = tk.Label(self.lbl_frame_attributi_fornitori, text='Inventario')
        self.valore_flag_inv = tk.IntVar()
        self.ckbtn_inv = tk.Checkbutton(self.lbl_frame_attributi_fornitori, variable=self.valore_flag_inv)

        # LABELFRAME scegli prodotto
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx)
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva modifiche',
                                      font=('Verdana', 10),
                                      command=self._modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Verdana', 10),
                                       command=self._inserisci)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, sticky='n')
        self.frame_centrale.grid(row=0, column=1, sticky='n')
        self.frame_dx.grid(row=0, column=2, sticky='n')

        self.tree_fornitori.grid(row=1, column=0, columnspan=3, sticky='we')
        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_azienda.grid(row=0, column=0)
        self.ent_azienda.grid(row=0, column=1)

        self.lbl_frame_attributi_fornitori.grid(row=2, column=0)
        self.lbl_flag_ing_merce.grid(row=0, column=0)
        self.ckbtn_ing_merce.grid(row=0, column=1)
        self.lbl_flag_inv.grid(row=1, column=0)
        self.ckbtn_inv.grid(row=1, column=1)

        self.lbl_frame_scegli.grid(row=3, column=0)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

        self._aggiorna()

    @staticmethod
    def _leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def _modifica(self):
        self.item = self.tree_fornitori.item(self.tree_fornitori.selection(), 'values')
        if self.item:
            lista = [self.ent_azienda.get(), self.valore_flag_ing_merce.get(), self.valore_flag_inv.get(), self.item[0]]
            stringa = 'UPDATE fornitori SET azienda = %s, flag1_ing_merce = %s, flag2_inventario = %s WHERE ID = %s'
            self.c.execute(stringa, lista)
            self.conn.commit()
            self._aggiorna()
        else:
            messagebox.showinfo("ATTENZIONE", "Non hai selezionato nessun record")

    def _inserisci(self):

        def _centra(toplevel):
            screen_width = toplevel.winfo_screenwidth()
            screen_height = toplevel.winfo_screenheight()

            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = screen_width / 3 - size[0] / 2
            y = screen_height / 3 - size[1] / 2

            toplevel.geometry("+%d+%d" % (x, y))

        def _salva_nuovo():
            if ent_azienda_new.get() != '':
                lista_da_salvare = [ent_azienda_new.get(), ckbtn_ing_merce_value.get(), ckbtn_inventario_value.get()]
                self.c.execute('INSERT INTO fornitori(azienda,flag1_ing_merce,flag2_inventario)'
                               'VALUES (%s,%s,%s)', lista_da_salvare)
                self.conn.commit()
                self._aggiorna()
                nuovo_fornitore.destroy()
            else:
                messagebox.showinfo('ATTENZIONE', 'Nome azienda non inserito')

        nuovo_fornitore = tk.Toplevel()
        _centra(nuovo_fornitore)

        azienda_new = tk.StringVar()
        ckbtn_ing_merce_value = tk.IntVar()
        ckbtn_inventario_value = tk.IntVar()

        lbl_azienda_new = tk.Label(nuovo_fornitore, text='Fornitore')
        ent_azienda_new = tk.Entry(nuovo_fornitore, textvariable=azienda_new)
        lblfrm_scelta_attributi = tk.LabelFrame(nuovo_fornitore, text='Mostra nei moduli:')
        lbl_ingresso_merce = tk.Label(lblfrm_scelta_attributi, text='Ingresso Merce')
        ckbtn_ingresso_merce = tk.Checkbutton(lblfrm_scelta_attributi, variable=ckbtn_ing_merce_value)
        lbl_inventario = tk.Label(lblfrm_scelta_attributi, text='Inventario')
        ckbtn_inventario = tk.Checkbutton(lblfrm_scelta_attributi, variable=ckbtn_inventario_value)

        btn_salva = tk.Button(nuovo_fornitore, text='Salva Dati', command=_salva_nuovo)
        btn_chiudi = tk.Button(nuovo_fornitore, text='Chiudi', command=nuovo_fornitore.destroy)

        lbl_azienda_new.grid(row=0, column=0)
        ent_azienda_new.grid(row=0, column=1)
        lblfrm_scelta_attributi.grid(row=1, column=0, columnspan=2, sticky='we')
        lbl_ingresso_merce.grid(row=0, column=0)
        ckbtn_ingresso_merce.grid(row=0, column=1)
        lbl_inventario.grid(row=1, column=0)
        ckbtn_inventario.grid(row=1, column=1)

        btn_salva.grid(row=2, column=0, sticky='we')
        btn_chiudi.grid(row=2, column=1, sticky='we')
        self._aggiorna()

    def _aggiorna(self):
        self.tree_fornitori.delete(*self.tree_fornitori.get_children())
        self.c.execute("SELECT * From fornitori ")
        for lista in self.c:
            self.tree_fornitori.insert('', 'end', values=(lista[0], lista[1]))

        lista = []

        self.c.execute("SELECT ID From fornitori")
        for row in self.c:
            lista.extend(row)

    def _ondoubleclick(self, event):
        self.ent_azienda.delete(0, 'end')
        self.ckbtn_ing_merce.deselect()
        self.ckbtn_inv.deselect()

        self.item = event.widget.item(self.tree_fornitori.selection(), 'values')

        self.c.execute("SELECT * FROM fornitori WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            self.ent_azienda.insert(0, self.row[1])
            if self.row[2] == 1:
                self.ckbtn_ing_merce.select()
            else:
                pass
            if self.row[3] == 1:
                self.ckbtn_inv.select()
            else:
                pass


if __name__ == '__main__':
    root = tk.Tk()
    new = Fornitori()
    root.mainloop()
