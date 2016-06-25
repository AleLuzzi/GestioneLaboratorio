import tkinter as tk
import tkinter.ttk as ttk

from ingredienti import Ingredienti
from ingresso_merce import IngressoMerce
from chiudi_lotto import ChiudiLotto
from lotti_vendita import LottiInVendita
from nuovo_lotto import NuovoLotto
from nuovo_lotto_cucina import NuovoLottoCucina
from inventario import Inventario
from anagrafica import Anagrafica


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.frm_alto = tk.Frame(self, bd=1, relief="raised", bg="yellow")
        self.frm_centrale = tk.Frame(self,height=400, width=self.winfo_screenwidth(), bd=1, relief="raised", bg="white")
        self.frm_basso = tk.Frame(self, bd=1, relief="raised")
        
        self.frm_alto.grid(row=0, column=0)
        self.frm_centrale.grid(row=1, column=0)
        self.frm_basso.grid(row=2, column=0, sticky="we")

        self.img_btn1 = tk.PhotoImage(file=".//immagini//lbeef.gif")
        self.img_btn2 = tk.PhotoImage(file=".//immagini//documentnew.gif")
        self.img_btn3 = tk.PhotoImage(file=".//immagini//drun.gif")
        self.img_btn4 = tk.PhotoImage(file=".//immagini//lfood.gif")
        self.img_btn5 = tk.PhotoImage(file=".//immagini//ingredienti.gif")
        self.img_btn6 = tk.PhotoImage(file=".//immagini//lock.gif")
        self.img_btn7 = tk.PhotoImage(file=".//immagini//lvendita.gif")
        self.img_btn8 = tk.PhotoImage(file=".//immagini//impostazioni.gif")
        self.img_btn9 = tk.PhotoImage(file=".//immagini//exit.gif")

        bottone1 = ttk.Button(self.frm_alto, text="Ingresso Merce", compound='bottom',
                              image=self.img_btn1, command=self.ingresso_merce)

        bottone1.grid(row=0, column=0, padx=4, pady=4)
    
        bottone2 = ttk.Button(self.frm_alto, text="Nuovo Lotto", compound='bottom',
                              image=self.img_btn2, command=self.nuovo_lotto)
        bottone2.grid(row=0, column=1, padx=4, pady=4)
    
        bottone3 = ttk.Button(self.frm_alto, text="Inventario", compound='bottom',
                              image=self.img_btn3, command=self.inventario)
        bottone3.grid(row=0, column=2, padx=4, pady=4)
    
        bottone4 = ttk.Button(self.frm_alto, text="Lotto Cucina", compound='bottom',
                              image=self.img_btn4, command=self.nuovo_lotto_cucina)
        bottone4.grid(row=0, column=3, padx=4, pady=4)
    
        bottone5 = ttk.Button(self.frm_alto, text="Ingredienti", compound='bottom',
                              image=self.img_btn5, command=self.ingredienti)
        bottone5.grid(row=0, column=4, padx=4, pady=4)
    
        bottone6 = ttk.Button(self.frm_alto, text="Chiudi Lotti", compound='bottom',
                              image=self.img_btn6, command=self.chiudi_lotto)
        bottone6.grid(row=0, column=5, padx=4, pady=4)
    
        bottone7 = ttk.Button(self.frm_alto, text="Vendita", compound='bottom',
                              image=self.img_btn7, command=self.lotti_in_vendita)
        bottone7.grid(row=0, column=6, padx=4, pady=4)

        bottone8 = ttk.Button(self.frm_alto, text="Impostazioni", compound='bottom',
                              image=self.img_btn8, command=self.anagrafica)

        bottone8.grid(row=0, column=7, padx=4, pady=4)
    
        bottone9 = ttk.Button(self.frm_alto, text="Uscita", compound='bottom',
                              image=self.img_btn9, command=self.quit)
        bottone9.grid(row=0, column=8, padx=4, pady=4)

        self.frm_centrale.grid_propagate(False)
        self.frm_centrale.grid_rowconfigure(0, weight=2)
        self.frm_centrale.grid_columnconfigure(0, weight=2)
        self.frm_centrale.grid(row=1, column=0)

        self.immagine1 = tk.PhotoImage(file=".//immagini//dlogo.gif")

        label1 = tk.Label(self.frm_centrale, image=self.immagine1, bd=0)
        label1.grid(row=0, column=0)

        label2 = tk.Label(self.frm_basso, text="Barra di stato")
        label2.grid(row=0, column=0, padx=4, pady=4)

    @staticmethod
    def ingresso_merce():
        IngressoMerce()

    @staticmethod
    def nuovo_lotto():
        NuovoLotto()

    @staticmethod
    def inventario():
        Inventario()

    @staticmethod
    def nuovo_lotto_cucina():
        NuovoLottoCucina()

    @staticmethod
    def ingredienti():
        Ingredienti()

    @staticmethod
    def chiudi_lotto():
        ChiudiLotto()

    @staticmethod
    def lotti_in_vendita():
        LottiInVendita()

    @staticmethod
    def anagrafica():
        Anagrafica()


if __name__ == "__main__":
    root = tk.Tk()
    Main(root).grid()
    root.mainloop()
