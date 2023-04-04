import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import configparser
import os


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.config = self.leggi_file_ini()

        self.frm_alto = tk.Frame(self, bd=1, relief="raised", bg="yellow")
        self.frm_centrale = tk.Frame(
            self, height=200, width=800, bd=1, relief="raised", bg="white")
        self.frm_basso = tk.Frame(self, bd=1, relief="raised")

        self.img_btn1 = tk.PhotoImage(
            file=os.path.join('immagini', 'lbeef.gif'))
        self.img_btn2 = tk.PhotoImage(
            file=os.path.join('immagini', 'documentnew.gif'))
        self.img_btn3 = tk.PhotoImage(
            file=os.path.join('immagini', 'drun.gif'))
        self.img_btn4 = tk.PhotoImage(
            file=os.path.join('immagini', 'lfood.gif'))
        self.img_btn4_a = tk.PhotoImage(
            file=os.path.join('immagini', 'list.gif'))
        self.img_btn5 = tk.PhotoImage(
            file=os.path.join('immagini', 'ingredienti.gif'))
        self.img_btn6 = tk.PhotoImage(
            file=os.path.join('immagini', 'lock.gif'))
        self.img_btn7 = tk.PhotoImage(
            file=os.path.join('immagini', 'lvendita.gif'))
        self.img_btn8 = tk.PhotoImage(
            file=os.path.join('immagini', 'impostazioni.gif'))
        self.img_btn9 = tk.PhotoImage(
            file=os.path.join('immagini', 'menu.gif'))
        self.img_btn9_a = tk.PhotoImage(
            file=os.path.join('immagini', 'Order.gif'))
        self.img_btn9_b = tk.PhotoImage(
            file=os.path.join('immagini', 'bilancia.gif'))
        self.img_btn10 = tk.PhotoImage(
            file=os.path.join('immagini', 'exit.gif'))

        bottone1 = ttk.Button(
            self.frm_alto, text="Ingresso Merce", compound='bottom',
            image=self.img_btn1, command=self.ingresso_merce)

        bottone2 = ttk.Button(
            self.frm_alto, text="Nuovo Lotto", compound='bottom',
            image=self.img_btn2, command=self.nuovo_lotto)

        bottone3 = ttk.Button(self.frm_alto, text="Inventario", compound='bottom',
                              image=self.img_btn3, command=self.inventario)

        bottone4 = ttk.Button(self.frm_alto, text="Lotto Cucina", compound='bottom',
                              image=self.img_btn4, command=self.nuovo_lotto_cucina)

        bottone4a = ttk.Button(self.frm_alto, text="Lotti Vendita Cucina", compound='bottom',
                               image=self.img_btn4_a, command=self.lotti_vendita_cucina)

        bottone5 = ttk.Button(self.frm_alto, text="Ingredienti", compound='bottom',
                              image=self.img_btn5, command=self.ingredienti)

        bottone6 = ttk.Button(self.frm_alto, text="Chiudi Lotti", compound='bottom',
                              image=self.img_btn6, command=self.chiudi_lotto)

        bottone7 = ttk.Button(self.frm_alto, text="Vendita", compound='bottom',
                              image=self.img_btn7, command=self.lotti_in_vendita)

        bottone8 = ttk.Button(self.frm_alto, text="Impostazioni", compound='bottom',
                              image=self.img_btn8, command=self.anagrafica)

        bottone9 = ttk.Button(self.frm_alto, text="Nuovo Menu", compound='bottom',
                              image=self.img_btn9, command=self.nuovo_menu)

        bottone9a = ttk.Button(self.frm_alto, text="Ordine", compound='bottom',
                               image=self.img_btn9_a)

        bottone9b = ttk.Button(self.frm_alto, text="Dosi", compound='bottom',
                               image=self.img_btn9_b, command=self.dosi)

        bottone10 = ttk.Button(self.frm_alto, text="Uscita", compound='bottom',
                               image=self.img_btn10, command=self.quit)

        self.immagine1 = tk.PhotoImage(
            file=os.path.join('immagini', 'dlogo.gif'))

        label1 = tk.Label(self.frm_centrale, image=self.immagine1, bd=0)

        lbl_utente = tk.Label(self.frm_basso, text='Utente Collegato : ')

        lbl_nome_utente = tk.Label(self.frm_basso, text=os.environ['COMPUTERNAME'])

        lbl_winswgx = tk.Label(self.frm_basso, text='Percorso Winswgx = ')
        lbl_winswgx_percorso = tk.Label(self.frm_basso, text=self.config['Winswgx']['dir'])

        bottone1.grid(row=0, column=0, padx=4, pady=4)
        bottone2.grid(row=0, column=1, padx=4, pady=4, sticky='we')
        bottone3.grid(row=0, column=2, padx=4, pady=4, sticky='we')
        bottone6.grid(row=0, column=3, padx=4, pady=4)
        bottone7.grid(row=0, column=4, padx=4, pady=4)
        bottone8.grid(row=0, column=5, padx=4, pady=4)
        bottone9a.grid(row=0, column=6, padx=4, pady=4)
        bottone9b.grid(row=0, column=7, padx=4, pady=4)
        bottone10.grid(row=0, column=8, padx=4, pady=4)
        bottone5.grid(row=1, column=0, padx=4, pady=4)
        bottone4.grid(row=1, column=1, padx=4, pady=4)
        bottone4a.grid(row=1, column=2, padx=4, pady=4)
        bottone9.grid(row=1, column=3, padx=4, pady=4)

        self.frm_centrale.grid_propagate(False)
        self.frm_centrale.grid_rowconfigure(0, weight=2)
        self.frm_centrale.grid_columnconfigure(0, weight=2)

        self.frm_alto.grid(row=0, column=0)
        self.frm_centrale.grid(row=1, column=0)
        self.frm_basso.grid(row=2, column=0, sticky="we")
        self.frm_centrale.grid(row=1, column=0)

        label1.grid(row=0, column=0)
        lbl_utente.grid(row=0, column=0)
        lbl_nome_utente.grid(row=0, column=1, padx=4, pady=4)
        lbl_winswgx.grid(row=0, column=2)
        lbl_winswgx_percorso.grid(row=0, column=3)

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini
    
    @staticmethod
    def ingresso_merce():
        from ingresso_merce import IngressoMerce
        IngressoMerce()

    @staticmethod
    def nuovo_lotto():
        from nuovo_lotto import NuovoLotto
        NuovoLotto()

    @staticmethod
    def inventario():
        from inventario import Inventario
        Inventario()

    @staticmethod
    def nuovo_lotto_cucina():
        from nuovo_lotto_cucina import NuovoLottoCucina
        NuovoLottoCucina()

    @staticmethod
    def lotti_vendita_cucina():
        from lotti_vendita_cucina import LottiInVenditaCucina
        LottiInVenditaCucina()

    @staticmethod
    def ingredienti():
        from ingredienti import Ingredienti
        Ingredienti()

    @staticmethod
    def chiudi_lotto():
        from chiudi_lotto import ChiudiLotto
        ChiudiLotto()

    @staticmethod
    def lotti_in_vendita():
        from lotti_vendita import LottiInVendita
        LottiInVendita()

    @staticmethod
    def nuovo_menu():
        from nuovo_menu import NuovoMenu
        NuovoMenu()

    @staticmethod
    def dosi():
        from dosi import Dosi
        Dosi()

    @staticmethod
    def anagrafica():
        password = "assist"

        def _centra(toplevel):
            screen_width = toplevel.winfo_screenwidth()
            screen_height = toplevel.winfo_screenheight()

            size = tuple(int(_)
                         for _ in toplevel.geometry().split('+')[0].split('x'))
            x = screen_width / 3 - size[0] / 2
            y = screen_height / 3 - size[1] / 2

            toplevel.geometry("+%d+%d" % (x, y))

        def _try_login(event=None):
            if ent_password.get() == password:
                from anagrafica import Anagrafica
                Anagrafica()
                window.destroy()
            else:
                messagebox.showinfo(
                    "-- ERRORE --", "Non sei autorizzato ad entrare qui!", icon="warning")
                window.destroy()

        window = tk.Toplevel()
        _centra(window)

        window.title("Log-In")
        window.bind('<Return>', _try_login)

        lbl_password = tk.Label(window, text="Password:", font=('Verdana', 15))
        ent_password = tk.Entry(window, show="*")

        btn_login = tk.Button(window, text="Login", command=_try_login)
        ent_password.focus()

        lbl_password.grid(row=0, column=0)
        ent_password.grid(row=0, column=1)
        btn_login.grid(row=1, column=0, columnspan=2, sticky='we')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('+0+0')
    root.title('Gestione Laboratorio')
    Main(root).grid()
    root.mainloop()
