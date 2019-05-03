import tkinter as tk
from tkinter import ttk, filedialog
import configparser
import win32print


class Impostazioni(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.config = self.leggi_file_ini()
        self.token_fb_status = self.controlla_token()
        self.img_btn = tk.PhotoImage(file=".//immagini//Save-icon.gif")

        # STRINGVAR
        self.win_dir = tk.StringVar()
        self.win_dir.set(self.config['Winswgx']['dir'])
        self.stampante_value = tk.StringVar()
        self.stampante_value.set(self.config['Stampante']['stampa'])

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

        # LABELFRAME Stampante
        self.lblfrm_stampante = tk.LabelFrame(self, text='Stampante', foreground='blue')

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
        self.lbl_win_loc_value = tk.Label(self.lblfrm_winswgx,
                                          textvariable=self.win_dir,
                                          relief='sunken')

        # LABEL Facebook
        self.lbl_token_fb = tk.Label(self.lblfrm_facebook,
                                     text='Token Facebook')
        self.lbl_token_fb_value = tk.Label(self.lblfrm_facebook,
                                           text=self.token_fb_status,
                                           relief='sunken')
        self.lbl_scad_token = tk.Label(self.lblfrm_facebook,
                                       text='Scadenza Token')
        self.lbl_scad_token_value = tk.Label(self.lblfrm_facebook,
                                             text=self.config['Facebook']['scadenza'],
                                             relief='sunken')

        # LABEL Stampante
        self.lbl_stampante = tk.Label(self.lblfrm_stampante,
                                      text='Stampante')
        self.lbl_stampante_value = tk.Label(self.lblfrm_stampante, textvariable=self.stampante_value)
        self.cmb_box_stampante = ttk.Combobox(self.lblfrm_stampante,
                                              textvariable=self.stampante_value,
                                              state='read only')
        self.btn_salva_stampante = ttk.Button(self.lblfrm_stampante, image=self.img_btn, command=self.salva_stampante)

        lista_stampanti = [printer[2] for printer in win32print.EnumPrinters(2)]
        self.cmb_box_stampante['values'] = lista_stampanti

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

        self.lblfrm_winswgx.grid(row=1, column=0, sticky='we')
        self.lbl_dir_name.grid(row=0, column=0)
        self.lbl_win_loc_value.grid(row=0, column=1, padx=15)

        self.lblfrm_facebook.grid(row=2, column=0, sticky='we')
        self.lbl_token_fb.grid(row=1, column=0)
        self.lbl_token_fb_value.grid(row=1, column=1)
        self.lbl_scad_token.grid(row=2, column=0)
        self.lbl_scad_token_value.grid(row=2, column=1)

        self.lblfrm_stampante.grid(row=3, column=0, sticky='we')
        self.lbl_stampante.grid(row=1, column=0)
        self.lbl_stampante_value.grid(row=1, column=1)
        self.cmb_box_stampante.grid(row=1, column=2)
        self.btn_salva_stampante.grid(row=1, column=3, padx=5)

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
        
    def controlla_token(self):
        if self.config['Facebook']['token']:
            return 'Impostato'
        else:
            return 'Non Impostato'

    def salva_stampante(self):
        scelta = self.stampante_value.get()
        cfg_file = open('config.ini', 'w')
        self.config.set('Stampante', 'stampa', scelta)
        self.config.write(cfg_file)


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Impostazioni(notebook)
    notebook.add(new, text='Impostazioni')
    root.mainloop()
