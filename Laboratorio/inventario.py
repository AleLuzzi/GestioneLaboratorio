import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import mysql.connector
from config import get_config
from db import get_connection, close_connection
from tastiera_num import Tast_num
from theme import COLORS, get_font


class Inventario(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.configure(bg=COLORS["bg_light"])
        self.geometry("+25+25")
        self.title("Inventario")

        self.value = tk.StringVar()
        self.data = dt.date.today()
        self.config = get_config()
        self.dati_da_salvare = []

        # connessione database
        self.conn = get_connection()
        self.c = self.conn.cursor(buffered=True)

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        # Definizione Frame
        self.frame_sx = tk.Frame(self, bg=COLORS["bg_light"], padx=8, pady=8)
        self.frame_dx = tk.Frame(self, bg=COLORS["bg_light"], padx=8, pady=8)

        self.notebook = ttk.Notebook(self.frame_dx)

        # TREEVIEW riepilogo inventario
        self.tree_riepilogo = ttk.Treeview(self.frame_sx, height=18)

        self.tree_riepilogo['columns'] = (
            'Data', 'IDTaglio', 'Taglio', 'IDMerc', 'Merceologia', 'Peso')
        self.tree_riepilogo['displaycolumns'] = (
            'Taglio', 'Merceologia', 'Peso')
        self.tree_riepilogo['show'] = 'headings'
        self.tree_riepilogo.heading('Taglio', text="Taglio")
        self.tree_riepilogo.heading('Merceologia', text='Merceologia')
        self.tree_riepilogo.heading('Peso', text="Peso")

        self.tree_riepilogo.column("Peso", width=80)

        # LABEL che mostra il numero della settimana
        self.lbl_settimana = ttk.Label(self.frame_dx, text='Settimana n. ',
                                       font=get_font(12, bold=True))
        self.lbl_nr_settimana = tk.Label(
            self.frame_dx, text=str(1 + int(self.data.strftime('%W'))),
            font=get_font(12), bg=COLORS["bg_content"], fg=COLORS["text_dark"], padx=12, pady=4)

        # BUTTON elimina riga
        self.btn_rimuovi_riga = ttk.Button(self.frame_sx, text="Rimuovi riga",
                                           command=self.rimuovi_riga_selezionata)

        # ENTRY peso inserito
        self.peso = tk.StringVar()
        self.ent_peso = ttk.Entry(self.frame_sx, textvariable=self.peso, width=12)

        self.img_btn_focus_ean = tk.PhotoImage(
            file=".//immagini//modifica.gif")

        self.btn_focus_ean = ttk.Button(
            self.frame_sx,
            image=self.img_btn_focus_ean,
            command=self._ins_peso_da_tastiera)

        # BUTTON inserimento peso
        self.btn_inserisci_peso = ttk.Button(self.frame_sx, text='Inserisci peso', command=self.ins_peso)

        # BUTTON salva dati
        self.btn_salva_dati = ttk.Button(self.frame_dx, text='Salva dati', command=self._salva_esci)

        # BUTTON chiudi finestra
        self.btn_chiudi = ttk.Button(self.frame_dx, text='Chiudi finestra', command=self.destroy)

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
        self.notebook.add(self.tab1, text='AGNELLO',
                          compound='left', image=self.img_btn1)

        lst_agnello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 12")
        for row in self.c:
            lst_agnello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_agnello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab1,
                text=lst_agnello[i].upper(),
                indicatoron=0,
                variable=self.value,
                font='Verdana',
                width=20,
                value=lst_agnello[i]).grid(row=r, column=c)
            r += 1

        # TAB 2 BOVINO
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='BOVINO',
                          compound='left', image=self.img_btn1)

        lst_bovino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 10")
        for row in self.c:
            lst_bovino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_bovino)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab2,
                text=lst_bovino[i].upper(),
                indicatoron=0,
                variable=self.value,
                font='Verdana',
                width=20,
                value=lst_bovino[i]).grid(row=r, column=c)
            r += 1

        # TAB 3 SUINO
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='SUINO',
                          compound='left', image=self.img_btn1)

        lst_suino = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 11")
        for row in self.c:
            lst_suino.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_suino)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab3,
                text=lst_suino[i].upper(),
                indicatoron=0,
                variable=self.value,
                font='Verdana',
                width=20,
                value=lst_suino[i]).grid(row=r, column=c)
            r += 1

        # TAB 4 VITELLO
        self.tab4 = tk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='VITELLO',
                          compound='left', image=self.img_btn1)

        lst_vitello = []
        self.c.execute("SELECT taglio FROM tagli WHERE Id_Merceologia = 13")
        for row in self.c:
            lst_vitello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_vitello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(
                self.tab4,
                text=lst_vitello[i].upper(),
                indicatoron=0,
                variable=self.value,
                font='Verdana',
                width=20,
                value=lst_vitello[i]).grid(row=r, column=c)
            r += 1

    def _ins_peso_da_tastiera(self):
        peso = Tast_num(self)
        val = peso.value.get()
        self.peso.set(val)

    def rimuovi_riga_selezionata(self):
        curitem = self.tree_riepilogo.selection()[0]
        self.tree_riepilogo.delete(curitem)

    def ins_peso(self):
        if self.value.get() != '' and self.peso.get() != '':
            data = self.data
            taglio = self.value.get()
            cat_merc = self.notebook.tab(self.notebook.select(), "text")
            self.c.execute(
                "SELECT Id FROM merceologie WHERE merceologia = %s",
                (cat_merc,))
            id_merc = self.c.fetchone()
            self.c.execute("SELECT Id FROM tagli WHERE taglio = %s", (taglio,))
            id_taglio = self.c.fetchone()
            self.tree_riepilogo.insert(
                '',
                'end',
                values=(
                    data,
                    id_taglio[0],
                    taglio,
                    id_merc[0],
                    cat_merc,
                    self.peso.get()))
            self.ent_peso.delete(0, tk.END)
        else:
            messagebox.showinfo('ATTENZIONE', 'dati mancanti.. controlla!!!')

    def _prepara_dati(self):
        res = []
        for items in self.tree_riepilogo.get_children():
            dati = [self.tree_riepilogo.item(items)['values'][0],
                    self.tree_riepilogo.item(items)['values'][1],
                    self.tree_riepilogo.item(items)['values'][3],
                    self.tree_riepilogo.item(items)['values'][5]]
            res.append(dati)
        return res

    def _salva_esci(self):
        dati_da_salvare = self._prepara_dati()
        sql = 'INSERT INTO inventari(data_rilevazione,prodID,mercID,peso_rilevato) VALUES (%s,%s,%s,%s)'
        self.c.executemany(sql, dati_da_salvare)
        self.conn.commit()
        self.conn.close()
        self.destroy()

    def destroy(self):
        close_connection(getattr(self, "conn", None))
        tk.Toplevel.destroy(self)


if __name__ == '__main__':
    root = tk.Tk()
    new = Inventario()
    root.mainloop()
