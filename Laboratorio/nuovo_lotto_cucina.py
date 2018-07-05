import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector
from tkinter import messagebox


class NuovoLottoCucina(tk.Toplevel):
    def __init__(self):
        super(NuovoLottoCucina, self).__init__()
        self.title("Nuovo Lotto Cucina")
        self.geometry("+0+0")

        self.data = dt.date.today().strftime('%d%m%y')

        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        self.nuova_produzione = tk.StringVar()
        self.peso_da_inserire = tk.StringVar()
        self.prog_lotto_ven = self.data
        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")
        self.value = tk.StringVar()

        # DISPOSIZIONE FRAME
        self.frame_alto = tk.Frame(self, bd='3', relief='groove')
        self.frame_centro = tk.Frame(self, height=450, width=self.winfo_screenwidth(),
                                     bd='3', relief='groove')
        self.frame_basso = tk.Frame(self, bd='3', background='white', relief='groove')

        self.frame_centro.grid_propagate(False)
        self.frame_centro.grid_rowconfigure(0, weight=2)
        self.frame_centro.grid_columnconfigure(0, weight=2)

        # TREEVIEW per riepilogo immissioni
        self.tree = ttk.Treeview(self.frame_centro, height=15)
        self.tree['columns'] = ('prog_v', 'prodotto', 'peso')

        self.tree['displaycolumns'] = ('prodotto', 'peso')
        self.tree['show'] = 'headings'

        self.tree.column("prodotto", width=180)
        self.tree.column("peso", width=80)

        self.tree.heading("prodotto", text="prodotto")
        self.tree.heading("peso", text="peso")

        self.tree.tag_configure('odd', background='light green')

        # LABEL nuovo lotto vendita
        self.lbl_nuovo_lotto = ttk.Label(self.frame_alto, text='NUOVO LOTTO VENDITA', font=('Helvetica', 20))
        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_alto, text=str(self.prog_lotto_ven),
                                                font=('Helvetica', 40))

        # LABELFRAME nuova produzione
        self.labelframe = ttk.Labelframe(self.frame_centro, text="Nuova Produzione")

        # NOTEBOOK e posizione
        self.notebook = ttk.Notebook(self.labelframe)

        # TAB 1 per PRIMI PIATTI
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Primi', compound='left', image=self.img_btn1)

        self.lista_primi = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'Primi piatti'")

        for row in self.c:
            self.lista_primi.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_primi)):
            if row % 10 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab1,
                           text=str(self.lista_primi[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_primi[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 2 per PRIMI pesce
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Primi Pesce', compound='left', image=self.img_btn1)

        self.lista_primi_pesce = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'Primi piatti di pesce'")

        for row in self.c:
            self.lista_primi_pesce.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_primi_pesce)):
            if row % 10 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab2,
                           text=str(self.lista_primi_pesce[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_primi_pesce[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 3 per SECONDI
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Secondi', compound='left', image=self.img_btn1)

        self.lista_secondi = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'secondi piatti'")

        for row in self.c:
            self.lista_secondi.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_secondi)):
            if row % 13 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab3,
                           text=str(self.lista_secondi[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_secondi[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 4 per SECONDI pesce
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='Secondi Pesce', compound='left', image=self.img_btn1)

        self.lista_secondi_pesce = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = '5'")

        for row in self.c:
            self.lista_secondi_pesce.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_secondi_pesce)):
            if row % 13 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab4,
                           text=str(self.lista_secondi_pesce[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_secondi_pesce[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 5 per CONTORNI
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text='Contorni', compound='left', image=self.img_btn1)

        self.lista_contorni = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'contorni'")

        for row in self.c:
            self.lista_contorni.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_contorni)):
            if row % 10 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab5,
                           text=str(self.lista_contorni[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_contorni[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 6 per DOLCI
        self.tab6 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab6, text='Dolci', compound='left', image=self.img_btn1)

        self.lista_dolci = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'dolci'")

        for row in self.c:
            self.lista_dolci.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_dolci)):
            if row % 10 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab6,
                           text=str(self.lista_dolci[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_dolci[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # TAB 7 per PIATTI freddi
        self.tab7 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab7, text='Piatti freddi', compound='left', image=self.img_btn1)

        self.lista_piatti_freddi = []
        self.c.execute("SELECT prodotto FROM prodotti WHERE merceologia = 'piatti freddi'")

        for row in self.c:
            self.lista_piatti_freddi.extend(row)

        row, col = 1, 0
        for i in range(0, len(self.lista_piatti_freddi)):
            if row % 10 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.tab7,
                           text=str(self.lista_piatti_freddi[i]),
                           variable=self.value,
                           width=25,
                           indicatoron=0,
                           value=self.lista_piatti_freddi[i],
                           font='Verdana').grid(row=row, column=col, sticky='w')
            row += 1

        # LABELFRAME per peso da inserire e bottoni
        self.lblframe_peso = ttk.LabelFrame(self.frame_basso, text='Peso')

        # ENTRY per inserimento del peso
        self.entry_peso = ttk.Entry(self.lblframe_peso,
                                    font=('Helvetica', 20),
                                    textvariable=self.peso_da_inserire)
        self.entry_peso.focus()

        # BOTTONE ESCI E SALVA
        self.btn_invia = tk.Button(self.frame_basso,
                                   text="Invio",
                                   font=('Helvetica', 20),
                                   command=self.invia)
        self.btn_esci = tk.Button(self.frame_basso,
                                  text="Chiudi finestra",
                                  font=('Helvetica', 20),
                                  command=self.esci_senza_salvare)
        self.btn_esci_salva = tk.Button(self.frame_basso,
                                        text="Esci e salva",
                                        font=('Helvetica', 20),
                                        command=self.esci_salva)
        self.btn_elimina_riga = tk.Button(self.frame_centro, text='Elimina riga', command=self.rimuovi_riga_selezionata)

        # LAYOUT
        self.frame_alto.grid(row=0, column=0, padx=10, sticky='n')
        self.frame_centro.grid(row=1, column=0, sticky='ns')
        self.frame_basso.grid(row=2, column=0, columnspan=3, sticky='we')

        self.tree.grid(row=0, column=1)
        self.btn_elimina_riga.grid(row=1, column=1, sticky='we')

        self.labelframe.grid(row=0, column=0, rowspan=2)
        self.notebook.grid(row=0, column=0)

        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.lbl_prog_lotto_vendita.grid(row=1, column=0)

        self.lblframe_peso.grid(row=0, column=0, sticky='w')
        self.entry_peso.grid()

        self.btn_invia.grid(row=0, column=1, padx=10, pady=20)
        self.btn_esci.grid(row=0, column=2, padx=10, pady=20)
        self.btn_esci_salva.grid(row=0, column=3, padx=10, pady=20)

        # self.crea_articoli_nuova_produzione()

    def rimuovi_riga_selezionata(self):
            curitem = self.tree.selection()[0]
            self.tree.delete(curitem)

    def invia(self, giorno=dt.date.today()):
        self.tree.insert('', 'end', values=('L' + (str(self.prog_lotto_ven)),
                                            self.value.get(),
                                            self.peso_da_inserire.get(),
                                            giorno))
        self.entry_peso.delete(0, tk.END)

    def esci_senza_salvare(self):
        if bool(self.tree.get_children()):
            messagebox.showinfo('Attenzione', 'Ci sono dati inseriti non salvati')
        else:
            self.destroy()

    def esci_salva(self):
        for child in self.tree.get_children():
            self.lista_da_salvare.append(self.tree.item(child)['values'])
        print(self.lista_da_salvare)
        self.c.executemany('INSERT INTO lotti_vendita_cucina VALUES (%s,%s,%s,%s)', self.lista_da_salvare)
        self.conn.commit()
        self.conn.close()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLottoCucina()
    root.mainloop()
