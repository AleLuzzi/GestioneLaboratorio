import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3


class Impostazioni(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        '''
        Connessione al Database
        '''
        self.conn = sqlite3.connect('data.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        '''
        Definizione Frame
        '''
        self.frame_sx = ttk.Frame(self)
        self.frame_centrale = ttk.Frame(self)
        self.frame_dx = ttk.Frame(self)

        self.btn1 = ttk.Button(self.frame_sx, text='Seleziona la cartella di Winswgx-net', command=self.open_dir)
        self.lbl_dir_name = ttk.Label(self.frame_sx, text='')

        self.frame_sx.grid()
        self.btn1.grid(row=1, column=1)
        self.lbl_dir_name.grid(row=2, column=1)

        self.dirname = ''

    def open_dir(self):
        self.dirname = filedialog.askdirectory(parent=self.frame_centrale, initialdir='c:\\')
        self.lbl_dir_name.config(text=self.dirname)


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Impostazioni(notebook)
    notebook.add(new, text='Impostazioni')
    root.mainloop()