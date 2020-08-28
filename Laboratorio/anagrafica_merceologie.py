import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import configparser


class MerceologieCucina(tk.Toplevel):
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

        # Definizione Frame
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        # TREEVIEW per tab Merceologie
        self.tree_merceologie = ttk.Treeview(self.frame_sx, height=23)
        self.tree_merceologie['columns'] = ('Id', 'Merceologia', 'Reparto')
        self.tree_merceologie['show'] = 'headings'
        self.tree_merceologie.heading('Id', text="Id")
        self.tree_merceologie.heading('Merceologia', text="Merceologia")
        self.tree_merceologie.heading('Reparto', text='Reparto')

        self.tree_merceologie.column("Id", width=10)
        self.tree_merceologie.column("Merceologia", width=150)
        self.tree_merceologie.column("Reparto", width=100)

        self.tree_merceologie.bind("<Double-1>", self._ondoubleclick)

        # Lista campi del record
        self.attributi = ['Mostra nel modulo Inventario', 'Mostra nel Tab Tagli', 'Mostra nel Tab ingredienti base']
        self.label = {}
        self.ckbutton = {}

        # LABELFRAME dettagli reparto selezionato
        self.lbl_frame_merceologia_selezionata = tk.LabelFrame(self.frame_centrale,
                                                               text='Dettagli merceologia selezionata',
                                                               font=('Verdana', 15))

        self.lbl_frame_attributi_merceologia = tk.LabelFrame(self.frame_centrale,
                                                             text='Attributi merceologia selezionata',
                                                             font=('Verdana', 15))

        # crea LABEL ed ENTRY merceologia
        self.lbl_merceologia = tk.Label(self.lbl_frame_merceologia_selezionata,
                                        text='MERCEOLOGIA')
        self.entry_merceologia = tk.Entry(self.lbl_frame_merceologia_selezionata)

        # CMB BOX e LABEL per scelta reparto merceologia
        self.lbl_reparto = tk.Label(self.lbl_frame_merceologia_selezionata,
                                    text='REPARTO')

        self.cmb_box_reparto_value = tk.StringVar()
        self.cmb_box_reparto = ttk.Combobox(self.lbl_frame_merceologia_selezionata,
                                            textvariable=self.cmb_box_reparto_value)

        lista_reparti = []

        self.c.execute("SELECT reparto From reparti")
        for row in self.c:
            lista_reparti.extend(row)
        self.cmb_box_reparto['values'] = lista_reparti

        # crea ATTRIBUTI
        r = 1
        c = 0
        for attributo in self.attributi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_attributi_merceologia, text=attributo)
            lbl.grid(row=r, column=c)
            self.label[attributo] = lbl

            self.valore_flag[attributo] = tk.IntVar()
            ckbtn = tk.Checkbutton(self.lbl_frame_attributi_merceologia, variable=self.valore_flag[attributo])
            ckbtn.grid(row=r, column=c + 1)
            self.ckbutton[attributo] = ckbtn
            r += 1

        # LABELFRAME scegli prodotto
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx, text='')
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Verdana', 10),
                                      command=self._modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Verdana', 10),
                                       command=self._inserisci)

        self._aggiorna()

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.tree_merceologie.grid(row=1, column=0, columnspan=3, sticky='ns')

        self.lbl_frame_merceologia_selezionata.grid(row=1, column=0, sticky='n')
        self.lbl_merceologia.grid(row=0, column=0)
        self.entry_merceologia.grid(row=0, column=1)
        self.lbl_reparto.grid(row=1, column=0, pady=10)
        self.cmb_box_reparto.grid(row=1, column=1, pady=10)

        self.lbl_frame_attributi_merceologia.grid(row=2, column=0)

        self.lbl_frame_scegli.grid(row=3, column=0)
        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

    @staticmethod
    def _leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def _modifica(self):
        valori_da_salvare = []
        stringa = 'UPDATE merceologie SET merceologia=%s WHERE ID = %s'
        self.c.execute(stringa, (self.entry_merceologia.get(), (self.item[0])))
        self.conn.commit()
        rep = self.cmb_box_reparto_value.get()
        self.c.execute("SELECT Id FROM reparti WHERE reparto = %s", (rep,))
        id_rep = []
        id_rep.extend(self.c.fetchone())
        id_rep.append(self.item[0])
        stringa = 'UPDATE merceologie SET id_reparto = %s WHERE ID = %s'
        self.c.execute(stringa, id_rep)
        self.conn.commit()

        for attributo in self.attributi:
            valori_da_salvare.append(self.valore_flag[attributo].get())

        stringa = 'UPDATE merceologie SET flag1_inv=%s , flag2_taglio=%s , flag3_ing_base=%s WHERE ID = %s'
        self.c.execute(stringa, (valori_da_salvare[0], valori_da_salvare[1], valori_da_salvare[2], (self.item[0])))
        self.conn.commit()
        self._aggiorna()

    def _aggiorna(self):
        self.tree_merceologie.delete(*self.tree_merceologie.get_children())
        self.c.execute("SELECT * From merceologie, reparti "
                       "WHERE merceologie.id_reparto = reparti.id")
        for lista in self.c:
            self.tree_merceologie.insert('', 'end', values=(lista[0], lista[1], lista[7]))

    def _ondoubleclick(self, event):
        self.entry_merceologia.delete(0, 'end')
        for attributo in self.attributi:
            self.ckbutton[attributo].deselect()
        self.item = event.widget.item(self.tree_merceologie.selection(), 'values')
        stringa = "SELECT * FROM merceologie, reparti WHERE merceologie.ID = %s AND merceologie.id_reparto = reparti.id"
        self.c.execute(stringa, (self.item[0],))
        for self.row in self.c:
            self.entry_merceologia.insert(0, self.row[1])
            self.cmb_box_reparto_value.set(self.row[7])

            i = 2
            for attributo in self.attributi:
                if self.row[i] == 1:
                    self.ckbutton[attributo].select()
                i += 1

    def _inserisci(self):

        def _centra(toplevel):
            screen_width = toplevel.winfo_screenwidth()
            screen_height = toplevel.winfo_screenheight()

            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = screen_width / 3 - size[0] / 2
            y = screen_height / 3 - size[1] / 2

            toplevel.geometry("+%d+%d" % (x, y))

        def _salva_nuovo():
            rep = rep_new.get()
            if rep != '' and merc_new.get() != '':
                self.c.execute("SELECT Id FROM reparti WHERE reparto = %s", (rep,))
                lista_da_salvare = [merc_new.get(), self.c.fetchone()[0], flag1.get(), flag2.get(), flag3.get()]
                print(lista_da_salvare)
                self.c.execute('INSERT INTO merceologie(merceologia,Id_Reparto,flag1_inv,flag2_taglio,flag3_ing_base) '
                               'VALUES (%s,%s,%s,%s,%s)', lista_da_salvare)
                self.conn.commit()
                self._aggiorna()
                nuovo_dato.destroy()
            else:
                messagebox.showinfo('ATTENZIONE', 'CI SONO CAMPI VUOTI')

        nuovo_dato = tk.Toplevel()

        _centra(nuovo_dato)

        merc_new = tk.StringVar()
        rep_new = tk.StringVar()
        flag1 = tk.IntVar()
        flag2 = tk.IntVar()
        flag3 = tk.IntVar()

        lbl_merceologia = tk.Label(nuovo_dato, text='Merceologia')
        ent_merceologia = tk.Entry(nuovo_dato, textvariable=merc_new)

        lbl_reparto = tk.Label(nuovo_dato, text='Reparto')
        cmb_reparto = ttk.Combobox(nuovo_dato, textvariable=rep_new)
        lista_reparti_new = []

        self.c.execute("SELECT reparto From reparti")
        for row in self.c:
            lista_reparti_new.extend(row)
        cmb_reparto['values'] = lista_reparti_new

        lbl_attributo_1 = tk.Label(nuovo_dato, text='Mostra nel modulo Inventario')
        ckbtn_1 = tk.Checkbutton(nuovo_dato, variable=flag1)
        lbl_attributo_2 = tk.Label(nuovo_dato, text='Mostra nel Tab Tagli')
        ckbtn_2 = tk.Checkbutton(nuovo_dato, variable=flag2)
        lbl_attributo_3 = tk.Label(nuovo_dato, text='Mostra nel Tab ingredienti base')
        ckbtn_3 = tk.Checkbutton(nuovo_dato, variable=flag3)

        btn_salva = tk.Button(nuovo_dato, text='Salva Dati', command=_salva_nuovo)
        btn_chiudi = tk.Button(nuovo_dato, text='Chiudi', command=nuovo_dato.destroy)

        lbl_merceologia.grid(row=0, column=0)
        ent_merceologia.grid(row=0, column=2, sticky='we')
        lbl_reparto.grid(row=1, column=0)
        cmb_reparto.grid(row=1, column=2)

        lbl_attributo_1.grid(row=2, column=0)
        ckbtn_1.grid(row=2, column=1)
        lbl_attributo_2.grid(row=3, column=0)
        ckbtn_2.grid(row=3, column=1)
        lbl_attributo_3.grid(row=4, column=0)
        ckbtn_3.grid(row=4, column=1)

        btn_salva.grid(row=3, column=2, sticky='we')
        btn_chiudi.grid(row=4, column=2, sticky='we')


if __name__ == '__main__':
    root = tk.Tk()
    new = MerceologieCucina()
    root.mainloop()
