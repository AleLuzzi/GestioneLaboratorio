import tkinter as tk
from tkinter import ttk
import mysql.connector
import configparser


class Tagli(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)

        self.item = ''
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

        # TREEVIEEW per tab Tagli
        self.tree_tagli = ttk.Treeview(self.frame_sx, height=23)
        self.tree_tagli['columns'] = ('Id', 'Tagli', 'Merceologia')
        self.tree_tagli['show'] = 'headings'
        self.tree_tagli.heading('Id', text="Id")
        self.tree_tagli.heading('Tagli', text="Tagli")
        self.tree_tagli.heading('Merceologia', text="Merceologia")

        self.tree_tagli.column("Id", width=20)
        self.tree_tagli.column("Tagli", width=150)
        self.tree_tagli.column("Merceologia", width=150)

        self.tree_tagli.bind("<Double-1>", self.ondoubleclick)

        # LABELFRAME dettagli taglio selezionato
        self.lbl_frame_taglio_selezionato = tk.LabelFrame(self.frame_centrale,
                                                          font=('Verdana', 15),
                                                          text='Dettagli taglio selezionato')
        self.lbl_taglio = tk.Label(self.lbl_frame_taglio_selezionato,
                                   text='TAGLIO')
        self.lbl_merceologia = tk.Label(self.lbl_frame_taglio_selezionato,
                                        text='MERCEOLOGIA')

        # CMB BOX per scelta merceologia taglio
        self.cmb_box_merc_value = tk.StringVar()
        self.cmb_box_merceologia = ttk.Combobox(self.lbl_frame_taglio_selezionato, textvariable=self.cmb_box_merc_value)

        lista_merceologie = []

        self.c.execute("SELECT merceologia From merceologie")
        for row in self.c:
            lista_merceologie.extend(row)
        self.cmb_box_merceologia['values'] = lista_merceologie

        # ENTRY per la descrizione del taglio
        self.entry_taglio = tk.Entry(self.lbl_frame_taglio_selezionato)

        # LABELFRAME Azioni e filtra
        self.lbl_frame_scegli = tk.LabelFrame(self.frame_dx,
                                              text='')
        self.lbl_frame_filtra = tk.LabelFrame(self.frame_centrale,
                                              font=('Verdana', 15),
                                              text='Filtra')

        # BOTTONI
        self.btn_salva_modifiche = tk.Button(self.lbl_frame_scegli,
                                             text='Salva Modifiche',
                                             font=('Helvetica', 10),
                                             command=self.modifica)

        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self.inserisci)

        self.btn_cancella = tk.Button(self.lbl_frame_scegli,
                                      text='Cancella riga',
                                      font=('Helvetica', 10),
                                      command=self.cancella)

        self.btn_mostra_tutti = tk.Button(self.lbl_frame_scegli,
                                          text='Mostra tutti',
                                          font=('Helvetica', 10),
                                          command=self.aggiorna)

        self.btn_applica_filtro = tk.Button(self.lbl_frame_filtra,
                                            text='Applica',
                                            font=('Helvetica', 10),
                                            padx=30,
                                            command=self.filtra)

        # COMBOBOX per gestire rimpimento tramite classe prodotti
        self.box_value = tk.StringVar()
        self.cmb_box_filtro = ttk.Combobox(self.lbl_frame_filtra, textvariable=self.box_value)

        lista = []

        self.c.execute("SELECT merceologia From merceologie WHERE flag2_taglio = '1' ")
        for row in self.c:
            lista.extend(row)
        self.cmb_box_filtro['values'] = lista

        self.cmb_box_filtro.current(0)

        self.flag1 = tk.Checkbutton(self.lbl_frame_taglio_selezionato, text='Visualizza nel modulo Inventario')

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.tree_tagli.grid(row=1, column=0, columnspan=3, sticky='we')

        self.lbl_frame_taglio_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_taglio.grid(row=0, column=0, pady=10)
        self.entry_taglio.grid(row=0, column=1, pady=10)

        self.lbl_merceologia.grid(row=1, column=0, pady=10)
        self.cmb_box_merceologia.grid(row=1, column=1, pady=10)

        self.flag1.grid(row=2, column=0, columnspan=2)

        self.lbl_frame_scegli.grid(row=4, column=0)
        self.lbl_frame_filtra.grid(row=3, column=0, sticky='we')

        self.btn_salva_modifiche.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')
        self.btn_cancella.grid(sticky='we')
        self.btn_mostra_tutti.grid(sticky='we')

        self.cmb_box_filtro.grid(row=0, column=0, padx=10)
        self.btn_applica_filtro.grid(row=0, column=1, sticky='we')

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def filtra(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        stringa = self.box_value.get()
        self.c.execute("SELECT * FROM tagli, merceologie "
                       "WHERE merceologia like %s AND tagli.id_merceologia = merceologie.id", ('%' + stringa + '%',))
        for lista in self.c:
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1], lista[4]))

    def modifica(self):
        stringa = 'UPDATE tagli SET taglio=%s WHERE ID = %s'
        self.c.execute(stringa, (self.entry_taglio.get(), (self.item[0])))
        self.conn.commit()
        merc = self.cmb_box_merc_value.get()
        self.c.execute("SELECT Id FROM merceologie WHERE merceologia = %s", (merc,))
        id_merc = []
        id_merc.extend(self.c.fetchone())
        id_merc.append(self.item[0])
        stringa = 'UPDATE tagli SET id_merceologia = %s WHERE ID = %s'
        self.c.execute(stringa, id_merc)
        self.conn.commit()
        self.filtra()

    def inserisci(self):
        lista_da_salvare = [self.entry_taglio.get()]
        merc = self.cmb_box_merc_value.get()
        self.c.execute("SELECT Id FROM merceologie WHERE merceologia = %s", (merc,))
        lista_da_salvare.extend(self.c.fetchone())
        self.c.execute('INSERT INTO tagli(taglio,Id_Merceologia) VALUES (%s,%s)', lista_da_salvare)
        self.conn.commit()

    def cancella(self):
        stringa = 'DELETE FROM tagli WHERE tagli.id = %s'
        self.c.execute(stringa, (self.item[0],))
        self.conn.commit()

    def aggiorna(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        self.c.execute("SELECT * FROM tagli, merceologie "
                       "WHERE tagli.id_merceologia = merceologie.id")
        for lista in self.c:
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1], lista[4]))

    def ondoubleclick(self, event):
        self.entry_taglio.delete(0, 'end')
        self.item = (self.tree_tagli.item(self.tree_tagli.selection(), 'values'))
        stringa = "SELECT * FROM tagli, merceologie WHERE tagli.ID = %s AND tagli.id_merceologia = merceologie.id"
        self.c.execute(stringa, (self.item[0],))
        for self.row in self.c:
            self.entry_taglio.insert(0, self.row[1])
            self.cmb_box_merc_value.set(self.row[4])


if __name__ == '__main__':
    root = tk.Tk()
    new = Tagli()
    root.mainloop()
