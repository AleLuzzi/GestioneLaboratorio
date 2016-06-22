from tkinter import *

from ingredienti import Ingredienti
from ingresso_merce import IngressoMerce
from chiudi_lotto import ChiudiLotto
from lotti_vendita import LottiInVendita
from nuovo_lotto import NuovoLotto
from nuovo_lotto_cucina import NuovoLottoCucina
from inventario import Inventario
from anagrafica import Anagrafica
import sys

sys.path.append('..//Laboratorio')

form1 = Tk()
form1.geometry('%dx525+0+0' % form1.winfo_screenwidth())
form1.title("Gestione Laboratorio 1.0")


def btn1premuto():
    IngressoMerce()


def btn2premuto():
    NuovoLotto()


def btn3premuto():
    Inventario()


def btn4premuto():
    NuovoLottoCucina()


def btn5premuto():
    Ingredienti()


def btn6premuto():
    ChiudiLotto()


def btn7premuto():
    LottiInVendita()


def btn8premuto():
    Anagrafica()


def btn9premuto():
    form1.destroy()


# Frame alto con pulsanti ---------------------------------------------
frame1 = Frame(form1, bd=1, relief="raised", bg="yellow")
frame1.grid(row=0, column=0, sticky="we")

img_btn1 = PhotoImage(file=".//immagini//lbeef.gif")
img_btn2 = PhotoImage(file=".//immagini//documentnew.gif")
img_btn3 = PhotoImage(file=".//immagini//drun.gif")
img_btn4 = PhotoImage(file=".//immagini//lfood.gif")
img_btn5 = PhotoImage(file=".//immagini//ingredienti.gif")
img_btn6 = PhotoImage(file=".//immagini//lock.gif")
img_btn7 = PhotoImage(file=".//immagini//lvendita.gif")
img_btn8 = PhotoImage(file=".//immagini//impostazioni.gif")
img_btn9 = PhotoImage(file=".//immagini//exit.gif")

bottone1 = Button(frame1, text="Ingresso Merce", compound='bottom',
                  image=img_btn1, command=btn1premuto)
bottone1.grid(row=0, column=0, padx=4, pady=4)

bottone2 = Button(frame1, text="Nuovo Lotto", compound='bottom',
                  image=img_btn2, command=btn2premuto)
bottone2.grid(row=0, column=1, padx=4, pady=4)

bottone3 = Button(frame1, text="Inventario", compound='bottom',
                  image=img_btn3, command=btn3premuto)
bottone3.grid(row=0, column=2, padx=4, pady=4)

bottone4 = Button(frame1, text="Lotto Cucina", compound='bottom',
                  image=img_btn4, command=btn4premuto)
bottone4.grid(row=0, column=3, padx=4, pady=4)

bottone5 = Button(frame1, text="Ingredienti", compound='bottom',
                  image=img_btn5, command=btn5premuto)
bottone5.grid(row=0, column=4, padx=4, pady=4)

bottone6 = Button(frame1, text="Chiudi Lotti", compound='bottom',
                  image=img_btn6, command=btn6premuto)
bottone6.grid(row=0, column=5, padx=4, pady=4)

bottone7 = Button(frame1, text="Vendita", compound='bottom',
                  image=img_btn7, command=btn7premuto)
bottone7.grid(row=0, column=6, padx=4, pady=4)

bottone8 = Button(frame1, text="Impostazioni", compound='bottom',
                  image=img_btn8, command=btn8premuto)
bottone8.grid(row=0, column=7, padx=4, pady=4)

bottone9 = Button(frame1, text="Uscita", compound='bottom',
                  image=img_btn9, command=btn9premuto)
bottone9.grid(row=0, column=8, padx=4, pady=4)


# Frame centrale con immagine centrata --------------------------------
frame2 = Frame(form1, height=400, width=form1.winfo_screenwidth(), bd=1, relief="raised", bg="white")
frame2.grid_propagate(False)
frame2.grid_rowconfigure(0, weight=2)
frame2.grid_columnconfigure(0, weight=2)
frame2.grid(row=1, column=0)

# versione Win
immagine1 = PhotoImage(file=".//immagini//dlogo.gif")

label1 = Label(frame2, image=immagine1, bd=0)
label1.grid(row=0, column=0)

# Frame basso con label -----------------------------------------------
frame3 = Frame(form1, bd=1, relief="raised")
frame3.grid(row=2, column=0, sticky="we")

label2 = Label(frame3, text="Barra di stato")
label2.grid(row=0, column=0, padx=4, pady=4)


form1.mainloop()
