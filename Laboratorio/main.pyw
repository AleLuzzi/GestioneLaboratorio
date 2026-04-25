import customtkinter as ctk
from tkinter import messagebox
import os

from config import get_config
from theme import COLORS
from main_TKinter import (
    setup_root,
    build_main_ui,
    center_toplevel,
    build_anagrafica_access_ui,
)

# Run with script directory as cwd so config.ini and immagini/ are found
# (works when run as "python main.pyw" or "python Laboratorio/main.pyw")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Main(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_light"], *args, **kwargs)
        self.parent = parent

        self.config = get_config()
        build_main_ui(self)

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

    def anagrafica(self):
        password = "assist"

        def _try_login(event=None):
            if ent_password.get() == password:
                from anagrafica import Anagrafica
                Anagrafica()
                window.destroy()
            else:
                messagebox.showinfo(
                    "-- ERRORE --", "Non sei autorizzato ad entrare qui!", icon="warning"
                )
                window.destroy()

        # master esplicito + modalità dopo il rilascio del clic sul bottone principale,
        # altrimenti il ButtonRelease puo' attivare subito "Accedi" e chiudere il dialog.
        window = ctk.CTkToplevel(self.parent)
        window.transient(self.parent)
        center_toplevel(window)
        ent_password = build_anagrafica_access_ui(window, _try_login)
        window.lift()

        def _arm_modal():
            window.grab_set()
            ent_password.focus_set()

        window.after(50, _arm_modal)


if __name__ == "__main__":
    root = ctk.CTk()
    setup_root(root)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    Main(root).grid(row=0, column=0, sticky="nsew")
    root.mainloop()
