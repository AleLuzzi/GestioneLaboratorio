from anagrafica_produzione import *
from anagrafica_merceologie import *
from anagrafica_tagli import *
from anagrafica_impostazioni import *
from report_cucina_note import ReportCucina
import tkinter as tk
import tkinter.ttk as ttk


class Anagrafica(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Anagrafica")
        '''
        Disposizione Menu
        '''
        menubar = tk.Menu(self)
        anagraficamenu = tk.Menu(menubar, tearoff=0)
        anagraficamenu.add_command(label="Dipendenti", command=self._dipendenti)
        anagraficamenu.add_command(label="Fornitori", command=self._fornitori)
        anagraficamenu.add_command(label="Ingredienti", command=self._ingredienti)
        anagraficamenu.add_command(label="Produzione")
        anagraficamenu.add_command(label="Reparti", command=self._reparti)
        anagraficamenu.add_command(label="Merceologie", command=self._merceologie)
        anagraficamenu.add_command(label="Tagli")
        menubar.add_cascade(label="Anagrafica", menu=anagraficamenu)

        reportmenu = tk.Menu(menubar, tearoff=0)
        reportmenu.add_command(label="Cucina")
        menubar.add_cascade(label="Report", menu=reportmenu)

        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Configurazione")
        menubar.add_cascade(label="Configurazione", menu=config_menu)

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        self.config(menu=menubar)
        '''
        Notebook e posizione
        '''
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row='1', column='0')
        '''
        TAB 4 per Produzione
        '''
        self.tab4 = Produzione(self.notebook)
        self.notebook.add(self.tab4, text='Produzione', compound='left', image=self.img_btn1)
        '''
        TAB 7 per gestione tagli
        '''
        self.tab7 = Tagli(self.notebook)
        self.notebook.add(self.tab7, text='Tagli', compound='left', image=self.img_btn1)
        '''
        TAB 8 per report cucina
        '''
        self.tab8 = ReportCucina(self.notebook)
        self.notebook.add(self.tab8, text='Report Cucina', compound='left', image=self.img_btn1)
        '''
        TAB 9 per impostazioni
        '''
        self.tab9 = Impostazioni(self.notebook)
        self.notebook.add(self.tab9, text='Impostazioni', compound='left', image=self.img_btn1)

    @staticmethod
    def _dipendenti():
        from anagrafica_dipendenti import Dipendenti
        Dipendenti()

    @staticmethod
    def _fornitori():
        from anagrafica_fornitori import Fornitori
        Fornitori()

    @staticmethod
    def _ingredienti():
        from anagrafica_ingredienti import Ingredienti
        Ingredienti()

    @staticmethod
    def _reparti():
        from anagrafica_reparti import Reparti
        Reparti()

    @staticmethod
    def _merceologie():
        from anagrafica_merceologie import MerceologieCucina
        MerceologieCucina()


if __name__ == '__main__':
    root = tk.Tk()  
    new = Anagrafica()
    root.mainloop()
