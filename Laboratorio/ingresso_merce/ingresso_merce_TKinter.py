import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import re

from datepicker import Datepicker
from theme import COLORS, get_font, FONT_FAMILY


def _ctk_image(path, size):
    """Carica un'immagine per widget CustomTkinter."""
    pil = Image.open(path)
    if pil.mode not in ("RGB", "RGBA"):
        pil = pil.convert("RGBA")
    return ctk.CTkImage(light_image=pil, dark_image=pil, size=size)


def _add_radio_grid(parent, items, variable, row_wrap, width=180):
    """Crea una griglia di CTkRadioButton con stile coerente."""
    radio_font = ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold")
    row, col = 1, 0
    for item in items:
        if row % row_wrap == 0:
            col += 1
            row = 1
        ctk.CTkRadioButton(
            parent,
            text=str(item).upper(),
            variable=variable,
            value=item,
            width=width,
            height=28,
            font=radio_font,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_dark"],
            radiobutton_width=18,
            radiobutton_height=18,
        ).grid(row=row, column=col, sticky="w", padx=2, pady=2)
        row += 1


def setup_window(window):
    """Configura finestra principale del modulo Ingresso Merce."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.geometry("+125+125")
    window.title("Ingresso Merce")


def build_ui(app):
    """
    Costruisce tutta la UI per IngressoMerce.
    Richiede che l'istanza `app` abbia gia' inizializzato dati e variabili.
    """
    app.img_btn1 = tk.PhotoImage(file=".//immagini//logo_piccolo.gif")
    app.img_btn = _ctk_image(".//immagini//modifica.gif", (18, 18))

    # LAYOUT dei frame per impaginazione
    app.frame_elenco = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

    app.frame_alto = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_toolbar = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

    # tree_elencoVIEW per riepilogo inserimenti
    app.tree_riepilogo = ttk.Treeview(app.frame_alto, height=8)
    app.tree_riepilogo["columns"] = (
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
    app.tree_riepilogo["displaycolumns"] = ("data", "fornitore", "taglio", "peso_i")
    app.tree_riepilogo["show"] = "headings"
    app.tree_riepilogo.column("data", width=100)
    app.tree_riepilogo.column("fornitore", width=100)
    app.tree_riepilogo.column("taglio", width=100)
    app.tree_riepilogo.column("peso_i", width=100)
    app.tree_riepilogo.heading("data", text="Data")
    app.tree_riepilogo.heading("fornitore", text="Fornitore")
    app.tree_riepilogo.heading("taglio", text="Prodotto")
    app.tree_riepilogo.heading("peso_i", text="Quantita")

    # Contenitore "Elenco" in stile CustomTkinter (come anag_dipendenti)
    app.labelframe_elenco = ctk.CTkFrame(
        app.frame_elenco,
        fg_color=COLORS["bg_content"],
        corner_radius=8,
    )

    # Titolo sezione
    app.lbl_titolo_elenco = ctk.CTkLabel(
        app.labelframe_elenco,
        text="Elenco",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        text_color=COLORS["text_dark"],
        anchor="w",
    )
    app.lbl_titolo_elenco.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 5))

    # Wrapper che ospita Treeview e si espande in altezza
    tree_wrap = ctk.CTkFrame(
        app.labelframe_elenco,
        fg_color="transparent",
        corner_radius=0,
    )
    tree_wrap.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
    tree_wrap.rowconfigure(0, weight=1)
    tree_wrap.columnconfigure(0, weight=1)

    app.tree_elenco = ttk.Treeview(tree_wrap, height=10, show="headings")

    # notebook_dettagli: contiene "dettagli fornitore" e "dettagli taglio"
    app.notebook_dettagli = ttk.Notebook(app.frame_dettagli)

    # TAB DETTAGLI DATI (primo tab)
    # Nota: su alcuni Tk/ttk la insert(0, ...) può fallire con "Slave index 0 out of bounds".
    # Quindi aggiungo e poi riordino i tab.
    app.tab_dettagli_dati = tk.Frame(app.notebook_dettagli)
    app.notebook_dettagli.add(app.tab_dettagli_dati, text="Dati")

    # TAB DETTAGLI FORNITORE
    app.tab_dettagli_fornitore = tk.Frame(app.notebook_dettagli)
    app.notebook_dettagli.add(app.tab_dettagli_fornitore, text="Fornitore")

    # TAB DETTAGLI TAGLIO
    app.tab_dettagli_taglio = tk.Frame(app.notebook_dettagli)
    app.notebook_dettagli.add(app.tab_dettagli_taglio, text="Tagli / Prodotti")

    # Riordina: garantisce "Dati" come primo tab
    _tabs = app.notebook_dettagli.tabs()
    _tab_dati_id = str(app.tab_dettagli_dati)
    if _tab_dati_id in _tabs:
        app.notebook_dettagli.forget(app.tab_dettagli_dati)
        app.notebook_dettagli.insert(0, app.tab_dettagli_dati, text="Dati")

    # Forza selezione del tab "Dati" all'apertura finestra
    try:
        app.notebook_dettagli.select(app.tab_dettagli_dati)
        app.notebook_dettagli.update_idletasks()
    except Exception:
        # Alcuni Tk/ttk possono avere differenze di comportamento in base alla versione
        pass

    # Colonne visibili:
    # - nr_lotto, fornitore, data
    #
    # Colonne "nascoste" (servono per ricostruire la chiave composta in _onsingleclick):
    # - num_ddt, taglio, peso_i, peso_f, lotto_chiuso, id_merc, prog_acq
    app.tree_elenco["columns"] = (
        "nr_lotto",
        "fornitore",
        "data",
        "prog_acq",
        "num_ddt",
        "taglio",
        "peso_i",
        "peso_f",
        "lotto_chiuso",
        "id_merc",
    )

    # Headings visibili
    app.tree_elenco.heading("nr_lotto", text="nr Lotto")
    app.tree_elenco.heading("fornitore", text="Fornitore")
    app.tree_elenco.heading("data", text="Data")

    # Headings invisibili
    app.tree_elenco.heading("prog_acq", text="")
    app.tree_elenco.heading("num_ddt", text="")
    app.tree_elenco.heading("taglio", text="")
    app.tree_elenco.heading("peso_i", text="")
    app.tree_elenco.heading("peso_f", text="")
    app.tree_elenco.heading("lotto_chiuso", text="")
    app.tree_elenco.heading("id_merc", text="")

    # Larghezze visibili
    app.tree_elenco.column("nr_lotto", width=90, anchor="center")
    app.tree_elenco.column("fornitore", width=120, anchor="w")
    app.tree_elenco.column("data", width=110, anchor="center")

    # Larghezze invisibili
    for _col in ("prog_acq", "num_ddt", "taglio", "peso_i", "peso_f", "lotto_chiuso", "id_merc"):
        app.tree_elenco.column(_col, width=0, minwidth=0, stretch=False, anchor="center")

    app.tree_elenco.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    app.labelframe_elenco.rowconfigure(1, weight=1)
    app.labelframe_elenco.columnconfigure(0, weight=1)

    app.labelframe_fornitori = tk.LabelFrame(
        app.tab_dettagli_fornitore,
        text="Selezione Fornitore",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )

    _add_radio_grid(app.labelframe_fornitori, app.lista_fornitori, app.fornitore, row_wrap=6, width=200)

    # Posizionamento labelframe fornitore dentro la sua tab
    app.labelframe_fornitori.grid(row=0, column=0, sticky="nsew")
    app.tab_dettagli_fornitore.rowconfigure(0, weight=1)
    app.tab_dettagli_fornitore.columnconfigure(0, weight=1)

    # LABELFRAME contiene bottoni per i tagli (dentro tab dettagli taglio)
    app.labelframe_taglio = tk.LabelFrame(
        app.tab_dettagli_taglio,
        text="Selezione Taglio / Prodotto",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.notebook_tagli = ttk.Notebook(app.labelframe_taglio)

    # TAB AGNELLO
    app.tab1 = tk.Frame(app.notebook_tagli)
    app.notebook_tagli.add(app.tab1, text="AGNELLO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab1, app.lst_agnello, app.taglio_s, row_wrap=10)

    # TAB BOVINO
    app.tab2 = tk.Frame(app.notebook_tagli)
    app.notebook_tagli.add(app.tab2, text="BOVINO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab2, app.lst_bovino, app.taglio_s, row_wrap=10)

    # TAB SUINO
    app.tab3 = tk.Frame(app.notebook_tagli)
    app.notebook_tagli.add(app.tab3, text="SUINO", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab3, app.lst_suino, app.taglio_s, row_wrap=8)

    # TAB VITELLO
    app.tab4 = tk.Frame(app.notebook_tagli)
    app.notebook_tagli.add(app.tab4, text="VITELLO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab4, app.lst_vitello, app.taglio_s, row_wrap=10)

    # Posizionamento notebook tagli dentro il labelframe_taglio
    app.labelframe_taglio.grid(row=0, column=0, sticky="nsew")
    app.tab_dettagli_taglio.rowconfigure(0, weight=1)
    app.tab_dettagli_taglio.columnconfigure(0, weight=1)

    app.notebook_tagli.grid(row=0, column=0, sticky="we")

    # Layout tab "Dati"
    app.tab_dettagli_dati.rowconfigure(0, weight=0)
    app.tab_dettagli_dati.rowconfigure(1, weight=0)
    app.tab_dettagli_dati.rowconfigure(2, weight=0)
    app.tab_dettagli_dati.rowconfigure(3, weight=0)
    app.tab_dettagli_dati.columnconfigure(0, weight=1)
    app.tab_dettagli_dati.columnconfigure(1, weight=0)

    # LABEL progressivo lotto (nel tab "Dati")
    # NOTE: le label/widget "Dati" (data/nddT/peso) devono essere parented e gridate nella stessa tab.
    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    value_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    app.label_lotto = ctk.CTkLabel(
        app.tab_dettagli_dati,
        text="PROGRESSIVO LOTTO",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.label_prog_lotto = ctk.CTkLabel(
        app.tab_dettagli_dati,
        text=str(app.prog_lotto_acq) + "A",
        font=value_font,
        fg_color=COLORS["bg_content"],
        corner_radius=8,
        width=120,
        height=36,
    )

    # LABEL data ingresso + data_picker (nel tab "Dati")
    app.label_data_ingresso = ctk.CTkLabel(
        app.tab_dettagli_dati,
        text="DATA INGRESSO MERCE",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.data_picker = Datepicker(app.tab_dettagli_dati, datevar=app.data, dateformat="%d-%m-%Y")

    # ENTRY numero ddt/fattura (nel tab "Dati")
    app.label_num_ddt = ctk.CTkLabel(
        app.tab_dettagli_dati,
        text="NUMERO DDT/FATTURA",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.num_ddt = tk.StringVar()
    app.entry_ddt = ctk.CTkEntry(app.tab_dettagli_dati, textvariable=app.num_ddt, width=220, height=34)
    app.btn_ins_num_ddt = ctk.CTkButton(
        app.tab_dettagli_dati,
        text="",
        image=app.img_btn,
        width=36,
        height=34,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._ins_num_ddt,
    )
    app.entry_ddt.focus()

    # ENTRY inserimento peso (nel tab "Dati")
    app.label_peso = ctk.CTkLabel(
        app.tab_dettagli_dati,
        text="INSERIMENTO PESO",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.entry = ctk.CTkEntry(app.tab_dettagli_dati, textvariable=app.peso, width=220, height=34)

    def _normalize_and_validate_peso_on_focus_out(_event=None):
        """
        Normalizza separatore decimale e valida solo quando la entry perde il focus.
        Formati validi: 12 oppure 12,3 oppure 12,34.
        """
        current_value = app.peso.get().strip()
        normalized_value = current_value.replace(".", ",").rstrip(",")

        if normalized_value == "":
            app.peso.set("")
            return

        if re.fullmatch(r"\d+(,\d{1,2})?", normalized_value):
            app.peso.set(normalized_value)
        else:
            app.peso.set("")

    app.entry.bind("<FocusOut>", _normalize_and_validate_peso_on_focus_out)
    app.btn_ins_peso = ctk.CTkButton(
        app.tab_dettagli_dati,
        text="",
        image=app.img_btn,
        width=36,
        height=34,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._ins_peso,
    )

    # BOTTONI principali
    app.btn_aggiungi_riga = ctk.CTkButton(
        app.frame_alto,
        text="AGGIUNGI RIGA",
        #font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=32,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._aggiungi_riga,
    )
    app.btn_rimuovi_riga = ctk.CTkButton(
        app.frame_alto,
        text="RIMUOVI RIGA",
        height=32,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app._rimuovi_riga,
    )
    
    app.btn_nuovo = ctk.CTkButton(
        app.frame_toolbar,
        text="NUOVO",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._nuovo,
    )
    app.btn_modifica = ctk.CTkButton(
        app.frame_toolbar,
        text="MODIFICA",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._modifica,
    )
    app.btn_salva = ctk.CTkButton(
        app.frame_toolbar,
        text="SALVA",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._salva,
        state="disabled",
    )
    app.btn_annulla = ctk.CTkButton(
        app.frame_toolbar,
        text="ANNULLA",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["accent"],
        hover_color="#a93226",
        command=app._annulla,
        state="disabled",
    )
    app.btn_chiudi_finestra = ctk.CTkButton(
        app.frame_toolbar,
        text="CHIUDI",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app._chiudi,
        state="disabled",
    )
    

    # Posizionamento layout
    # (configurazioni per permettere espansione contenuti nella colonna centrale)
    # Configurazione righe/colonne del contenitore principale (root app)
    app.rowconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=0)  # elenco
    app.columnconfigure(1, weight=1)  # dettagli/alto
    app.columnconfigure(2, weight=0)  # riepilogo/toolbar

    app.frame_dettagli.rowconfigure(0, weight=1)
    app.frame_dettagli.columnconfigure(0, weight=0)
    app.frame_dettagli.columnconfigure(1, weight=1)

    app.frame_alto.grid(row=0, column=1, padx=8, pady=6, sticky="we")
    app.frame_dettagli.grid(row=1, column=1, padx=8, pady=6, sticky="we")

    # Toolbar a partire dalla colonna 1: lasciamo la colonna 2 libera per il riepilogo
    app.frame_toolbar.grid(row=2, column=1, columnspan=1, padx=8, pady=6, sticky="we")

    app.tree_riepilogo.grid(row=0, column=0, rowspan=2, padx=10)
    app.frame_elenco.grid(row=0, column=0, rowspan=2, padx=8, pady=6, sticky="nswe")
    app.labelframe_elenco.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    app.notebook_dettagli.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    # Nel tab "Dati"
    app.label_lotto.grid(row=1, column=0, sticky="w", padx=(0, 0), pady=(10, 0))
    app.label_prog_lotto.grid(row=1, column=1, sticky="w", padx=(0, 0), pady=(10, 0))
    app.label_data_ingresso.grid(row=2, column=0, sticky="w")
    app.data_picker.grid(row=2, column=1)

    app.label_num_ddt.grid(row=3, column=0, sticky="w")
    app.entry_ddt.grid(row=3, column=1)
    app.btn_ins_num_ddt.grid(row=3, column=2)

    app.label_peso.grid(row=4, column=0, sticky="w")
    app.entry.grid(row=4, column=1)
    app.btn_ins_peso.grid(row=4, column=2)

    app.btn_aggiungi_riga.grid(row=0, column=1, sticky="we")
    app.btn_rimuovi_riga.grid(row=1, column=1, sticky="we")
      
    app.btn_nuovo.grid(row=0, column=0, sticky="we", padx=(0, 6))
    app.btn_modifica.grid(row=0, column=1, sticky="we")
    app.btn_salva.grid(row=0, column=2, sticky="we")
    app.btn_annulla.grid(row=0, column=3, sticky="we", padx=(6, 6))
    app.btn_chiudi_finestra.grid(row=0, column=4, sticky="we")
  
