import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import configparser


class Dipendenti(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.item = ''
        self.config = self.leggi_file_ini()

        # Connessione al Database
        self.conn = mysql.connector.connect(host=self.config['DataBase']['host'],
                                            database=self.config['DataBase']['db'],
                                            user=self.config['DataBase']['user'],
                                            password='')
        self.c = self.conn.cursor()

        # Definizione Frame
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        # LabelFrame gestione Dipendenti
        self.lbl_gest_dipendenti = ttk.LabelFrame(self.frame_sx, text='Gestione Dipendenti')

        # Treeview per tab Dipendenti
        self.tree_dipendenti = ttk.Treeview(self.lbl_gest_dipendenti, height=23)
        self.tree_dipendenti['columns'] = ('Id', 'Nome', 'Cognome', 'Reparto', 'email')
        self.tree_dipendenti['show'] = 'headings'
        self.tree_dipendenti.heading('Id', text="Id")
        self.tree_dipendenti.heading('Nome', text="Nome")
        self.tree_dipendenti.heading('Cognome', text="Cognome")
        self.tree_dipendenti.heading('Reparto', text="Reparto")
        self.tree_dipendenti.heading('email', text="E-mail")

        self.tree_dipendenti.column("Id", width=20)
        self.tree_dipendenti.column("Nome", width=80)
        self.tree_dipendenti.column("Cognome", width=80)
        self.tree_dipendenti.column("Reparto", width=50)
        self.tree_dipendenti.column("email", width=150)

        self.tree_dipendenti.bind("<Double-1>", self.ondoubleclick)

        # Lista campi del record
        self.campi = ['nome', 'cognome', 'reparto', 'email']
        self.label = {}
        self.entry = {}

        # LABELFRAME dettagli prodotto selezionato
        self.lbl_frame_dettagli_selezionato = ttk.LabelFrame(self.frame_centrale, text='Dettagli riga selezionata')

        # LABEL ed entry per mostrare dettagli prodotto selezionato
        r = 1
        c = 0
        for campo in self.campi:
            if r % 12 == 0:
                r = 1
                c += 2
            lbl = ttk.Label(self.lbl_frame_dettagli_selezionato, text=campo)
            lbl.grid(row=r, column=c)
            self.label[campo] = lbl

            ent = ttk.Entry(self.lbl_frame_dettagli_selezionato, width=25)
            ent.grid(row=r, column=c+1)
            self.entry[campo] = ent
            r += 1

        # LABELFRAME scegli prodotto
        self.lbl_frame_scegli = ttk.LabelFrame(self.frame_dx)

        # BOTTONI per azioni
        self.btn_modifica = tk.Button(self.lbl_frame_scegli,
                                      text='Salva Modifiche',
                                      font=('Helvetica', 10),
                                      command=self.modifica)
        self.btn_inserisci = tk.Button(self.lbl_frame_scegli,
                                       text='Inserisci Dati',
                                       font=('Helvetica', 10),
                                       command=self._inserisci)

        # LAYOUT
        self.frame_sx.grid(row=1, column=0, sticky='n')
        self.frame_centrale.grid(row=1, column=1, sticky='n')
        self.frame_dx.grid(row=1, column=2, sticky='n')

        self.lbl_gest_dipendenti.grid(row=1, column=0, sticky='n')
        self.tree_dipendenti.grid(row=1, column=0, columnspan=3)

        self.lbl_frame_dettagli_selezionato.grid(row=1, column=0, sticky='n')

        self.lbl_frame_scegli.grid(row=1, column=0)
        self.btn_modifica.grid(row=1, column=0, columnspan=2, sticky='we')
        self.btn_inserisci.grid(row=2, column=0, columnspan=2, sticky='we')

        self.aggiorna()

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def modifica(self):
        for campo in self.campi:
            stringa = 'UPDATE dipendenti SET {}=%s WHERE ID = %s'.format(campo)
            self.c.execute(stringa, (self.entry[campo].get(), (self.item[0])))
            self.conn.commit()
        self.aggiorna()

    def aggiorna(self):
        self.tree_dipendenti.delete(*self.tree_dipendenti.get_children())
        self.c.execute("SELECT * From dipendenti ")
        for lista in self.c:
            self.tree_dipendenti.insert('', 'end', values=(lista[0], lista[1], lista[2], lista[3], lista[4]))

        lista = []

        self.c.execute("SELECT ID From dipendenti")
        for row in self.c:
            lista.extend(row)

    def ondoubleclick(self, event):
        for campo in self.campi:
            self.entry[campo].delete(0, 'end')

        self.item = (self.tree_dipendenti.item(self.tree_dipendenti.selection(), 'values'))

        i = 1
        self.c.execute("SELECT * FROM dipendenti WHERE ID = %s", (self.item[0],))
        for self.row in self.c:
            for campo in self.campi:
                self.entry[campo].insert(0, self.row[i])
                i += 1
                
    def _inserisci(self):

        def _centra(toplevel):
            screen_width = toplevel.winfo_screenwidth()
            screen_height = toplevel.winfo_screenheight()

            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = screen_width / 3 - size[0] / 2
            y = screen_height / 3 - size[1] / 2

            toplevel.geometry("+%d+%d" % (x, y))

        def _salva_nuovo():
            rep = reparto_new.get()
            if rep != '' and nome_new.get() != '':
                self.c.execute("SELECT Id FROM reparti WHERE reparto = %s", (rep,))
                lista_da_salvare = [nome_new.get(), cognome_new.get(), self.c.fetchone()[0], email_new.get()]
                # print(lista_da_salvare)
                self.c.execute('INSERT INTO dipendenti(nome,cognome,reparto,email) VALUES (%s,%s,%s,%s)', lista_da_salvare)
                self.conn.commit()
                self._aggiorna()
                nuovo_dato.destroy()
            else:
                messagebox.showinfo('ATTENZIONE', 'CI SONO CAMPI VUOTI')

        nuovo_dato = tk.Toplevel()

        _centra(nuovo_dato)
        nome_new = tk.StringVar()
        cognome_new = tk.StringVar()
        reparto_new = tk.StringVar()
        email_new = tk.StringVar()
        
        lbl_nome = tk.Label(nuovo_dato, text='Nome')
        ent_nome = tk.Entry(nuovo_dato, textvariable=nome_new)
        lbl_cognome = tk.Label(nuovo_dato, text='Cognome')
        ent_cognome = tk.Entry(nuovo_dato, textvariable=cognome_new)
        lbl_reparto = tk.Label(nuovo_dato, text='Reparto')
        cmb_reparto = ttk.Combobox(nuovo_dato, textvariable=reparto_new)
        lbl_email = tk.Label(nuovo_dato, text='Email')
        ent_email = ttk.Entry(nuovo_dato, textvariable=email_new)

        btn_salva = tk.Button(nuovo_dato, text='Salva Dati', command=_salva_nuovo)
        btn_chiudi = tk.Button(nuovo_dato, text='Chiudi', command=nuovo_dato.destroy)
        
        lista_reparti_new = []
        self.c.execute("SELECT reparto From reparti")
        for row in self.c:
            lista_reparti_new.extend(row)
        cmb_reparto['values'] = lista_reparti_new

        lbl_nome.grid(row=0, column=0)
        ent_nome.grid(row=0, column=1, sticky='we')
        lbl_cognome.grid(row=1, column=0)
        ent_cognome.grid(row=1, column=1, sticky='we')
        lbl_reparto.grid(row=2, column=0)
        cmb_reparto.grid(row=2, column=1)
        lbl_email.grid(row=3, column=0)
        ent_email.grid(row=3, column=1, sticky='we')

        btn_salva.grid(row=4, column=0, sticky='we')
        btn_chiudi.grid(row=4, column=1, sticky='we')
	
		
		


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Dipendenti(notebook)
    notebook.add(new, text='Dipendenti')
    root.mainloop()
