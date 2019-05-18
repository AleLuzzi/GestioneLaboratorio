import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import mysql.connector
import configparser


class Inventario(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Inventario")

        self.value = tk.StringVar()
        self.data = dt.date.today()
        self.config = self.leggi_file_ini()

        # connessione database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        # Definizione Frame
        self.frame_sx = tk.Frame(self)
        self.frame_dx = tk.Frame(self)

        self.notebook = ttk.Notebook(self.frame_dx)

        # TREEVIEW riepilogo inventario
        self.tree_riepilogo = ttk.Treeview(self.frame_sx, height=18)

        self.tree_riepilogo['columns'] = ('Taglio', 'Merceologia', 'Peso')
        self.tree_riepilogo['show'] = 'headings'
        self.tree_riepilogo.heading('Taglio', text="Taglio")
        self.tree_riepilogo.heading('Merceologia', text='Merceologia')
        self.tree_riepilogo.heading('Peso', text="Peso")

        self.tree_riepilogo.column("Peso", width=80)

        # LABEL che mostra il numero della settimana
        self.lbl_settimana = tk.Label(self.frame_dx, text='SETTIMANA NUMERO ',
                                      foreground='blue', font=('Verdana', 20), relief='ridge', padx=20)
        self.lbl_nr_settimana = tk.Label(self.frame_dx, text=str(1 + int(self.data.strftime('%W'))),
                                         font=('Verdana', 20), bg='white', relief='sunken', padx=20)

        # BUTTON elimina riga
        self.btn_rimuovi_riga = tk.Button(self.frame_sx,
                                          text="RIMUOVI RIGA",
                                          font=('Verdana', 15),
                                          command=self.rimuovi_riga_selezionata)

        # ENTRY peso inserito
        self.peso = tk.StringVar()
        self.ent_peso = tk.Entry(self.frame_sx, textvariable=self.peso, font=('Verdana', 15))

        self.img_btn_focus_ean = tk.PhotoImage(file=".//immagini//modifica.gif")
        self.btn_focus_ean = ttk.Button(self.frame_sx, image=self.img_btn_focus_ean, command=self.ent_peso.focus)

        # BUTTON inserimento peso
        self.btn_inserisci_peso = tk.Button(self.frame_sx, text='INSERISCI PESO', font=('Verdana', 15),
                                            command=self.ins_peso)

        # BUTTON salva dati
        self.btn_salva_dati = tk.Button(self.frame_dx, text='SALVA DATI', font=('Verdana', 15))

        # BUTTON chiudi finestra
        self.btn_chiudi = tk.Button(self.frame_dx, text='CHIUDI FINESTRA', font=('Verdana', 15), command=self.destroy)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, rowspan=2)
        self.frame_dx.grid(row=0, column=1, sticky='n')

        self.tree_riepilogo.grid(row=0, column=0, columnspan=3)
        self.btn_rimuovi_riga.grid(row=1, column=0, columnspan=3, sticky='we')
        self.ent_peso.grid(row=2, column=0)
        self.btn_focus_ean.grid(row=2, column=1)
        self.btn_inserisci_peso.grid(row=2, column=2)

        self.lbl_settimana.grid(row=0, column=0, sticky='we')
        self.lbl_nr_settimana.grid(row=0, column=1, sticky='we')
        self.notebook.grid(row=1, column=0, columnspan=2, sticky='we')

        self.btn_salva_dati.grid(row=2, column=0, sticky='we')
        self.btn_chiudi.grid(row=2, column=1, sticky='we')

        # TAB 1 AGNELLO
        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='AGNELLO', compound='left', image=self.img_btn1)

        lst_agnello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 12")
        for row in self.c:
            lst_agnello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_agnello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab1, text=lst_agnello[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_agnello[i]).grid(row=r, column=c)
            r += 1

        # TAB 2 BOVINO
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='BOVINO', compound='left', image=self.img_btn1)

        lst_bovino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 10")
        for row in self.c:
            lst_bovino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_bovino)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab2, text=lst_bovino[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_bovino[i]).grid(row=r, column=c)
            r += 1

        # TAB 3 SUINO
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='SUINO', compound='left', image=self.img_btn1)

        lst_suino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 11")
        for row in self.c:
            lst_suino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_suino)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab3, text=lst_suino[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_suino[i]).grid(row=r, column=c)
            r += 1

        # TAB 4 VITELLO
        self.tab4 = tk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='VITELLO', compound='left', image=self.img_btn1)

        lst_vitello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 13")
        for row in self.c:
            lst_vitello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_vitello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab4, text=lst_vitello[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_vitello[i]).grid(row=r, column=c)
            r += 1

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def rimuovi_riga_selezionata(self):
        curitem = self.tree_riepilogo.selection()[0]
        self.tree_riepilogo.delete(curitem)

    def ins_peso(self):
        if self.value.get() != '' and self.peso.get() != '':
            taglio = self.value.get()
            cat_merc = self.notebook.tab(self.notebook.select(), "text")
            self.c.execute("SELECT Id FROM merceologie WHERE merceologia = %s", (cat_merc,))
            id_merc = self.c.fetchone()
            dati = [taglio, id_merc, self.peso.get(), self.data]
            self.tree_riepilogo.insert('', 'end', values=(taglio, cat_merc, self.peso.get()))
            self.ent_peso.delete(0, tk.END)
            print(dati)
        else:
            messagebox.showinfo('ATTENZIONE', 'dati mancanti.. controlla!!!')


if __name__ == '__main__':
    root = tk.Tk()
    new = Inventario()
    root.mainloop()
