import tkinter as tk
from tkinter import ttk
from time import strftime
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
import sqlite3
import os


class ReportCucina(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        '''
        Connessione al database
        '''
        self.conn = sqlite3.connect(os.path.join('..', 'laboratorio', 'data.db'))
        self.c = self.conn.cursor()
        '''
        Treeview per riepilogo immissioni
        '''
        self.tree = ttk.Treeview(self, height=20)
        self.tree['columns'] = ('Prodotto', 'Quantita')
        self.tree['show'] = 'headings'
        self.tree.heading('Prodotto', text="Prodotto")
        self.tree.heading('Quantita', text="Quantita")

        self.tree.column("Prodotto", width=200)
        self.tree.column("Quantita", width=100)

        self.tree.grid(row='0', column='0')
        '''
        Labelframe per contenere i bottoni
        '''
        self.lblFrame_azioni = ttk.Labelframe(self, text='Azioni')
        self.lblFrame_azioni.grid(row='0', column='1', sticky='n')
        '''
        Label che indica la settimana
        '''
        n_sett = str(1 + int(strftime('%W')))
        self.lbl_settimana = ttk.Label(self.lblFrame_azioni, text='SETTIMANA NUMERO ' + n_sett, font='Helvetica')
        self.lbl_settimana.grid()
        '''
        Bottone per popolare il treeview
        '''
        self.btn = ttk.Button(self.lblFrame_azioni, text='Inserisci dati', command=self.inserisci)
        self.btn.grid()
        '''
        Entry per scegliere la settimana
        '''
        self.lbl_scelta_sett = ttk.Label(self.lblFrame_azioni, text='Settimana da visualizzare ')
        self.lbl_scelta_sett.grid()

        self.settimana = tk.StringVar()
        self.settimana.set('')
        self.entry_settimana_s = ttk.Entry(self.lblFrame_azioni, textvariable=self.settimana)
        self.entry_settimana_s.focus()
        self.entry_settimana_s.grid()
        '''
        Bottone per generare la stampa del pdf
        '''
        self.stampa = ttk.Button(self.lblFrame_azioni, text="Crea PDF", command=self.crea_pdf)
        self.stampa.grid()
        '''
        Bottone per uscita
        '''
        self.esci = ttk.Button(self.lblFrame_azioni, text='Esci', command=self.destroy)
        self.esci.grid()

    def inserisci(self):

        self.tree.delete(*self.tree.get_children())
        for row in self.c.execute('SELECT prodotto,SUM(quantita) '
                                  'FROM ingredienti '
                                  'WHERE settimana = ? '
                                  'GROUP BY prodotto',
                                  (self.settimana.get(),)):
            self.tree.insert("", 'end', values=(row[0], row[1]))

    def crea_pdf(self):
        data = [('settimana', 'codice', 'prodotto')]

        for i in self.c.execute("SELECT settimana,prodotto,SUM(quantita) "
                                "FROM ingredienti "
                                "WHERE settimana = ? "
                                "GROUP BY prodotto",
                                (self.settimana.get(),)):
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
        os.startfile("table.pdf")


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = ReportCucina(notebook)
    notebook.add(new, text='Dipendenti')
    root.mainloop()
