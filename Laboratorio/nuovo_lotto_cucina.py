import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector


class NuovoLottoCucina(tk.Toplevel):
    def __init__(self):
        super(NuovoLottoCucina, self).__init__()
        self.title("Nuovo Lotto Cucina")
        self.geometry("1024x525+0+0")

        self.data = dt.date.today()

        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.lista_da_salvare = []
        self.lista_nuova_produzione = []
        # self.prog_lotto_ven = ''
        self.nuova_produzione = tk.StringVar()
        self.peso_da_inserire = tk.StringVar()

        self.genera_progressivo()

        # DISPOSIZIONE FRAME
        self.frame_sx = tk.Frame(self, bd='3', relief='groove')
        self.frame_dx = tk.Frame(self, bd='3', relief='groove')
        self.frame_basso = tk.Frame(self, bd='3', background='white', relief='groove')

        # TREEVIEW per riepilogo immissioni
        self.tree = ttk.Treeview(self.frame_dx, height=5)
        self.tree['columns'] = ('prodotto', 'peso')

        self.tree['show'] = 'headings'

        self.tree.column("prodotto", width=120)
        self.tree.column("peso", width=80)

        self.tree.heading("prodotto", text="prodotto")
        self.tree.heading("peso", text="peso")

        self.tree.tag_configure('odd', background='light green')

        # LABEL nuovo lotto vendita
        self.lbl_nuovo_lotto = ttk.Label(self.frame_dx, text='NUOVO LOTTO VENDITA', font=('Helvetica', 20))
        self.lbl_prog_lotto_vendita = ttk.Label(self.frame_dx, text=str(self.prog_lotto_ven) + 'V',
                                                font=('Helvetica', 40))

        # LABELFRAME nuova produzione
        self.labelframe = ttk.Labelframe(self.frame_sx, text="Nuova Produzione")

        self.c.execute("SELECT prodotto FROM prodotti WHERE flag1_prod = 1 ")
        for row in self.c:
            self.lista_nuova_produzione.extend(row)

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
                                  command=self.destroy)
        self.btn_esci_salva = tk.Button(self.frame_basso,
                                        text="Esci e salva",
                                        font=('Helvetica', 20),
                                        command=self.esci_salva)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, padx=10, sticky='n')
        self.frame_dx.grid(row=0, column=1, sticky='ns')
        self.frame_basso.grid(row=1, column=0, columnspan=3, sticky='we')

        self.tree.grid(row=3, column=0, sticky='we')

        self.labelframe.grid(row=2, column=0)
        self.lbl_nuovo_lotto.grid(row=0, column=0)
        self.lbl_prog_lotto_vendita.grid(row=1, column=0)

        self.lblframe_peso.grid(row=0, column=0, sticky='w')
        self.entry_peso.grid()

        self.btn_invia.grid(row=0, column=1, padx=10, pady=20)
        self.btn_esci.grid(row=0, column=2, padx=10, pady=20)
        self.btn_esci_salva.grid(row=0, column=3, padx=10, pady=20)

        self.crea_articoli_nuova_produzione()

    def crea_articoli_nuova_produzione(self):
        row, col = 1, 0
        for i in range(0, len(self.lista_nuova_produzione)):
            if row % 8 == 0:
                col += 1
                row = 1
            tk.Radiobutton(self.labelframe,
                           text=str(self.lista_nuova_produzione[i]).upper(),
                           variable=self.nuova_produzione,
                           width=25,
                           indicatoron=0,
                           value=self.lista_nuova_produzione[i],
                           font='Helvetica').grid(row=row, column=col, sticky="w", pady=2)
            row += 1

    def genera_progressivo(self):
        self.c.execute("SELECT prog_ven FROM progressivi")
        self.prog_lotto_ven = self.c.fetchone()[0]

    def invia(self):
        if (self.nuova_produzione.get() != '') and (self.peso_da_inserire.get() != ''):
            self.tree.insert('', 'end', values=(self.nuova_produzione.get(), self.peso_da_inserire.get()))
            self.lista_da_salvare.append(((str(self.prog_lotto_ven) + 'V'), self.data, '0', self.nuova_produzione.get(),
                                         self.peso_da_inserire.get(), '0'))

    def esci_salva(self):
        if (self.nuova_produzione.get() != '') \
                and (self.peso_da_inserire.get() != '') \
                and (self.lista_da_salvare != []):
            self.c.executemany('INSERT INTO lotti_vendita VALUES (%s,%s,%s,%s,%s,%s)', self.lista_da_salvare)
            self.conn.commit()
            self.c.execute('UPDATE progressivi SET prog_ven = %s', (self.prog_lotto_ven + 1,))
            self.conn.commit()
            self.conn.close()
            self.destroy()
        else:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    new = NuovoLottoCucina()
    root.mainloop()
