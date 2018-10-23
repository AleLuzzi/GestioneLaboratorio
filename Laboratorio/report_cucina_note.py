import tkinter as tk
from tkinter import ttk
from time import strftime
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
import mysql.connector
# import os
from tkinter import messagebox
import win32api


class ReportCucina(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Connessione al database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        # Treeview per merce ingresso
        self.tree_ingresso = ttk.Treeview(self, height=20)
        self.tree_ingresso['columns'] = ('Prodotto', 'Quantita', 'cod_ean')
        self.tree_ingresso['show'] = 'headings'
        self.tree_ingresso.heading('Prodotto', text="Prodotto")
        self.tree_ingresso.heading('Quantita', text="Quantita")
        self.tree_ingresso.heading('cod_ean', text="Cod EAN")

        self.tree_ingresso.column("Prodotto", width=200)
        self.tree_ingresso.column("Quantita", width=100)
        self.tree_ingresso.column("cod_ean", width=100)

        # Treeview per merce in uscita
        self.tree_uscita = ttk.Treeview(self, height=20)
        self.tree_uscita['columns'] = ('Prodotto', 'Quantita')
        self.tree_uscita['show'] = 'headings'
        self.tree_uscita.heading('Prodotto', text="Prodotto")
        self.tree_uscita.heading('Quantita', text="Quantita")

        self.tree_uscita.column("Prodotto", width=200)
        self.tree_uscita.column("Quantita", width=100)

        # Labelframe per contenere i bottoni
        self.lblFrame_azioni = ttk.Labelframe(self, text='Azioni')

        # Label che indica la settimana
        n_sett = str(1 + int(strftime('%W')))
        anno = strftime('%Y')
        self.lbl_settimana = ttk.Label(self.lblFrame_azioni, text='SETTIMANA NUMERO ' + n_sett + ' '
                                       + anno, font='Helvetica')

        # Bottone per popolare il treeview
        self.btn = ttk.Button(self.lblFrame_azioni, text='Inserisci dati', command=self.inserisci)

        # Entry per scegliere la settimana
        self.lbl_scelta_sett = ttk.Label(self.lblFrame_azioni, text='Settimana da visualizzare ')
        self.settimana = tk.StringVar()
        self.settimana.set('')
        self.entry_settimana_s = ttk.Entry(self.lblFrame_azioni, textvariable=self.settimana)
        self.entry_settimana_s.focus()

        # Bottone per generare la stampa del pdf
        self.stampa = ttk.Button(self.lblFrame_azioni, text="Crea PDF", command=self.crea_pdf)

        # LAYOUT
        self.tree_ingresso.grid(row=0, column=0)
        self.tree_uscita.grid(row=0, column=1)
        self.lblFrame_azioni.grid(row=0, column=2, sticky='n')
        self.lbl_settimana.grid()
        self.lbl_scelta_sett.grid()
        self.btn.grid()
        self.entry_settimana_s.grid()
        self.stampa.grid()

    def inserisci(self, anno=strftime('%Y')):

        self.tree_ingresso.delete(*self.tree_ingresso.get_children())
        self.tree_uscita.delete(*self.tree_uscita.get_children())

        self.c.execute('SELECT prodotto,SUM(quantita),cod_ean '
                       'FROM ingredienti '
                       'WHERE settimana = %s '
                       'AND ingredienti.data_utilizzo>%s '
                       'GROUP BY prodotto',
                       (self.settimana.get(),anno),)
        for row in self.c:
            self.tree_ingresso.insert("", 'end', values=(row[0], row[1], row[2]))

        self.c.execute('SELECT prodotto, quantita '
                       'FROM lotti_vendita_cucina '
                       'WHERE settimana = %s '
                       'GROUP BY prodotto ',
                       (self.settimana.get(),))

        for row in self.c:
            self.tree_uscita.insert("", 'end', values=(row[0], row[1]))

    def crea_pdf(self):
        data = [('settimana', 'codice', 'prodotto', 'cod_ean')]

        self.c.execute("SELECT settimana,prodotto,SUM(quantita),cod_ean "
                       "FROM ingredienti "
                       "WHERE settimana = %s "
                       "GROUP BY prodotto",
                       (self.settimana.get(),))
        for i in self.c:
            data.append(i)

        doc = SimpleDocTemplate("./table.pdf", pagesize=A4)

        parts = []
        table_with_style = Table(data, [1 * inch, 1.7 * inch, inch])
        table_with_style.hAlign = "LEFT"

        table_with_style.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, 0), 0.25, colors.green),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))

        parts.append(Spacer(1, 0.5 * inch))
        parts.append(table_with_style)
        doc.build(parts)
        if messagebox.askyesno('STAMPA', 'Vuoi stampare il pdf?'):
            win32api.ShellExecute(None, "print", "table.pdf", None, ".", 0)


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = ReportCucina(notebook)
    notebook.add(new, text='Report cucina')
    root.mainloop()
