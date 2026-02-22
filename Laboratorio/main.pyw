import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os

from config import get_config
from theme import (
    apply_theme, COLORS,
    style_header_frame, style_content_frame, style_footer_frame,
    get_font, FONT_SIZE_LARGE,
)

# Run with script directory as cwd so config.ini and immagini/ are found
# (works when run as "python main.pyw" or "python Laboratorio/main.pyw")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg=COLORS["bg_light"])

        self.config = get_config()

        self.frm_alto = tk.Frame(self, bd=0, highlightthickness=0)
        style_header_frame(self.frm_alto)
        self.frm_centrale = tk.Frame(self, height=200, width=800, bd=0, highlightthickness=0)
        style_content_frame(self.frm_centrale)
        self.frm_basso = tk.Frame(self, bd=0, highlightthickness=0)
        style_footer_frame(self.frm_basso)

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
                               image=self.img_btn9_a, state='disabled')  # da implementare

        bottone9b = ttk.Button(self.frm_alto, text="Dosi", compound='bottom',
                               image=self.img_btn9_b, command=self.dosi)

        bottone10 = ttk.Button(self.frm_alto, text="Uscita", compound='bottom',
                               image=self.img_btn10, command=self._esci)

        self.immagine1 = tk.PhotoImage(
            file=os.path.join('immagini', 'dlogo.gif'))

        label1 = tk.Label(self.frm_centrale, image=self.immagine1, bd=0, bg=COLORS["bg_content"])

        lbl_utente = tk.Label(
            self.frm_basso, text='Utente: ',
            font=get_font(), fg=COLORS["text_dark"], bg=COLORS["bg_light"])
        lbl_nome_utente = tk.Label(
            self.frm_basso, text=os.environ.get('COMPUTERNAME', ''),
            font=get_font(), fg=COLORS["text_dark"], bg=COLORS["bg_light"])
        lbl_winswgx = tk.Label(
            self.frm_basso, text='Winswgx: ',
            font=get_font(), fg=COLORS["text_light"], bg=COLORS["bg_light"])
        lbl_winswgx_percorso = tk.Label(
            self.frm_basso, text=self.config['Winswgx']['dir'] or '(non impostato)',
            font=get_font(), fg=COLORS["text_dark"], bg=COLORS["bg_light"])

        pad = (8, 12)
        bottone1.grid(row=0, column=0, padx=pad[0], pady=pad[1])
        bottone2.grid(row=0, column=1, padx=pad[0], pady=pad[1], sticky='we')
        bottone3.grid(row=0, column=2, padx=pad[0], pady=pad[1], sticky='we')
        bottone6.grid(row=0, column=3, padx=pad[0], pady=pad[1])
        bottone7.grid(row=0, column=4, padx=pad[0], pady=pad[1])
        bottone8.grid(row=0, column=5, padx=pad[0], pady=pad[1])
        bottone9a.grid(row=0, column=6, padx=pad[0], pady=pad[1])
        bottone9b.grid(row=0, column=7, padx=pad[0], pady=pad[1])
        bottone10.grid(row=0, column=8, padx=pad[0], pady=pad[1])
        bottone5.grid(row=1, column=0, padx=pad[0], pady=pad[1])
        bottone4.grid(row=1, column=1, padx=pad[0], pady=pad[1])
        bottone4a.grid(row=1, column=2, padx=pad[0], pady=pad[1])
        bottone9.grid(row=1, column=3, padx=pad[0], pady=pad[1])

        self.frm_centrale.grid_propagate(False)
        self.frm_centrale.grid_rowconfigure(0, weight=2)
        self.frm_centrale.grid_columnconfigure(0, weight=2)

        self.frm_alto.grid(row=0, column=0)
        self.frm_centrale.grid(row=1, column=0)
        self.frm_basso.grid(row=2, column=0, sticky="we")

        label1.grid(row=0, column=0)
        lbl_utente.grid(row=0, column=0)
        lbl_nome_utente.grid(row=0, column=1, padx=4, pady=4)
        lbl_winswgx.grid(row=0, column=2)
        lbl_winswgx_percorso.grid(row=0, column=3)

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

    def _esci(self):
        """Chiude l'applicazione."""
        self.parent.destroy()

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
        window.configure(bg=COLORS["bg_light"])
        window.title("Accesso Impostazioni")
        window.bind('<Return>', _try_login)

        lbl_password = tk.Label(
            window, text="Password:", font=get_font(FONT_SIZE_LARGE),
            bg=COLORS["bg_light"], fg=COLORS["text_dark"])
        ent_password = ttk.Entry(window, show="*", width=20)
        btn_login = ttk.Button(window, text="Accedi", command=_try_login)
        ent_password.focus()

        lbl_password.grid(row=0, column=0, padx=8, pady=8)
        ent_password.grid(row=0, column=1, padx=8, pady=8)
        btn_login.grid(row=1, column=0, columnspan=2, padx=8, pady=12, sticky='we')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('900x400+40+40')
    root.minsize(800, 350)
    root.title('Gestione Laboratorio')
    root.configure(bg=COLORS["bg_light"])
    apply_theme(root)
    Main(root).grid(sticky='nsew')
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
