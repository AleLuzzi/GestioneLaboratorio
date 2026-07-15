import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from theme import COLORS, FONT_FAMILY


def build_ui(app):
    """Costruisce la UI merceologie (grafica) usando CustomTkinter.

    Compatibile con il controller `anag_merceologie_controller.py`.

    Richiede che `app` sia un controller con attributi/metodi:
      - tree_merceologie: Treeview
      - ent_merceologia: Entry (con .get/.delete/.insert)
      - cmb_box_reparto_value / cmb_box_reparto: Combobox
      - valore_flag (dict) e ckbutton (dict) e ATTRIBUTI (list di label)
      - btn_modifica / btn_inserisci: bottoni command al controller
      - _aggiorna e _ondoubleclick già definiti sul controller
      - _disabilita_campi (opzionale)
    """

    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    label_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
    body_font = ctk.CTkFont(family=FONT_FAMILY, size=12)
    btn_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")

    # Root frame
    app.frame_root = ctk.CTkFrame(
        app,
        fg_color=COLORS["bg_light"],
        corner_radius=0,
    )
    app.frame_root.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    app.frame_root.columnconfigure(0, weight=2)
    app.frame_root.columnconfigure(1, weight=1)
    app.frame_root.columnconfigure(2, weight=0)
    app.frame_root.rowconfigure(0, weight=0)
    app.frame_root.rowconfigure(1, weight=1)

    app.lbl_titolo = ctk.CTkLabel(
        app.frame_root,
        text="ANAGRAFICA MERCEOLOGIE",
        font=title_font,
        text_color=COLORS["accent_hover"],
        anchor="w",
    )
    app.lbl_titolo.grid(row=0, column=0, columnspan=3, sticky="w", padx=4, pady=(0, 8))

    # Frame tre colonne
    app.frame_elenco = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)

    app.frame_dettagli = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_toolbar = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)

    app.frame_elenco.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=(0, 0))
    app.frame_dettagli.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=(0, 0))
    app.frame_toolbar.grid(row=1, column=2, sticky="new", padx=(8, 0), pady=(0, 0))

    app.frame_elenco.rowconfigure(0, weight=1)
    app.frame_elenco.columnconfigure(0, weight=1)

    # --- TREE ---
    tree_wrap = ctk.CTkFrame(app.frame_elenco, fg_color=COLORS["bg_content"], corner_radius=8)
    tree_wrap.grid(row=0, column=0, sticky="nsew")
    tree_wrap.rowconfigure(1, weight=1)
    tree_wrap.columnconfigure(0, weight=1)

    titolo_elenco = ctk.CTkLabel(
        tree_wrap,
        text="Elenco",
        font=ctk.CTkFont(size=14, weight="bold"),
        anchor="w",
        text_color=COLORS["text_dark"],
    )
    titolo_elenco.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 5))

    # Barra filtro (come anag_dipendenti)
    app.frame_ricerca_sub = ctk.CTkFrame(tree_wrap, fg_color="transparent")
    app.frame_ricerca_sub.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
    app.frame_ricerca_sub.columnconfigure(0, weight=1)
    app.frame_ricerca_sub.columnconfigure(1, weight=0)

    app.entry_filtro = ctk.CTkEntry(
        app.frame_ricerca_sub,
        placeholder_text="Cerca merceologia...",
    )
    app.entry_filtro.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=0)
    app.entry_filtro.bind("<KeyRelease>", app._filtra_merceologia)

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

    # Treeview (riga 2)
    app.tree_merceologie = ttk.Treeview(tree_wrap, height=18)
    app.tree_merceologie["columns"] = ("Id", "Merceologia", "Reparto")
    app.tree_merceologie["show"] = "headings"
    app.tree_merceologie.heading("Id", text="Id")
    app.tree_merceologie.heading("Merceologia", text="Merceologia")
    app.tree_merceologie.heading("Reparto", text="Reparto")
    app.tree_merceologie.column("Id", width=30)
    app.tree_merceologie.column("Merceologia", width=200)
    app.tree_merceologie.column("Reparto", width=120)
    app.tree_merceologie.bind("<<TreeviewSelect>>", app._onsingleclick)

    app.tree_merceologie.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))


    # --- Dettagli ---
    app.lbl_frame_merceologia_selezionata = ctk.CTkFrame(
        app.frame_dettagli,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.lbl_frame_merceologia_selezionata.grid(
        row=0, column=0, sticky="nsew", padx=(0, 0), pady=(0, 8)
    )
    app.lbl_frame_merceologia_selezionata.columnconfigure(1, weight=1)

    app.lbl_merceologia = ctk.CTkLabel(
        app.lbl_frame_merceologia_selezionata,
        text="Merceologia",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_merceologia.grid(row=0, column=0, padx=8, pady=(10, 6), sticky="w")

    app.ent_merceologia = ctk.CTkEntry(
        app.lbl_frame_merceologia_selezionata,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ent_merceologia.grid(row=0, column=1, padx=8, pady=(10, 6), sticky="ew")

    app.lbl_reparto = ctk.CTkLabel(
        app.lbl_frame_merceologia_selezionata,
        text="Reparto",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_reparto.grid(row=1, column=0, padx=8, pady=8, sticky="w")

    app.cmb_box_reparto_value = tk.StringVar()
    app.cmb_box_reparto = ttk.Combobox(
        app.lbl_frame_merceologia_selezionata,
        state="disabled",
        textvariable=app.cmb_box_reparto_value,
        values=[],
        font=(FONT_FAMILY, 12),
    )
    app.cmb_box_reparto.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

    # Frame attributi
    app.lbl_frame_attributi_merceologia = ctk.CTkFrame(
        app.frame_dettagli,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.lbl_frame_attributi_merceologia.grid(
        row=1, column=0, sticky="nsew", padx=(0, 0), pady=(0, 0)
    )
    app.lbl_frame_attributi_merceologia.columnconfigure(0, weight=1)

    # Header attributi
    app.lbl_titolo_attributi = ctk.CTkLabel(
        app.lbl_frame_attributi_merceologia,
        text="Attributi",
        font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
        text_color=COLORS["text_dark"],
    )
    app.lbl_titolo_attributi.grid(row=0, column=0, padx=8, pady=8, sticky="n")

    # Attributi (checkbox)
    app.label = {}
    app.ckbutton = {}
    if not hasattr(app, "valore_flag"):
        app.valore_flag = {}

    r = 1
    c = 0
    for attributo in app.ATTRIBUTI:
        if r % 12 == 0:
            r = 1
            c += 2

        lbl = ctk.CTkLabel(
            app.lbl_frame_attributi_merceologia,
            text=attributo,
            font=body_font,
            text_color=COLORS["text_dark"],
            anchor="w",
        )
        lbl.grid(row=r, column=c, padx=8, pady=6, sticky="w")
        app.label[attributo] = lbl

        app.valore_flag[attributo] = tk.IntVar()
        ckbtn = ctk.CTkCheckBox(
            app.lbl_frame_attributi_merceologia,
            text="",
            variable=app.valore_flag[attributo],
            onvalue=1,
            offvalue=0,
            fg_color=COLORS.get("accent", COLORS["accent_hover"]),
            hover_color=COLORS.get("accent_hover", COLORS["accent_hover"]),
            border_color=COLORS["border"],
            checkmark_color=COLORS["bg_content"],
            state="disabled",
        )
        ckbtn.grid(row=r, column=c + 1, padx=0, pady=6, sticky="w")
        app.ckbutton[attributo] = ckbtn

        r += 1

    # --- Toolbar (azioni) ---

    # Posizionamento “stile dipendenti”: in alto a destra (riga 0 della colonna dx)
    # e NON deformata in altezza (sticky="new" come anag_dipendenti).

    app.lbl_frame_scegli = ctk.CTkFrame(
        app.frame_toolbar,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )

    # In anag_dipendenti la toolbar sta su riga 0, colonna 1 con sticky="new".
    # Qui impostiamo direttamente lo stesso comportamento: toolbar compatta in alto.
    app.lbl_frame_scegli.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 12))

    # Toolbar azioni in verticale (1 colonna)
    app.lbl_frame_scegli.columnconfigure(0, weight=1)

    app.btn_nuovo = ctk.CTkButton(

        app.lbl_frame_scegli,
        text="Nuovo",
        font=btn_font,
        height=38,
        fg_color=COLORS.get("success", "#2ecc71"),
        hover_color="#1e8449",
        command=app._nuovo,
        state="normal",
    )

    app.btn_modifica = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Modifica",
        font=btn_font,
        height=38,
        fg_color=COLORS.get("success", "#2ecc71"),
        hover_color="#1e8449",
        command=app._modifica,
        state="normal",
    )

    app.btn_salva = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Salva",
        font=btn_font,
        height=38,
        fg_color=COLORS.get("accent", COLORS["accent_hover"]),
        hover_color=COLORS.get("accent_hover", COLORS["accent_hover"]),
        command=app._salva,
        state="disabled",
    )

    app.btn_annulla = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Annulla",
        font=btn_font,
        height=38,
        fg_color=COLORS.get("accent", COLORS["accent_hover"]),
        hover_color="#a93226",
        command=app._annulla,
        state="disabled",
    )

    app.btn_elimina = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Elimina",
        font=btn_font,
        height=38,
        fg_color=COLORS.get("danger", "#e74c3c"),
        hover_color=COLORS.get("accent_hover", COLORS["accent_hover"]),
        command=app._elimina,
        state="normal",
    )

    # Pulsanti in verticale (1 colonna)
    # Riga/colonna: in verticale (non orizzontale)
    app.btn_nuovo.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
    app.btn_modifica.grid(row=2, column=0, padx=8, pady=8, sticky="ew")
    app.btn_salva.grid(row=3, column=0, padx=8, pady=8, sticky="ew")
    app.btn_annulla.grid(row=4, column=0, padx=8, pady=8, sticky="ew")
    app.btn_elimina.grid(row=5, column=0, padx=8, pady=8, sticky="ew")

    # Stato iniziale: blocca campi e pulsanti salvataggio
    if hasattr(app, "_disabilita_campi"):
        app._disabilita_campi()



