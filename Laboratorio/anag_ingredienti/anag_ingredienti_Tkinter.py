
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import customtkinter as ctk

from theme import COLORS, FONT_FAMILY, get_font


def setup_window(window):
    """Configura finestra principale anagrafica ingredienti."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.title("Anagrafica Ingredienti")
    window.geometry("+80+80")
    window.minsize(720, 420)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)


def build_ui(app):
    """Costruisce layout e widget; richiede connessione/cursor gia' su `app`."""

    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    label_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
    body_font = ctk.CTkFont(family=FONT_FAMILY, size=12)
    btn_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")

    app.frame_root = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_root.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    app.frame_root.columnconfigure(0, weight=2)
    app.frame_root.columnconfigure(1, weight=1)
    app.frame_root.columnconfigure(2, weight=0)

    app.frame_root.rowconfigure(0, weight=0)
    app.frame_root.rowconfigure(1, weight=1)

    app.lbl_titolo = ctk.CTkLabel(
        app.frame_root,
        text="ANAGRAFICA INGREDIENTI",
        font=title_font,
        text_color=COLORS["accent_hover"],
    )
    app.lbl_titolo.grid(row=0, column=0, columnspan=3, sticky="w", padx=4, pady=(0, 8))

    app.frame_elenco = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli.grid_columnconfigure(0, weight=1)
    app.frame_dettagli.grid_columnconfigure(1, weight=1)
    app.frame_dettagli.grid_rowconfigure(0, weight=1)
    app.frame_toolbar = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)

    app.frame_elenco.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8), pady=0)
    app.frame_toolbar.grid(row=0, column=1, sticky="new", padx=(8, 0), pady=(0, 12))
    app.frame_dettagli.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=0)

    app.frame_elenco.rowconfigure(0, weight=1)
    app.frame_elenco.columnconfigure(0, weight=1)

    app.label_frame_elenco = ctk.CTkFrame(app.frame_elenco, fg_color=COLORS["bg_content"], corner_radius=8)
    app.label_frame_elenco.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    app.label_frame_elenco.rowconfigure(2, weight=1)
    app.label_frame_elenco.columnconfigure(0, weight=1)

    titolo_elenco = ctk.CTkLabel(
        app.label_frame_elenco,
        text="Elenco",
        font=ctk.CTkFont(size=14, weight="bold"),
        anchor="w",
    )
    titolo_elenco.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 5))

    app.frame_ricerca_sub = ctk.CTkFrame(app.label_frame_elenco, fg_color="transparent")
    app.frame_ricerca_sub.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
    app.frame_ricerca_sub.columnconfigure(0, weight=1)
    app.frame_ricerca_sub.columnconfigure(1, weight=0)

    app.entry_filtro = ctk.CTkEntry(
        app.frame_ricerca_sub,
        placeholder_text="Cerca ingrediente...",
    )
    app.entry_filtro.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=0)
    app.entry_filtro.bind("<KeyRelease>", app._filtra_ingrediente)

    app.btn_reset_filtro = ctk.CTkButton(
        app.frame_ricerca_sub,
        text="✕",
        width=30,
        height=28,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=COLORS["border"],
        hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_dark"],
        command=app._reset_ricerca,
    )
    app.btn_reset_filtro.grid(row=0, column=1, sticky="e", padx=0, pady=0)

    tree_wrap = ctk.CTkFrame(app.label_frame_elenco, fg_color=COLORS["bg_content"], corner_radius=0)
    tree_wrap.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
    tree_wrap.rowconfigure(0, weight=1)
    tree_wrap.columnconfigure(0, weight=1)

    app.tree_ingredienti = ttk.Treeview(tree_wrap, height=18)
    app.tree_ingredienti["columns"] = ("Id", "Ingrediente", "cod_ean", "merceologia")
    app.tree_ingredienti["show"] = "headings"
    app.tree_ingredienti.heading("Id", text="Id")
    app.tree_ingredienti.heading("Ingrediente", text="Ingrediente")
    app.tree_ingredienti.heading("cod_ean", text="cod EAN")
    app.tree_ingredienti.heading("merceologia", text='Merceologia')
    app.tree_ingredienti.column("Id", width=30)
    app.tree_ingredienti.column("Ingrediente", width=150)
    app.tree_ingredienti.column("cod_ean", width=100)
    app.tree_ingredienti.column("merceologia", width=100)
    app.tree_ingredienti.bind("<<TreeviewSelect>>", app._onsingleclick)
    app.tree_ingredienti.bind("<Double-1>", app._onsingleclick)
    app.tree_ingredienti.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    
    app.lbl_frame_dettagli_selezionato = tk.LabelFrame(
        app.frame_dettagli,
        text="Dettagli ingrediente selezionato",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
  
    app.lbl_frame_dettagli_selezionato.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 8))
    
    app.lbl_ingrediente = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="Ingrediente",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    
    app.lbl_ingrediente.grid(row=0, column=0, padx=8, pady=8, sticky="w")

    app.ent_ingrediente = ctk.CTkEntry(
        app.lbl_frame_dettagli_selezionato,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ent_ingrediente.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    
    app.lbl_frame_dettagli_selezionato.columnconfigure(1, weight=1)

    app.lbl_cod_ean = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="cod EAN",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_cod_ean.grid(row=2, column=0, padx=8, pady=8, sticky="w")

    app.ent_cod_ean = ctk.CTkEntry(
        app.lbl_frame_dettagli_selezionato,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ent_cod_ean.grid(row=2, column=1, padx=8, pady=8, sticky="ew")

    app.lbl_merceologia = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="Merceologia",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_merceologia.grid(row=3, column=0, padx=8, pady=8, sticky="w")

    # Merceologia: combobox (coerente con `anagrafica_ingredienti.py`)
    app.box_merceologia = ttk.Combobox(
        app.lbl_frame_dettagli_selezionato,
        state="disabled",
        font=(FONT_FAMILY, 12),
        values=[],
    )
    app.box_merceologia.grid(row=3, column=1, padx=8, pady=8, sticky="ew")

    # Compatibilità con controller: mantiene l'API `ent_merceologia.get()`
    app.ent_merceologia = app.box_merceologia


    app.lbl_frame_attributi_ingrediente = ctk.CTkFrame(
        app.frame_dettagli,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.lbl_frame_attributi_ingrediente.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=(0, 8))
    app.lbl_frame_attributi_ingrediente.columnconfigure(0, weight=1)

    app.lbl_titolo_attributi = ctk.CTkLabel(
        app.lbl_frame_attributi_ingrediente,
        text="Attributi ingrediente selezionato",
        font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
        text_color=COLORS["text_dark"],
    )
    app.lbl_titolo_attributi.grid(row=0, column=0, padx=8, pady=8, sticky="n")

    app.valori_flag_dip = tk.IntVar()
    app.valori_flag_prod = tk.IntVar()

    app.ckbtn_dip = ctk.CTkCheckBox(
        app.lbl_frame_attributi_ingrediente,
        text="Mostra nel tab dipendenti",
        variable=app.valori_flag_dip,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ckbtn_dip.grid(row=1, column=0, padx=8, pady=10, sticky="w")

    app.ckbtn_prod = ctk.CTkCheckBox(
        app.lbl_frame_attributi_ingrediente,
        text="Mostra nel tab produzione",
        variable=app.valori_flag_prod,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ckbtn_prod.grid(row=2, column=0, padx=8, pady=10, sticky="w")

    app.lbl_frame_scegli = ctk.CTkFrame(
        app.frame_toolbar,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.lbl_frame_scegli.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

    for col in range(5):
        app.lbl_frame_scegli.columnconfigure(col, weight=1)

    app.btn_nuovo = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Nuovo",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._nuovo,
    )

    app.btn_modifica = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Modifica",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._modifica,
    )

    app.btn_salva = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Salva",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        state="disabled",
        command=app._salva,
    )

    app.btn_annulla = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Annulla",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color="#a93226",
        state="disabled",
        command=app._annulla,
    )

    app.btn_elimina = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Elimina",
        font=btn_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color=COLORS["accent_hover"],
        state="disabled",
        command=app._elimina,
    )

    app.btn_nuovo.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
    app.btn_modifica.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    app.btn_salva.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
    app.btn_annulla.grid(row=0, column=3, padx=8, pady=8, sticky="ew")
    app.btn_elimina.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

    for col in range(5):
        app.lbl_frame_scegli.columnconfigure(col, weight=1)

    app._aggiorna()