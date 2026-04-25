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
    app.frame_alto = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_centrale = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_basso_azioni = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

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
        text="Selezione Fornitore",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )

    _add_radio_grid(app.labelframe_fornitori, app.lista_fornitori, app.fornitore, row_wrap=6, width=200)

    # LABELFRAME contiene bottoni per i tagli
    app.labelframe_taglio = tk.LabelFrame(
        app.frame_centrale,
        text="Selezione Taglio / Prodotto",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.notebook = ttk.Notebook(app.labelframe_taglio)

    # TAB AGNELLO
    app.tab1 = tk.Frame(app.notebook)
    app.notebook.add(app.tab1, text="AGNELLO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab1, app.lst_agnello, app.taglio_s, row_wrap=10)

    # TAB BOVINO
    app.tab2 = tk.Frame(app.notebook)
    app.notebook.add(app.tab2, text="BOVINO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab2, app.lst_bovino, app.taglio_s, row_wrap=10)

    # TAB SUINO
    app.tab3 = tk.Frame(app.notebook)
    app.notebook.add(app.tab3, text="SUINO", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab3, app.lst_suino, app.taglio_s, row_wrap=8)

    # TAB VITELLO
    app.tab4 = tk.Frame(app.notebook)
    app.notebook.add(app.tab4, text="VITELLO", state="disabled", compound="left", image=app.img_btn1)
    _add_radio_grid(app.tab4, app.lst_vitello, app.taglio_s, row_wrap=10)

    # LABEL progressivo lotto
    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    value_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    app.label_lotto = ctk.CTkLabel(
        app.frame_alto,
        text="PROGRESSIVO LOTTO",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.label_prog_lotto = ctk.CTkLabel(
        app.frame_alto,
        text=str(app.prog_lotto_acq) + "A",
        font=value_font,
        fg_color=COLORS["bg_content"],
        corner_radius=8,
        width=120,
        height=36,
    )

    # LABEL data ingresso + datepicker
    app.label_data_ingresso = ctk.CTkLabel(
        app.frame_alto,
        text="DATA INGRESSO MERCE",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.picker = Datepicker(app.frame_alto, datevar=app.data, dateformat="%d-%m-%Y")

    # ENTRY numero ddt/fattura
    app.label_num_ddt = ctk.CTkLabel(
        app.frame_alto,
        text="NUMERO DDT/FATTURA",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.num_ddt = tk.StringVar()
    app.entry_ddt = ctk.CTkEntry(app.frame_alto, textvariable=app.num_ddt, width=220, height=34)
    app.btn_ins_num_ddt = ctk.CTkButton(
        app.frame_alto,
        text="",
        image=app.img_btn,
        width=36,
        height=34,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._ins_num_ddt,
    )
    app.entry_ddt.focus()

    # ENTRY inserimento peso
    app.label_peso = ctk.CTkLabel(
        app.frame_alto,
        text="INSERIMENTO PESO",
        text_color=COLORS["accent_hover"],
        font=title_font,
    )
    app.entry = ctk.CTkEntry(app.frame_alto, textvariable=app.peso, width=220, height=34)
    def _normalize_and_validate_peso_on_focus_out(_event=None):
        """
        Normalizza separatore decimale e valida solo quando la entry perde il focus.
        Formati validi: 12 oppure 12,3 oppure 12,34.
        """
        current_value = app.peso.get().strip()
        normalized_value = current_value.replace(".", ",").rstrip(",")

        # Campo vuoto consentito.
        if normalized_value == "":
            app.peso.set("")
            return

        if re.fullmatch(r"\d+(,\d{1,2})?", normalized_value):
            app.peso.set(normalized_value)
        else:
            # Valore non valido: pulizia campo.
            app.peso.set("")

    app.entry.bind("<FocusOut>", _normalize_and_validate_peso_on_focus_out)
    app.btn_ins_peso = ctk.CTkButton(
        app.frame_alto,
        text="",
        image=app.img_btn,
        width=36,
        height=34,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._ins_peso,
    )

    # BOTTONI principali
    app.btn_invio = ctk.CTkButton(
        app.frame_basso_azioni,
        text="INVIO",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._invio,
    )
    app.btn_salva_esci = ctk.CTkButton(
        app.frame_basso_azioni,
        text="SALVA ed ESCI",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._salva_esci,
    )
    app.btn_chiudi_finestra = ctk.CTkButton(
        app.frame_basso_azioni,
        text="CHIUDI FINESTRA",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        height=38,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app._chiudi,
    )
    app.btn_rimuovi_riga = ctk.CTkButton(
        app.frame_alto,
        text="RIMUOVI RIGA",
        height=32,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app._rimuovi_riga_selezionata,
    )

    # Posizionamento layout
    app.frame_alto.grid(row=0, column=1, padx=8, pady=6, sticky="we")
    app.frame_centrale.grid(row=1, column=1, padx=8, pady=6, sticky="we")
    app.frame_basso_azioni.grid(row=2, column=1, columnspan=2, padx=8, pady=6, sticky="we")

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
