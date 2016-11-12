import tkinter as tk
from tkinter import ttk
# from time import strftime
import datetime
import sqlite3


class Ingredienti(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Ingredienti")
        self.geometry("%dx525+0+0" % self.winfo_screenwidth())

        self.lista_da_salvare = []
        self.value = tk.StringVar()
        self.peso = tk.StringVar()
        self.peso.set('')
        self.img_btn1 = tk.PhotoImage(file="..//Laboratorio//immagini//logo_piccolo.gif")
        '''
        Connessione al database
        '''

        '''
        Definizione Frame
        '''
        self.frame_sx = tk.Frame(self, bd=3, relief='groove')
        self.frame_dx = tk.Frame(self, bd=3, relief='groove')
        self.frame_basso = tk.Frame(self, background='white')
        self.frame_sx.grid(row=0, column=0, sticky='ns')
        self.frame_dx.grid(row=0, column=1)
        self.frame_basso.grid(row=1, column=0, columnspan=2, sticky='we')
        '''
        Treeview per riepilogo ingredienti inseriti
        '''
        self.tree = ttk.Treeview(self.frame_sx)
        self.tree['columns'] = 'quantita'
        self.tree.column("quantita", width=100)
        self.tree.heading("quantita", text="quantita")
        self.tree.grid(row=3, column=0, columnspan=2)
        '''
        Label che mostra il numero della settimana
        '''
        self.data = datetime.date.today()
        self.n_sett = str(1 + int(self.data.strftime('%W')))
        self.lbl_settimana = ttk.Label(self.frame_sx, text='SETTIMANA NUMERO ' + self.n_sett,
                                       foreground='blue', font=('Helvetica', 20))
        self.label_data_utilizzo = ttk.Label(self.frame_sx,
                                             text="Data Utilizzo Merce", foreground='blue', font=('Helvetica', 20))
        self.label_data = ttk.Label(self.frame_sx, anchor='center',
                                    text=self.data.strftime('%d/%m/%y'), font=('Helvetica', 20))
        self.lbl_settimana.grid(row=0, column=0, columnspan=2)
        self.label_data_utilizzo.grid(row=1, column=0)
        self.label_data.grid(row=1, column=1)
        '''
        Notebook e posizione
        '''
        self.notebook = ttk.Notebook(self.frame_dx)
        self.notebook.grid(row=0, column=0)
        '''
        Definizione dizionari per ingredienti
        '''
        self.lista_surgelati = {'spinaci': '1950', 'cicoria': '1973', 'seppia': '2033', 'baccala': '2038',
                                'pangasio': '2025', 'frittura pesce': '1984', 'spiedini pesce': '2024',
                                'carciofi': '2012', 'fil.gallinella': '2052', 'gamberi 50-60': '1992',
                                'fagiolini': '1919', 'melanzane grigliate': '2016', 'lasagna sfoglia': '2000',
                                'filetto orata': '2028', 'orata': '2045', 'halibut': '2050',
                                'minestrone di verdure': '1955'}
        self.lista_freschi = {'pecorino romano': '010082', 'mozzarella': '010325', 'grana padano': '010080',
                              'prosc.cotto': '010332', 'ricotta mista': '010020', 'uova': 'uova medie sciolte'}
        self.lista_pasta_fresca = {'gnocchi': '010031', 'ciriole': '010032', 'fettuccine': '010034'}
        self.lista_carne = {'pollo ruspante': '030115', 'cosce pollo': '030182', 'piccioni': '030207',
                            'petto tacchino': '030135', 'magro suino': '030121', 'pancia suino': '030111',
                            'salsicce fresche': '030130', 'macinato magro': '030119', 'spalla agnello': '030104',
                            'carne x gnocchi': '030139', 'cotolette agnello': '030105', 'trippa bovino': '030192',
                            'coratella agnello': '030106', 'magro vitella': '030163', 'petto pollo': '030114',
                            'macinato x polpette': '030206', 'fegatini di pollo': '030113',
                            'pancia di vitella': '030140', 'coniglio': '030185', 'roastbeef vitella': '030162',
                            'filetto suino': '030110', 'coscio agnello': '030103', 'fegato suino': '030169',
                            'paliata vit.': '030243', 'faraona': '030158', 'anatra': '030147', 'arista suino': '030166'}
        '''
        TAB 1 per SURGELATI
        '''
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='SURGELATI', compound='left', image=self.img_btn1)
        '''
        ciclo per creazione bottoni surgelati
        '''
        self.crea_bottoni_surgelati()

        ttk.Separator(self.tab1, orient='vertical').grid(row='1', column='2', rowspan=8, sticky='ns', padx=5)

        self.lbl_peso_s = ttk.Label(self.tab1, text='PESO', width=20, anchor='center')
        self.lbl_peso_s.grid(row='1', column='3', columnspan='2')

        self.entry_peso_s = ttk.Entry(self.tab1, textvariable=self.peso)
        self.entry_peso_s.focus()
        self.entry_peso_s.grid(row='2', column='4', columnspan='2', sticky='we')
        '''
        TAB 2 per FRESCHI
        '''
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='FRESCHI', compound='left', image=self.img_btn1)
        '''
        ciclo per creazione bottoni freschi
        '''
        self.crea_bottoni_freschi()

        ttk.Separator(self.tab2, orient='vertical').grid(row='1', column='1', rowspan=5, sticky='ns', padx=5)

        self.lbl_peso_f = ttk.Label(self.tab2, text='PESO', width=20, anchor='center')
        self.lbl_peso_f.grid(row='1', column='2', columnspan='2')

        self.entry_peso_f = ttk.Entry(self.tab2, textvariable=self.peso)
        self.entry_peso_f.focus()
        self.entry_peso_f.grid(row='2', column='2', columnspan='2', sticky='we')
        '''
        TAB 3 per codice EAN
        '''
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='CODICE EAN', compound='left', image=self.img_btn1)

        self.lbl_ean = ttk.Label(self.tab3, text='EAN', width=20, anchor='center')
        self.lbl_ean.grid(row='1', column='0')

        self.ean = tk.StringVar()
        self.ean.set('')
        self.entry_ean = ttk.Entry(self.tab3, textvariable=self.ean)
        self.entry_ean.grid(row='2', column='0')

        self.lbl_pezzi = ttk.Label(self.tab3, text='PEZZI', width=20, anchor='center')
        self.lbl_pezzi.grid(row='3', column='0')

        self.pezzi = tk.StringVar()
        self.pezzi.set('')
        self.entry_pezzi = ttk.Entry(self.tab3, textvariable=self.pezzi)
        self.entry_pezzi.grid(row='4', column='0')

        self.img_btn_focus_ean = tk.PhotoImage(file="..//Laboratorio//immagini//modifica.gif")
        self.btn_focus_ean = ttk.Button(self.tab3, image=self.img_btn_focus_ean, command=self.entry_ean.focus)
        self.btn_focus_ean.grid(row=2, column=1, padx=10)

        self.img_btn_focus_pezzi = tk.PhotoImage(file="..//Laboratorio//immagini//modifica.gif")
        self.btn_focus_pezzi = ttk.Button(self.tab3, image=self.img_btn_focus_pezzi, command=self.entry_pezzi.focus)
        self.btn_focus_pezzi.grid(row=4, column=1, padx=10)
        '''
        TAB 4 per pasta fresca
        '''
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='PASTA FRESCA', compound='left', image=self.img_btn1)
        '''
        ciclo per creazione bottoni pasta fresca
        '''
        self.crea_bottoni_pasta_fresca()

        self.lbl_peso_pf = ttk.Label(self.tab4, text='PESO', width=20, anchor='center')
        self.lbl_peso_pf.grid(row='1', column='2', columnspan='2')

        self.entry_peso_pf = ttk.Entry(self.tab4, textvariable=self.peso)
        self.entry_peso_pf.focus()
        self.entry_peso_pf.grid(row='2', column='2', columnspan='2', sticky='we')
        '''
        TAB 5 per CARNE
        '''
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text='CARNE', compound='left', image=self.img_btn1)
        '''
        ciclo per creazione bottoni carne
        '''
        self.crea_bottoni_carne()

        self.lbl_peso_c = ttk.Label(self.tab5, text='PESO', width=20, anchor='center')
        self.lbl_peso_c.grid(row='1', column='3', columnspan='2')

        self.entry_peso_c = ttk.Entry(self.tab5, textvariable=self.peso)
        self.entry_peso_c.focus()
        self.entry_peso_c.grid(row='2', column='3', columnspan='2', sticky='we')
        '''
        BOTTONI per inserimento salvataggio e chiusura finestra
        '''
        self.btn_invio = ttk.Button(self.frame_basso, text="Conferma", command=self.invio)
        self.btn_salva = ttk.Button(self.frame_basso, text='salva', command=self.salva)
        self.btn_chiudi = ttk.Button(self.frame_basso, text="Chiudi finestra", command=self.destroy)
        self.btn_invio.grid(row='3', column='0', padx=20, pady=20)
        self.btn_salva.grid(row='3', column='1', padx=20, pady=20)
        self.btn_chiudi.grid(row='3', column='2', padx=20, pady=20)

    def crea_bottoni_surgelati(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_surgelati.items()):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab1, text=k.upper(), indicatoron=0, variable=self.value, font='Helvetica', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def crea_bottoni_freschi(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_freschi.items()):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab2, text=k.upper(), indicatoron=0, variable=self.value, font='Helvetica', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def crea_bottoni_pasta_fresca(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_pasta_fresca.items()):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab4, text=k.upper(), indicatoron=0, variable=self.value, font='Helvetica', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def crea_bottoni_carne(self):
        r, c = 1, 0
        for k, v in sorted(self.lista_carne.items()):
            if r % 12 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab5, text=k.upper(), indicatoron=0, variable=self.value, font='Helvetica', width=20,
                           value=k + ' cod.' + v).grid(row=r, column=c)
            r += 1

    def invio(self):
        if self.value.get() != '':
            self.tree.insert("", 0, text=self.value.get(), values=(self.peso.get()))
            self.lista_da_salvare.append((self.n_sett, (self.value.get()), (self.peso.get()), self.data))
            self.entry_peso_s.delete(0, tk.END)
            self.value.set('')
        elif self.ean.get() != '':
            self.tree.insert("", 0, text=self.ean.get(), values=(self.pezzi.get()))
            self.lista_da_salvare.append((self.n_sett, (self.ean.get()), (self.pezzi.get()), self.data))
            self.entry_pezzi.delete(0, tk.END)
            self.ean.set('')

    def salva(self):
        conn = sqlite3.connect('../Laboratorio/data.db',
                               detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        c.executemany('INSERT INTO ingredienti VALUES (?,?,?,?)', self.lista_da_salvare)
        conn.commit()
        conn.close()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = Ingredienti()
    root.mainloop()
