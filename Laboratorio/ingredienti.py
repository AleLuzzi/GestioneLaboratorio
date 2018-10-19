import tkinter as tk
from tkinter import ttk
import datetime
import mysql.connector


class Ingredienti(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Ingredienti")
        self.geometry("1024x525+0+0")

        self.lista_da_salvare = []
        self.value = tk.StringVar()
        self.peso = tk.StringVar()
        self.peso.set('')
        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        # connessione database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='db_prova',
                                            user='prova',
                                            password='')
        self.c = self.conn.cursor()

        # FRAME definizione
        self.frame_sx = tk.Frame(self, bd=3, relief='groove')
        self.frame_dx = tk.Frame(self, bd=3, relief='groove')
        self.frame_basso = tk.Frame(self, background='white')

        # LABEL che mostra il numero della settimana
        self.data = datetime.date.today()
        self.n_sett = str(1 + int(self.data.strftime('%W')))
        self.lbl_settimana = ttk.Label(self.frame_sx, text='SETTIMANA NUMERO ' + self.n_sett,
                                       foreground='blue', font=('Verdana', 20))
        self.label_data_utilizzo = ttk.Label(self.frame_sx,
                                             text="Data Utilizzo Merce", foreground='blue', font=('Verdana', 20))
        self.label_data = ttk.Label(self.frame_sx, anchor='center',
                                    text=self.data.strftime('%d/%m/%y'), font=('Verdana', 20))

        # TREEVIEW per riepilogo ingredienti inseriti
        self.tree = ttk.Treeview(self.frame_sx)
        self.tree['columns'] = ('n_settimana', 'articolo', 'quantita', 'data', 'cod_ean')
        self.tree['show'] = 'headings'
        self.tree['displaycolumns'] = ('articolo', 'quantita', 'cod_ean')
        self.tree.column("articolo", width=200)
        self.tree.column("quantita", width=100)
        self.tree.column("cod_ean", width=100)
        self.tree.heading("articolo", text="articolo")
        self.tree.heading("quantita", text="quantita")
        self.tree.heading("cod_ean", text="Cod EAN")

        # BOTTONE elimina riga
        self.btn_elimina_riga = tk.Button(self.frame_sx,
                                          text='Elimina riga',
                                          font=('Verdana', 15),
                                          command=self.rimuovi_riga_selezionata)

        # LABEL peso da inserire
        self.lbl_peso = ttk.Label(self.frame_sx, text='Quantità merce utilizzata',
                                  foreground='blue',
                                  font=('Verdana', 15))

        # ENTRY peso da inserire
        self.entry_peso = ttk.Entry(self.frame_sx,
                                    textvariable=self.peso,
                                    font=('Verdana', 10))

        # LABELFRAME per inserimento EAN
        self.lblfr_ins_ean = tk.LabelFrame(self.frame_sx,
                                           text='Inserimento ean',
                                           font=('Verdana', 15),
                                           labelanchor='n')

        # NOTEBOOK e posizione
        self.notebook = ttk.Notebook(self.frame_dx)
        self.notebook.bind_all("<<NotebookTabChanged>>", self.rimetti_focus)

        # Definizione dizionari per ingredienti
        self.lista_surgelati = {'spinaci': '1950', 'cicoria': '1973', 'seppia': '2033', 'baccala': '2038',
                                'pangasio': '2025', 'frittura pesce': '1984', 'spiedini pesce': '2024',
                                'carciofi': '2012', 'fil.gallinella': '2052', 'gamberi 50-60': '1992',
                                'fagiolini': '1919', 'melanzane grigliate': '2016', 'lasagna sfoglia': '2000',
                                'filetto orata': '2028', 'orata': '2045', 'halibut': '2050',
                                'minestrone di verdure': '1955'}
        self.lista_freschi = {'pecorino romano': '010082', 'mozzarella': '010325', 'grana padano': '010080',
                              'prosc.cotto': '010332', 'ricotta mista': '010020', 'uova': 'uova medie sciolte'}
        # self.lista_pasta_fresca = {'gnocchi': '010031', 'ciriole': '010032', 'fettuccine': '010034'}
        self.lista_carne = {'pollo ruspante': '030115', 'cosce pollo': '030182', 'piccioni': '030207',
                            'petto tacchino': '030135', 'magro suino': '030121', 'pancia suino': '030111',
                            'salsicce fresche': '030130', 'macinato magro': '030119', 'spalla agnello': '030104',
                            'carne x gnocchi': '030139', 'cotolette agnello': '030105', 'trippa bovino': '030192',
                            'coratella agnello': '030106', 'magro vitella': '030163', 'petto pollo': '030114',
                            'macinato x polpette': '030206', 'fegatini di pollo': '030113',
                            'pancia di vitella': '030140', 'coniglio': '030185', 'roastbeef vitella': '030162',
                            'filetto suino': '030110', 'coscio agnello': '030103', 'fegato suino': '030169',
                            'paliata vit.': '030243', 'faraona': '030158', 'anatra': '030147', 'arista suino': '030166'}

        # TAB 1 per SURGELATI
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='SURGELATI', compound='left', image=self.img_btn1)

        # TAB 2 per FRESCHI
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='FRESCHI', compound='left', image=self.img_btn1)

        # TAB 3 per pasta fresca
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='PASTA FRESCA', compound='left', image=self.img_btn1)

        # TAB 4 per CARNE
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text='CARNE', compound='left', image=self.img_btn1)

        # LABEL ed ENTRY per inserimento EAN
        self.lbl_ean = ttk.Label(self.lblfr_ins_ean, text='EAN', width=20, anchor='center')
        self.ean = tk.StringVar()
        self.ean.set('')
        self.entry_ean = ttk.Entry(self.lblfr_ins_ean, textvariable=self.ean)

        self.lbl_pezzi = ttk.Label(self.lblfr_ins_ean, text='PEZZI', width=20, anchor='center')
        self.pezzi = tk.StringVar()
        self.pezzi.set('')
        self.entry_pezzi = ttk.Entry(self.lblfr_ins_ean, textvariable=self.pezzi)

        self.img_btn_focus_ean = tk.PhotoImage(file=".//immagini//modifica.gif")
        self.btn_focus_ean = ttk.Button(self.lblfr_ins_ean, image=self.img_btn_focus_ean, command=self.entry_ean.focus)

        self.img_btn_focus_pezzi = tk.PhotoImage(file=".//immagini//modifica.gif")
        self.btn_focus_pezzi = ttk.Button(self.lblfr_ins_ean, image=self.img_btn_focus_pezzi,
                                          command=self.entry_pezzi.focus)

        # BOTTONI per inserimento salvataggio e chiusura finestra
        self.btn_invio = tk.Button(self.frame_basso,
                                   text="Conferma",
                                   font=('Verdana', 15),
                                   width=20,
                                   command=self.invio)
        self.btn_salva = tk.Button(self.frame_basso,
                                   text='salva',
                                   font=('Verdana', 15),
                                   width=20,
                                   command=self.salva)
        self.btn_chiudi = tk.Button(self.frame_basso,
                                    text="Chiudi finestra",
                                    font=('Verdana', 15),
                                    width=20,
                                    command=self.destroy)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, sticky='ns')
        self.frame_dx.grid(row=0, column=1)
        self.frame_basso.grid(row=1, column=0, columnspan=2, sticky='we')

        self.lbl_settimana.grid(row=0, column=0, columnspan=2)

        self.label_data_utilizzo.grid(row=1, column=0)
        self.label_data.grid(row=1, column=1)

        self.tree.grid(row=3, column=0, pady=5)
        self.btn_elimina_riga.grid(row=3, column=1, sticky='n')

        self.lbl_peso.grid(row=4, column=0)
        self.entry_peso.grid(row=4, column=1)

        self.lblfr_ins_ean.grid(row=5, column=0, columnspan=2)
        self.lbl_ean.grid(row=1, column=0)
        self.entry_ean.grid(row=1, column=1)
        self.lbl_pezzi.grid(row=2, column=0)
        self.entry_pezzi.grid(row=2, column=1)
        self.btn_focus_ean.grid(row=1, column=2)
        self.btn_focus_pezzi.grid(row=2, column=2)

        self.notebook.grid(row=0, column=0)

        self.btn_invio.grid(row=3, column=0, padx=20, pady=17)
        self.btn_salva.grid(row=3, column=1, padx=20, pady=17)
        self.btn_chiudi.grid(row=3, column=2, padx=20, pady=17)

        self.entry_peso.focus()

        # cicli per creazione bottoni
        self.crea_bottoni_surgelati()
        self.crea_bottoni_freschi()
        self.crea_bottoni_pasta_fresca()
        self.crea_bottoni_carne()

    def crea_bottoni_surgelati(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_surgelati.items()):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab1, text=k.upper(), indicatoron=0, variable=self.value, font='Verdana', width=22,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def crea_bottoni_freschi(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_freschi.items()):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab2, text=k.upper(), indicatoron=0, variable=self.value, font='Verdana', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def crea_bottoni_pasta_fresca(self):
        lst_pasta_fresca = []
        self.c.execute("SELECT ingrediente_base FROM ingredienti_base WHERE merceologia LIKE '%Pasta Fresca'")

        for row in self.c:
            lst_pasta_fresca.extend(row)
        r, c = 1, 0
        for i in range(0, len(lst_pasta_fresca)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab4, text=lst_pasta_fresca[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_pasta_fresca[i]).grid(row=r, column=c)
            r += 1

    def crea_bottoni_carne(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_carne.items()):
            if r % 15 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab5, text=k.upper(), indicatoron=0, variable=self.value, font='Verdana', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def rimetti_focus(self, event):
        self.entry_peso.focus()

    def rimuovi_riga_selezionata(self):
            curitem = self.tree.selection()[0]
            self.tree.delete(curitem)

    def invio(self):
        if self.value.get() != '':
            self.c.execute("SELECT cod_ean FROM ingredienti_base WHERE ingrediente_base = %s ", (self.value.get(),))
            cod_ean = self.c.fetchone()
            self.tree.insert("", 0, values=(self.n_sett, self.value.get(), self.peso.get(), self.data, cod_ean))
            self.entry_peso.delete(0, tk.END)
            self.value.set('')
        elif self.ean.get() != '' and self.pezzi.get() != '':
            self.tree.insert("", 0, values=(self.n_sett, self.ean.get(), self.pezzi.get(), self.data, self.ean.get()))
            self.entry_pezzi.delete(0, tk.END)
            self.ean.set('')

    def salva(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        print(self.lista_da_salvare)
        self.c.executemany('INSERT INTO ingredienti VALUES (%s,%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.conn.close()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = Ingredienti()
    root.mainloop()
