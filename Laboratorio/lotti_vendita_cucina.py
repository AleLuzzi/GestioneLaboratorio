import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import mysql.connector
import shutil
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Spacer,
                                Table, TableStyle, Paragraph)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import win32api
from tkinter import messagebox

class LottiInVenditaCucina(tk.Toplevel):
    def __init__(self):
        super(LottiInVenditaCucina, self).__init__()
        self.geometry("1024x525+0+0")
        self.title('Lotti in vendita Cucina')

        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.data = dt.date.today()

        # Disposizione Frame e LabelFrame
        self.frame_sx = tk.Frame(self)
        self.frame_dx = tk.Frame(self)
        self.frame_dx_basso = tk.Frame(self, background='white')

        # Treeview con lotti disponibili
        self.tree = ttk.Treeview(self.frame_sx, height=23)
        self.tree['columns'] = ('peso')

        self.tree.heading('peso', text="peso")

        self.tree.column("peso", width=80)

        self.tree.tag_configure('odd', background='light green')

        # LAYOUT
        self.frame_sx.grid(row=0, column=0, rowspan=2)
        self.frame_dx.grid(row=0, column=1)
        self.frame_dx_basso.grid(row=1, column=1)

        self.tree.grid(row=1, column=0)

        self.riempi_tutti()

    def riempi_tutti(self):
        self.tree.delete(*self.tree.get_children())

        self.c.execute("SELECT DISTINCT progressivo_ven_c,prodotto,quantita "
                       "FROM lotti_vendita_cucina "
                       "ORDER BY progressivo_ven_c DESC")
        for lista in self.c:
            print (lista)
            try:
                self.tree.insert('', 'end', lista[0], text=lista[0], tags=('odd',))
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(lista[2]))
                self.tree.item(lista[0], open='true')
            except:
                self.tree.insert(lista[0], 'end', text=lista[1],
                                 values=(lista[2]))
                self.tree.item(lista[0], open='true')

if __name__ == "__main__":
    root = tk.Tk()
    new = LottiInVenditaCucina()
    root.mainloop()
