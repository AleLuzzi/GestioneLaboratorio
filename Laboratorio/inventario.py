import tkinter as tk
from tkinter import ttk
import datetime as dt
import mysql.connector


class Inventario(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Inventario")

        self.value = tk.StringVar()

        self.data = dt.date.today()

        # connessione database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        # Definizione Frame
        self.frame_sx = tk.Frame(self)
        self.frame_alto = tk.Frame(self, bd='3', relief='groove')
        self.frame_dx = tk.Frame(self)

        self.notebook = ttk.Notebook(self.frame_dx)

        # TREEVIEW riepilogo inventario
        self.tree_riepilogo = ttk.Treeview(self.frame_sx, height=20)

        self.tree_riepilogo['columns'] = ('Taglio', 'Peso')
        self.tree_riepilogo['show'] = 'headings'
        self.tree_riepilogo.heading('Taglio', text="Taglio")
        self.tree_riepilogo.heading('Peso', text="Peso")

        self.tree_riepilogo.column("Peso", width=80)

        # LABEL che mostra il numero della settimana
        self.lbl_settimana = tk.Label(self.frame_alto, text='SETTIMANA NUMERO ',
                                      foreground='blue', font=('Verdana', 20), relief='ridge', padx=20)
        self.lbl_nr_settimana = tk.Label(self.frame_alto, text=str(1 + int(self.data.strftime('%W'))),
                                         font=('Verdana', 20), bg='white', relief='sunken', padx=20)

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, rowspan=2)
        self.frame_alto.grid(row=0, column=1)
        self.frame_dx.grid(row=1, column=1, sticky='n')

        self.tree_riepilogo.grid()
        self.lbl_settimana.grid(row=0, column=1)
        self.lbl_nr_settimana.grid(row=0, column=2)
        self.notebook.grid()

        # TAB 1 AGNELLO
        self.tab1 = ttk.Frame(self.notebook)
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
        self.tab2 = ttk.Frame(self.notebook)
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
        self.tab3 = ttk.Frame(self.notebook)
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
        self.tab4 = ttk.Frame(self.notebook)
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


if __name__ == '__main__':
    root = tk.Tk()
    new = Inventario()
    root.mainloop()
