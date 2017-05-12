import tkinter as tk
from tkinter import ttk, filedialog
import configparser


class Impostazioni(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.config = self.leggi_file_ini()

        # STRINGVAR
        self.win_dir = tk.StringVar()
        self.win_dir.set(self.config['Winswgx']['dir'])

        # FRAME
        self.frame_sx = tk.Frame(self)
        self.frame_centrale = tk.Frame(self)
        self.frame_dx = tk.Frame(self)

        # LABELFRAME Database
        self.lblfrm_imp_database = tk.LabelFrame(self, text='DataBase', foreground='blue')

        # LABELFRAME winswgx
        self.lblfrm_winswgx = tk.LabelFrame(self, text='Winswgx-net', foreground='blue')

        # LABELFRAME Facebook
        self.lblfrm_facebook = tk.LabelFrame(self, text='Facebook', foreground='blue')

        # LABEL Database
        self.lbl_database = tk.Label(self.lblfrm_imp_database, text='Data Base')
        self.lbl_host = tk.Label(self.lblfrm_imp_database, text='Host')
        self.lbl_port = tk.Label(self.lblfrm_imp_database, text='Port')
        self.lbl_user = tk.Label(self.lblfrm_imp_database, text='User')
        self.lbl_pwd = tk.Label(self.lblfrm_imp_database, text='Password')

        self.lbl_database_value = tk.Label(self.lblfrm_imp_database, text=self.config['DataBase']['db'])
        self.lbl_host_value = tk.Label(self.lblfrm_imp_database, text=self.config['DataBase']['host'])
        self.lbl_port_value = tk.Label(self.lblfrm_imp_database, text=self.config['DataBase']['port'])
        self.lbl_user_value = tk.Label(self.lblfrm_imp_database, text=self.config['DataBase']['user'])
        self.lbl_pwd_value = tk.Label(self.lblfrm_imp_database, text=self.config['DataBase']['pwd'])

        # LABEL Winswgx-net
        self.lbl_dir_name = tk.Button(self.lblfrm_winswgx,
                                      text='Winswgx-Net Folder',
                                      command=self.open_dir)
        self.lbl_win_loc = tk.Label(self.lblfrm_winswgx,
                                    textvariable=self.win_dir,
                                    relief='sunken')

        # LABEL Facebook
        self.lbl_facebook = tk.Label(self.lblfrm_facebook,
                                     text='Token Facebook')

        # LAYOUT
        self.frame_sx.grid()

        self.lblfrm_imp_database.grid(row=0, column=0, sticky='we')
        self.lbl_database.grid(row=0, column=0)
        self.lbl_database_value.grid(row=0, column=1)
        self.lbl_host.grid(row=1, column=0)
        self.lbl_host_value.grid(row=1, column=1)
        self.lbl_port.grid(row=2, column=0)
        self.lbl_port_value.grid(row=2, column=1)
        self.lbl_user.grid(row=3, column=0)
        self.lbl_user_value.grid(row=3, column=1)
        self.lbl_pwd.grid(row=4, column=0)
        self.lbl_pwd_value.grid(row=4, column=1)

        self.lblfrm_winswgx.grid(row=1, column=0)
        self.lbl_dir_name.grid(row=0, column=0)
        self.lbl_win_loc.grid(row=0, column=1)

        self.lblfrm_facebook.grid(row=2, column=0, sticky='we')
        self.lbl_facebook.grid()

    @staticmethod
    def leggi_file_ini():
        ini = configparser.ConfigParser()
        ini.read('config.ini')
        return ini

    def open_dir(self):
        new_dirname = filedialog.askdirectory(parent=self.frame_centrale, initialdir='c:\\')
        cfg_file = open('config.ini', 'w')
        self.config.set('Winswgx', 'dir', new_dirname)
        self.config.write(cfg_file)
        self.win_dir.set(new_dirname)


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Impostazioni(notebook)
    notebook.add(new, text='Impostazioni')
    root.mainloop()
