import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import re

from theme import COLORS, FONT_FAMILY


def _ctk_image(path, size):
    """Carica un'immagine per widget CustomTkinter."""
    pil = Image.open(path)
    if pil.mode not in ("RGB", "RGBA"):
        pil = pil.convert("RGBA")
    return ctk.CTkImage(light_image=pil, dark_image=pil, size=size)


def _add_radio_grid(parent, items, variable, row_wrap, width=240):
    """Crea una griglia di CTkRadioButton con stile coerente."""
    radio_font = ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold")
    row, col = 0, 0
    for item in items:
        if row and row % row_wrap == 0:
            col += 1
            row = 0
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
    """Configura finestra principale del modulo Nuovo Lotto."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.geometry("+25+25")
    window.title("Nuovo Lotto")


def build_ui(app):
    """
    Costruisce tutta la UI per NuovoLotto.
    Richiede che `app` abbia gia' inizializzato variabili e dati.
    """
    app.img_btn = _ctk_image(".//immagini//modifica.gif", (18, 18))

    # DISPOSIZIONE FRAME
    app.frame_sx = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dx = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dx_r = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dx_basso = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

    # TREEVIEW per riepilogo immissioni
    app.tree = ttk.Treeview(app.frame_sx, height=20)
    app.tree["columns"] = ("data ingresso", "fornitore", "peso", "residuo")

    app.tree.column("data ingresso", width=80)
    app.tree.column("fornitore", width=80)
    app.tree.column("peso", width=80)
    app.tree.column("residuo", width=60)

    app.tree.heading("data ingresso", text="Data ingresso")
    app.tree.heading("fornitore", text="Fornitore")
    app.tree.heading("peso", text="Peso")
    app.tree.heading("residuo", text="Residuo")
    app.tree.tag_configure("odd", background=COLORS["bg_light"])
    app.tree.bind("<Double-1>", app.ondoubleclick)

    # LABEL nuovo lotto vendita
    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    value_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    app.lbl_nuovo_lotto = ctk.CTkLabel(
        app.frame_dx,
        text="NUOVO LOTTO VENDITA",
        font=title_font,
        text_color=COLORS["accent_hover"],
    )
    app.lbl_prog_lotto_vendita = ctk.CTkLabel(
        app.frame_dx,
        text=str(app.prog_lotto_ven) + "V",
        font=value_font,
        fg_color=COLORS["bg_content"],
        text_color=COLORS["text_dark"],
        corner_radius=8,
        width=120,
        height=36,
    )

    # LABEL quantita' prodotta
    app.lbl_qta_prodotto = ctk.CTkLabel(
        app.frame_dx,
        text="QUANTITA PRODOTTA",
        font=title_font,
        text_color=COLORS["accent_hover"],
    )

    # TREEVIEW per lotti selezionati
    app.tree_lotti_selezionati = ttk.Treeview(app.frame_dx_r, height=6)
    app.tree_lotti_selezionati["columns"] = (
        "progressivo_v",
        "data",
        "lotto ingresso",
        "nuova_produzione",
        "peso",
        "taglio",
    )
    app.tree_lotti_selezionati["displaycolumns"] = ("lotto ingresso", "taglio")
    app.tree_lotti_selezionati["show"] = "headings"
    app.tree_lotti_selezionati.column("lotto ingresso", width=100)
    app.tree_lotti_selezionati.column("taglio", width=100)
    app.tree_lotti_selezionati.heading("lotto ingresso", text="Lotto ingresso")
    app.tree_lotti_selezionati.heading("taglio", text="Taglio")

    # LABELFRAME nuova produzione
    app.lbl_nuova_produzione = ctk.CTkLabel(
        app.frame_dx_basso,
        text="SELEZIONE NUOVA PRODUZIONE",
        font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        text_color=COLORS["accent_hover"],
    )
    app.labelframe = ctk.CTkFrame(
        app.frame_dx_basso,
        fg_color=COLORS["bg_content"],
        corner_radius=8,
        border_width=1,
        border_color=COLORS["border"],
    )

    # ENTRY per inserimento del peso
    app.entry_peso = ctk.CTkEntry(app.frame_dx, width=220, height=34, textvariable=app.peso_da_inserire)
    app.entry_peso.focus()
    def _normalize_and_validate_peso_on_focus_out(_event=None):
        """
        Normalizza separatore decimale e valida solo quando la entry perde il focus.
        Formati validi: 12 oppure 12,3 oppure 12,34.
        """
        current_value = app.peso_da_inserire.get().strip()
        normalized_value = current_value.replace(".", ",").rstrip(",")

        # Campo vuoto consentito.
        if normalized_value == "":
            app.peso_da_inserire.set("")
            return

        if re.fullmatch(r"\d+(,\d{1,2})?", normalized_value):
            app.peso_da_inserire.set(normalized_value)
        else:
            # Valore non valido: pulizia campo.
            app.peso_da_inserire.set("")

    app.entry_peso.bind("<FocusOut>", _normalize_and_validate_peso_on_focus_out)
    app.btn_ins_qta_prodotto = ctk.CTkButton(
        app.frame_dx,
        text="",
        image=app.img_btn,
        width=36,
        height=34,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._ins_peso,
    )

    # BOTTONI azioni
    action_font = ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold")
    app.btn_elimina_riga = ctk.CTkButton(
        app.frame_dx_r,
        text="RIMUOVI RIGA",
        font=action_font,
        height=32,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app.rimuovi_riga_selezionata,
    )
    app.btn_esci = ctk.CTkButton(
        app.frame_sx,
        text="CHIUDI FINESTRA",
        font=action_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app.esci_senza_salvare,
    )
    app.btn_esci_salva = ctk.CTkButton(
        app.frame_sx,
        text="SALVA ed ESCI",
        font=action_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app.esci_salva,
    )

    # LAYOUT
    app.frame_sx.grid(row=0, column=0, rowspan=2, padx=8, pady=6, sticky="we")
    app.frame_dx.grid(row=0, column=1, padx=8, pady=6, sticky="we")
    app.frame_dx_r.grid(row=0, column=2, padx=8, pady=6, sticky="we")
    # Area "Nuova produzione" sotto i pannelli centrali/destro per evitare sovrapposizioni.
    app.frame_dx_basso.grid(row=1, column=1, columnspan=2, padx=8, pady=(0, 6), sticky="new")

    app.tree.grid(row=0, column=0, columnspan=2, padx=10)
    app.btn_esci.grid(row=1, column=0, sticky="we")
    app.btn_esci_salva.grid(row=1, column=1, sticky="we")

    app.lbl_nuovo_lotto.grid(row=0, column=0, sticky="we")
    app.lbl_prog_lotto_vendita.grid(row=1, column=0, sticky="w")
    app.lbl_qta_prodotto.grid(row=2, column=0, sticky="we")
    app.entry_peso.grid(row=3, column=0, sticky="w")
    app.btn_ins_qta_prodotto.grid(row=3, column=1)

    app.tree_lotti_selezionati.grid(row=0, column=0, sticky="we", padx=10)
    app.btn_elimina_riga.grid(row=1, column=0, sticky="we")

    app.lbl_nuova_produzione.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 4))
    app.labelframe.grid(row=3, column=0, columnspan=2, sticky="we")


def populate_produzione_radio(app):
    """Popola la sezione nuova produzione con radiobutton CustomTkinter."""
    for child in app.labelframe.winfo_children():
        child.destroy()
    _add_radio_grid(app.labelframe, app.lista_nuova_produzione, app.nuova_produzione, row_wrap=8, width=260)
