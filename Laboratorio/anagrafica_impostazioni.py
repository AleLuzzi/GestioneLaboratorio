import datetime
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# Gestione dinamica e sicura delle librerie Windows
if platform.system() == "Windows":
    try:
        import win32print
    except ImportError:
        win32print = None
else:
    win32print = None

# Import dei moduli personalizzati dell'applicazione
from config import get_config, save_config
from theme import COLORS, get_font
from datepicker import Datepicker


class Impostazioni(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg=COLORS["bg_light"])
        self.config = get_config()
        self.token_fb_status = self.controlla_token()

        # Gestione percorsi cross-platform con pathlib (evita problemi con / e \)
        percorso_icona = Path("immagini") / "Save-icon.gif"
        self.img_btn = tk.PhotoImage(file=str(percorso_icona))

        # STRINGVAR (Variabili di controllo per la GUI)
        self.win_dir = tk.StringVar()
        self.win_dir.set(self.config['Winswgx']['dir'])
        self.stampante_value = tk.StringVar()
        self.stampante_value.set(self.config['Stampante']['stampa'])
        self.data = tk.StringVar()
        self.data.set(self.config['Modulo_lotti_vendita']['data_dal'])

        # FRAME PRINCIPALI
        self.frame_sx = tk.Frame(self, bg=COLORS["bg_light"], padx=8, pady=8)
        self.frame_centrale = tk.Frame(self, bg=COLORS["bg_light"], padx=8, pady=8)
        self.frame_dx = tk.Frame(self, bg=COLORS["bg_light"], padx=8, pady=8)

        # CONFIGURAZIONE UNIFORME DEI LABELFRAME (Stile grafico coerente)
        lf_opts = dict(font=get_font(12, bold=True), fg=COLORS["text_dark"], bg=COLORS["bg_light"])

        # CREAZIONE LABELFRAME
        self.lblfrm_imp_database = tk.LabelFrame(self.frame_sx, text='DataBase', **lf_opts)
        self.lblfrm_winswgx = tk.LabelFrame(self.frame_sx, text='Winswgx-net', **lf_opts)
        self.lblfrm_facebook = tk.LabelFrame(self.frame_sx, text='Facebook', **lf_opts)
        self.lblfrm_stampante = tk.LabelFrame(self.frame_sx, text='Stampante', **lf_opts)
        self.lblfrm_lotti_vendita_carne = tk.LabelFrame(self.frame_sx, text='Modulo Lotti Vendita Carne', **lf_opts)

        # ELEMENTI: Modulo Lotti Vendita Carne
        self.lbl_visualizza_lotti = tk.Label(self.lblfrm_lotti_vendita_carne, text='Visualizza lotti dal ', bg=COLORS["bg_light"])
        self.picker_lot_vend_carne = Datepicker(self.lblfrm_lotti_vendita_carne, datevar=self.data, dateformat='%d-%m-%Y')
        self.btn_salva_data = ttk.Button(self.lblfrm_lotti_vendita_carne, image=self.img_btn, command=self._salva_data)

        # ELEMENTI: Database
        self.lbl_database = tk.Label(self.lblfrm_imp_database, text='Data Base', bg=COLORS["bg_light"])
        self.lbl_host = tk.Label(self.lblfrm_imp_database, text='Host', bg=COLORS["bg_light"])
        self.lbl_port = tk.Label(self.lblfrm_imp_database, text='Port', bg=COLORS["bg_light"])
        self.lbl_user = tk.Label(self.lblfrm_imp_database, text='User', bg=COLORS["bg_light"])
        self.lbl_pwd = tk.Label(self.lblfrm_imp_database, text='Password', bg=COLORS["bg_light"])

        self.lbl_database_value = tk.Label(self.lblfrm_imp_database, text=str(self.config['DataBase']['db']), bg=COLORS["bg_light"])
        self.lbl_host_value = tk.Label(self.lblfrm_imp_database, text=str(self.config['DataBase']['host']), bg=COLORS["bg_light"])
        self.lbl_port_value = tk.Label(self.lblfrm_imp_database, text=str(self.config['DataBase']['port']), bg=COLORS["bg_light"])
        self.lbl_user_value = tk.Label(self.lblfrm_imp_database, text=str(self.config['DataBase']['user']), bg=COLORS["bg_light"])
        self.lbl_pwd_value = tk.Label(self.lblfrm_imp_database, text=str(self.config['DataBase']['pwd']), bg=COLORS["bg_light"])

        # ELEMENTI: Winswgx-net
        self.lbl_dir_name = tk.Button(self.lblfrm_winswgx, text='Winswgx-Net Folder', command=self.open_dir)
        self.lbl_win_loc_value = tk.Label(self.lblfrm_winswgx, textvariable=self.win_dir, relief='sunken')

        # ELEMENTI: Facebook
        self.lbl_token_fb = tk.Label(self.lblfrm_facebook, text='Token Facebook', bg=COLORS["bg_light"])
        self.lbl_token_fb_value = tk.Label(self.lblfrm_facebook, text=self.token_fb_status, relief='sunken')
        self.lbl_scad_token = tk.Label(self.lblfrm_facebook, text='Scadenza Token', bg=COLORS["bg_light"])
        self.lbl_scad_token_value = tk.Label(self.lblfrm_facebook, text=str(self.config['Facebook']['scadenza']), relief='sunken')

        # ELEMENTI: Stampante
        self.lbl_stampante = tk.Label(self.lblfrm_stampante, text='Stampante', bg=COLORS["bg_light"])
        self.lbl_stampante_value = tk.Label(self.lblfrm_stampante, textvariable=self.stampante_value, bg=COLORS["bg_light"])
        self.cmb_box_stampante = ttk.Combobox(self.lblfrm_stampante, textvariable=self.stampante_value, state='readonly')
        self.btn_salva_stampante = ttk.Button(self.lblfrm_stampante, image=self.img_btn, command=self.salva_stampante)

        # Popolamento dinamico delle stampanti in base al sistema operativo
        self.cmb_box_stampante['values'] = self._ottieni_lista_stampanti()

        # DISPOSIZIONE LAYOUT SULLO SCHERMO (GRID)
        self.frame_sx.grid(row=0, column=0, sticky="nsew")

        # Posizionamento Sezione Database
        self.lblfrm_imp_database.grid(row=0, column=0, sticky='we', pady=5)
        self.lbl_database.grid(row=0, column=0, sticky="w", padx=5)
        self.lbl_database_value.grid(row=0, column=1, sticky="w", padx=5)
        self.lbl_host.grid(row=1, column=0, sticky="w", padx=5)
        self.lbl_host_value.grid(row=1, column=1, sticky="w", padx=5)
        self.lbl_port.grid(row=2, column=0, sticky="w", padx=5)
        self.lbl_port_value.grid(row=2, column=1, sticky="w", padx=5)
        self.lbl_user.grid(row=3, column=0, sticky="w", padx=5)
        self.lbl_user_value.grid(row=3, column=1, sticky="w", padx=5)
        self.lbl_pwd.grid(row=4, column=0, sticky="w", padx=5)
        self.lbl_pwd_value.grid(row=4, column=1, sticky="w", padx=5)

        # Posizionamento Sezione Winswgx
        self.lblfrm_winswgx.grid(row=1, column=0, sticky='we', pady=5)
        self.lbl_dir_name.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_win_loc_value.grid(row=0, column=1, padx=15, pady=5, sticky='we')

        # Posizionamento Sezione Facebook
        self.lblfrm_facebook.grid(row=2, column=0, sticky='we', pady=5)
        self.lbl_token_fb.grid(row=1, column=0, sticky="w", padx=5)
        self.lbl_token_fb_value.grid(row=1, column=1, sticky="w", padx=5)
        self.lbl_scad_token.grid(row=2, column=0, sticky="w", padx=5)
        self.lbl_scad_token_value.grid(row=2, column=1, sticky="w", padx=5)

        # Posizionamento Sezione Stampante
        self.lblfrm_stampante.grid(row=3, column=0, sticky='we', pady=5)
        self.lbl_stampante.grid(row=1, column=0, padx=5)
        self.lbl_stampante_value.grid(row=1, column=1, padx=5)
        self.cmb_box_stampante.grid(row=1, column=2, padx=5)
        self.btn_salva_stampante.grid(row=1, column=3, padx=5, pady=5)

        # Posizionamento Sezione Lotti Carne
        self.lblfrm_lotti_vendita_carne.grid(row=4, column=0, sticky='we', pady=5)
        self.lbl_visualizza_lotti.grid(row=1, column=0, padx=5)
        self.picker_lot_vend_carne.grid(row=1, column=1, padx=5)
        self.btn_salva_data.grid(row=1, column=2, padx=5, pady=5)

    def _ottieni_lista_stampanti(self):
        """Metodo privato per rilevare le stampanti su Windows, macOS e Linux."""
        os_name = platform.system()
        if os_name == "Windows" and win32print:
            try:
                return [printer[2] for printer in win32print.EnumPrinters(2)]
            except Exception:
                return ["Stampante Predefinita Windows"]
        elif os_name in ["Linux", "Darwin"]:  # Darwin = macOS
            try:
                # Utilizza il sottosistema universale CUPS standard POSIX
                risultato = subprocess.run(['lpstat', '-a'], capture_output=True, text=True, check=True)
                lista = []
                for linea in risultato.stdout.splitlines():
                    if linea.strip():
                        lista.append(linea.split()[0])  # Prende solo il nome univoco del dispositivo
                return lista if lista else ["Stampante Predefinita Unix"]
            except Exception:
                return ["Stampante Predefinita Unix"]
        return ["Nessuna stampante rilevata"]

    def open_dir(self):
        # Percorso di fallback cross-platform sicuro (Cartella utente di sistema)
        cartella_fallback = str(Path.home())
        
        # Corretto parent=self per evitare blocchi dell'interfaccia su Linux/macOS
        new_dirname = filedialog.askdirectory(parent=self, initialdir=cartella_fallback)
        
        if new_dirname:  # Impedisce di sovrascrivere la config se l'utente chiude la finestra senza scegliere
            self.config.set('Winswgx', 'dir', str(new_dirname))
            save_config()
            self.win_dir.set(new_dirname)
            messagebox.showinfo('Attenzione', 'Per vedere l\'impostazione correttamente\n'
                                              'riavvia l\'applicazione.')

    def controlla_token(self):
        # Controllo difensivo per evitare KeyError se la chiave non esiste nel file di configurazione
        if self.config.has_option('Facebook', 'token') and self.config['Facebook']['token']:
            return 'Impostato'
        return 'Non Impostato'

    def salva_stampante(self):
        scelta = self.stampante_value.get()
        self.config.set('Stampante', 'stampa', str(scelta))
        save_config()

    def _salva_data(self):
        scelta = self.data.get()
        print(f"Salvataggio data lotti: {scelta}")
        self.config.set('Modulo_lotti_vendita', 'data_dal', str(scelta))
        save_config()


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.grid(row='1', column='0')
    new = Impostazioni(notebook)
    notebook.add(new, text='Impostazioni')
    root.mainloop()
