from anagrafica_reparti import *
from anagrafica_dipendenti import *
from anagrafica_fornitori import *
from anagrafica_ingredienti import *
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
        # self.geometry('%dx525+0+0' % self.winfo_screenwidth())
        '''
        Disposizione Frame
        '''
        '''
        self.frame = ttk.Frame(self)
        self.frame.grid(row='1', column='0')
        '''
        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")
        '''
        Notebook e posizione
        '''
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row='1', column='0')
        '''
        TAB 1 per Dipendenti
        '''
        self.tab1 = Dipendenti(self.notebook)
        self.notebook.add(self.tab1,  text='Dipendenti', compound='left', image=self.img_btn1)
        '''
        TAB 2 per Fornitori
        '''
        self.tab2 = Fornitori(self.notebook)
        self.notebook.add(self.tab2, text='Fornitori', compound='left', image=self.img_btn1)

        '''
        TAB 3 per Ingredienti
        '''
        self.tab3 = Ingredienti(self.notebook)
        self.notebook.add(self.tab3, text='Ingredienti', compound='left', image=self.img_btn1)
        '''
        TAB 4 per Produzione
        '''
        self.tab4 = Produzione(self.notebook)
        self.notebook.add(self.tab4, text='Produzione', compound='left', image=self.img_btn1)
        '''
        TAB 5 per Reparti
        '''
        self.tab5 = Reparti(self.notebook)
        self.notebook.add(self.tab5, text='Reparti', compound='left', image=self.img_btn1)
        '''
        TAB 6 per Merceologia Cucina
        '''
        self.tab6 = MerceologieCucina(self.notebook)
        self.notebook.add(self.tab6, text='Merceologia', compound='left', image=self.img_btn1)
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

if __name__ == '__main__':
    root = tk.Tk()
    new = Anagrafica()
    root.mainloop()
