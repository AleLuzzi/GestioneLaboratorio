import tkinter as tk
from tkinter import ttk
import mysql.connector


class Tagli(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''

        # Connessione al Database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        # Definizione Frame
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        # TREEVIEEW per tab Tagli
        self.tree_tagli = ttk.Treeview(self.frame_sx, height=23)
        self.tree_tagli['columns'] = ('Id', 'Tagli')
        self.tree_tagli['show'] = 'headings'
        self.tree_tagli.heading('Id', text="Id")
        self.tree_tagli.heading('Tagli', text="Tagli")

        self.tree_tagli.column("Id", width=10)
        self.tree_tagli.column("Tagli", width=150)

        self.tree_tagli.bind("<Double-1>", self.ondoubleclick)

        # Lista campi del record
        self.campi = ['taglio']
        self.label = {}
        self.entry = {}

        # LABELFRAME dettagli taglio selezionato
        self.lbl_frame_taglio_selezionato = tk.LabelFrame(self.frame_centrale,
                                                          font=('Verdana', 15),
                                                          text='Dettagli taglio selezionato')

        # LABELFRAME Azioni e filtra
        self.lbl_frame_scegli = tk.LabelFrame(self.frame_dx,
                                              text='')
        self.lbl_frame_filtra = tk.LabelFrame(self.frame_centrale,
                                              font=('Verdana', 15),
                                              text='Filtra')

        # BOTTONI
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Helvetica', 10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self.inserisci)
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

        # LABELFRAME Attributi Taglio
        self.lbl_frame_attributi_taglio = tk.LabelFrame(self.frame_centrale,
                                                        font=('Verdana', 15),
                                                        text='Attributi taglio selezionato')
        self.flag1 = tk.Checkbutton(self.lbl_frame_attributi_taglio, text='Modulo Inventario')

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.tree_tagli.grid(row=1, column=0, columnspan=3, sticky='we')
        self.lbl_frame_taglio_selezionato.grid(row=1, column=0, sticky='n')
        self.lbl_frame_attributi_taglio.grid(row=2, column=0)
        self.flag1.grid()
        self.lbl_frame_scegli.grid(row=4, column=0)
        self.lbl_frame_filtra.grid(row=3, column=0, sticky='we')

        self.btn_modifica.grid(sticky='we')
        self.btn_inserisci.grid(sticky='we')

        self.cmb_box_filtro.grid(row=0, column=0, padx=10)
        self.btn_applica_filtro.grid(row=0, column=1, sticky='we')

        self.crea_label_entry()

    def filtra(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        stringa = self.box_value.get()
        self.c.execute("SELECT * FROM tagli WHERE taglio like %s", ('%' + stringa + '%',))
        for lista in self.c:
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1]))

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
            stringa = 'UPDATE tagli SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()
        self.aggiorna()

    def inserisci(self):
        lista_da_salvare = []
        for campo in self.campi:
            lista_da_salvare.append(self.entry[campo].get())
        self.c.execute('INSERT INTO tagli(taglio) VALUES (%s)', lista_da_salvare)
        self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_tagli.delete(*self.tree_tagli.get_children())
        self.c.execute("SELECT * From tagli ")
        for lista in self.c:
            self.tree_tagli.insert('', 'end', values=(lista[0], lista[1]))

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        self.item = (self.tree_tagli.item(self.tree_tagli.selection(), 'values'))

        i = 1
        self.c.execute("SELECT * FROM tagli WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
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
