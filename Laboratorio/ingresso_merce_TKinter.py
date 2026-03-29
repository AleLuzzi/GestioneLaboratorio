import tkinter as tk
from tkinter import ttk

from datepicker import Datepicker
from theme import COLORS, get_font


def setup_window(window):
    """Configura finestra principale del modulo Ingresso Merce."""
    window.configure(bg=COLORS["bg_light"])
    window.geometry("+125+125")
    window.title("Ingresso Merce")


def build_ui(app):
    """
    Costruisce tutta la UI per IngressoMerce.
    Richiede che l'istanza `app` abbia gia' inizializzato dati e variabili.
    """
    app.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")
    app.img_btn = tk.PhotoImage(file=".//immagini//modifica.gif")

    # LAYOUT dei frame per impaginazione
    app.frame_alto = tk.Frame(app, bd=0, bg=COLORS["bg_light"], padx=8, pady=8)
    app.frame_centrale = tk.Frame(app, bd=0, bg=COLORS["bg_light"], padx=8, pady=8)
    app.frame_basso = tk.Frame(app, bd=0, bg=COLORS["bg_light"], padx=8, pady=8)

    # TREEVIEW per riepilogo inserimenti
    app.tree = ttk.Treeview(app.frame_alto, height=8)
    app.tree["columns"] = (
        "prog_acq",
        "data",
        "num_ddt",
        "fornitore",
        "taglio",
        "peso_i",
        "peso_f",
        "lotto_chiuso",
        "id_merc",
    )
    app.tree["displaycolumns"] = ("data", "fornitore", "taglio", "peso_i")
    app.tree["show"] = "headings"
    app.tree.column("data", width=100)
    app.tree.column("fornitore", width=100)
    app.tree.column("taglio", width=100)
    app.tree.column("peso_i", width=100)
    app.tree.heading("data", text="Data")
    app.tree.heading("fornitore", text="Fornitore")
    app.tree.heading("taglio", text="Prodotto")
    app.tree.heading("peso_i", text="Quantita")

    # LABELFRAME contiene bottoni per scelta fornitore
    app.labelframe_fornitori = tk.LabelFrame(
        app.frame_centrale,
        text="Fornitore",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )

    row, col = 1, 0
    for fornitore in app.lista_fornitori:
        if row % 6 == 0:
            col += 1
            row = 1
        tk.Radiobutton(
            app.labelframe_fornitori,
            text=str(fornitore).upper(),
            variable=app.fornitore,
            width=20,
            indicatoron=0,
            value=fornitore,
            font="Verdana",
        ).grid(row=row, column=col, sticky="w")
        row += 1

    # LABELFRAME contiene bottoni per i tagli
    app.labelframe_taglio = tk.LabelFrame(
        app.frame_centrale,
        text="Taglio",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.notebook = ttk.Notebook(app.labelframe_taglio)

    # TAB AGNELLO
    app.tab1 = tk.Frame(app.notebook)
    app.notebook.add(app.tab1, text="AGNELLO", state="disabled", compound="left", image=app.img_btn1)
    row, col = 1, 0
    for taglio in app.lst_agnello:
        if row % 10 == 0:
            col += 1
            row = 1
        tk.Radiobutton(
            app.tab1,
            text=taglio.upper(),
            indicatoron=0,
            variable=app.taglio_s,
            font="Verdana",
            width=20,
            value=taglio,
        ).grid(row=row, column=col)
        row += 1

    # TAB BOVINO
    app.tab2 = tk.Frame(app.notebook)
    app.notebook.add(app.tab2, text="BOVINO", state="disabled", compound="left", image=app.img_btn1)
    row, col = 1, 0
    for taglio in app.lst_bovino:
        if row % 10 == 0:
            col += 1
            row = 1
        tk.Radiobutton(
            app.tab2,
            text=taglio.upper(),
            indicatoron=0,
            variable=app.taglio_s,
            font="Verdana",
            width=20,
            value=taglio,
        ).grid(row=row, column=col)
        row += 1

    # TAB SUINO
    app.tab3 = tk.Frame(app.notebook)
    app.notebook.add(app.tab3, text="SUINO", compound="left", image=app.img_btn1)
    row, col = 1, 0
    for taglio in app.lst_suino:
        if row % 8 == 0:
            col += 1
            row = 1
        tk.Radiobutton(
            app.tab3,
            text=taglio.upper(),
            indicatoron=0,
            variable=app.taglio_s,
            font="Verdana",
            width=20,
            value=taglio,
        ).grid(row=row, column=col)
        row += 1

    # TAB VITELLO
    app.tab4 = tk.Frame(app.notebook)
    app.notebook.add(app.tab4, text="VITELLO", state="disabled", compound="left", image=app.img_btn1)
    row, col = 1, 0
    for taglio in app.lst_vitello:
        if row % 10 == 0:
            col += 1
            row = 1
        tk.Radiobutton(
            app.tab4,
            text=taglio.upper(),
            indicatoron=0,
            variable=app.taglio_s,
            font="Verdana",
            width=20,
            value=taglio,
        ).grid(row=row, column=col)
        row += 1

    # LABEL progressivo lotto
    app.label_lotto = tk.Label(
        app.frame_alto,
        text="PROGRESSIVO LOTTO",
        foreground="blue",
        font=("Verdana", 15),
    )
    app.label_prog_lotto = tk.Label(
        app.frame_alto,
        anchor="center",
        relief="ridge",
        bg="white",
        text=str(app.prog_lotto_acq) + "A",
        font=("Verdana", 15),
        padx=35,
    )

    # LABEL data ingresso + datepicker
    app.label_data_ingresso = tk.Label(
        app.frame_alto,
        text="DATA INGRESSO MERCE",
        foreground="blue",
        font=("Verdana", 15),
    )
    app.picker = Datepicker(app.frame_alto, datevar=app.data, dateformat="%d-%m-%Y")

    # ENTRY numero ddt/fattura
    app.label_num_ddt = tk.Label(
        app.frame_alto,
        text="NUMERO DDT/FATTURA",
        foreground="blue",
        font=("Verdana", 15),
    )
    app.num_ddt = tk.StringVar()
    app.entry_ddt = ttk.Entry(app.frame_alto, textvariable=app.num_ddt, width=25)
    app.btn_ins_num_ddt = ttk.Button(app.frame_alto, image=app.img_btn, command=app._ins_num_ddt)
    app.entry_ddt.focus()

    # ENTRY inserimento peso
    app.label_peso = tk.Label(
        app.frame_alto,
        text="INSERIMENTO PESO",
        foreground="blue",
        font=("Verdana", 15),
    )
    app.entry = tk.Entry(app.frame_alto, textvariable=app.peso, width=25)
    app.btn_ins_peso = ttk.Button(app.frame_alto, image=app.img_btn, command=app._ins_peso)

    # BOTTONI principali
    app.btn_invio = tk.Button(
        app.frame_basso,
        text="INVIO",
        font=("Verdana", 15),
        width=18,
        command=app._invio,
    )
    app.btn_salva_esci = tk.Button(
        app.frame_basso,
        text="SALVA ed ESCI",
        font=("Verdana", 15),
        width=18,
        command=app._salva_esci,
    )
    app.btn_chiudi_finestra = tk.Button(
        app.frame_basso,
        text="CHIUDI FINESTRA",
        font=("Verdana", 15),
        width=18,
        command=app._chiudi,
    )
    app.btn_rimuovi_riga = tk.Button(
        app.frame_alto,
        text="RIMUOVI RIGA",
        command=app._rimuovi_riga_selezionata,
    )

    # Posizionamento layout
    app.frame_alto.grid(row=0, column=1)
    app.frame_centrale.grid(row=1, column=1)
    app.frame_basso.grid(row=2, column=1, columnspan=2)

    app.tree.grid(row=1, column=3, rowspan=4, padx=10)
    app.labelframe_fornitori.grid(row=1, column=0, sticky="n")
    app.labelframe_taglio.grid(row=1, column=1)
    app.notebook.grid(row=1, column=0, columnspan=2, sticky="we")

    app.label_lotto.grid(row=1, column=0, sticky="w")
    app.label_prog_lotto.grid(row=1, column=1)
    app.label_data_ingresso.grid(row=2, column=0, sticky="w")
    app.picker.grid(row=2, column=1)

    app.label_num_ddt.grid(row=3, column=0, sticky="w")
    app.entry_ddt.grid(row=3, column=1)
    app.btn_ins_num_ddt.grid(row=3, column=2)

    app.label_peso.grid(row=4, column=0, sticky="w")
    app.entry.grid(row=4, column=1)
    app.btn_ins_peso.grid(row=4, column=2)

    app.btn_invio.grid(row=0, column=0, sticky="we")
    app.btn_salva_esci.grid(row=0, column=1, sticky="we")
    app.btn_chiudi_finestra.grid(row=0, column=2, sticky="we")
    app.btn_rimuovi_riga.grid(row=5, column=3, sticky="we")
