import tkinter as tk
from tkinter import ttk
import mysql.connector


class Inventario(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Inventario")

        self.value = tk.StringVar()

        # connessione database
        self.conn = mysql.connector.connect(host='192.168.0.100',
                                            database='data',
                                            user='root',
                                            password='')
        self.c = self.conn.cursor()

        self.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0)

        # TAB 1 AGNELLO
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='AGNELLO', compound='left', image=self.img_btn1)

        lst_agnello = []
        self.c.execute("SELECT taglio FROM tagli")
        for row in self.c:
            lst_agnello.extend(row)

        r, c = 1, 0
        for i in range(0, len(lst_agnello)):
            if r % 10 == 0:
                c += 1
                r = 1
            tk.Radiobutton(self.tab1, text=lst_agnello[i].upper(), indicatoron=0, variable=self.value,
                           font='Verdana', width=20,
                           value=lst_agnello[i]).grid(row=r, column=c)
            r += 1

        # TAB 2 BOVINO
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='BOVINO', compound='left', image=self.img_btn1)

        # TAB 3 SUINO
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='SUINO', compound='left', image=self.img_btn1)

        # TAB 4 VITELLO
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='VITELLO', compound='left', image=self.img_btn1)


if __name__ == '__main__':
    root = tk.Tk()
    new = Inventario()
    root.mainloop()
