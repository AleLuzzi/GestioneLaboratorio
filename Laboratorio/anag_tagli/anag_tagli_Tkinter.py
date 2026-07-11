import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from theme import COLORS, FONT_FAMILY, get_font


def setup_window(window):
    """Configura la finestra principale per l'anagrafica tagli."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.title("Anagrafica Tagli")
    window.geometry("+80+80")
    window.minsize(720, 420)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)


def build_ui(app):
    """Costruisce la UI; il controller gestisce DB/cursor.

    Richiede che su `app` esistano:
    - self.conn e self.c o comunque gestisce i dati altrove

    Espone widget come attributi per il controller:
    - tree_tagli
    - entry_taglio
    - ent_merceologia (combobox)
    - ckbtn_in_inventario (checkbox)
    - btn_nuovo, btn_modifica, btn_salva, btn_annulla, btn_elimina
    - entry_filtro (per _filtra)

    Gestione eventi attesi (tipicamente nel controller):
    - _onsingleclick, _filtra_tagli, _reset_ricerca, _nuovo, _modifica, _salva, _annulla, _elimina
    """

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
        text="ANAGRAFICA TAGLI",
        font=title_font,
        text_color=COLORS["accent_hover"],
    )
    app.lbl_titolo.grid(row=0, column=0, columnspan=3, sticky="w", padx=4, pady=(0, 8))

    app.frame_elenco = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
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
        placeholder_text="Cerca taglio...",
    )
    app.entry_filtro.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=0)
    app.entry_filtro.bind("<KeyRelease>", getattr(app, "_filtra_tagli", lambda e=None: None))

    app.btn_reset_filtro = ctk.CTkButton(
        app.frame_ricerca_sub,
        text="✕",
        width=30,
        height=28,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=COLORS["border"],
        hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_dark"],
        command=getattr(app, "_reset_ricerca", lambda: None),
    )
    app.btn_reset_filtro.grid(row=0, column=1, sticky="e", padx=0, pady=0)

    tree_wrap = ctk.CTkFrame(app.label_frame_elenco, fg_color=COLORS["bg_content"], corner_radius=0)
    tree_wrap.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
    tree_wrap.rowconfigure(0, weight=1)
    tree_wrap.columnconfigure(0, weight=1)

    app.tree_tagli = ttk.Treeview(tree_wrap, height=18)
    app.tree_tagli["columns"] = ("Id", "Tagli", "Merceologia")
    app.tree_tagli["show"] = "headings"
    app.tree_tagli.heading("Id", text="Id")
    app.tree_tagli.heading("Tagli", text="Tagli")
    app.tree_tagli.heading("Merceologia", text="Merceologia")

    app.tree_tagli.column("Id", width=30)
    app.tree_tagli.column("Tagli", width=150)
    app.tree_tagli.column("Merceologia", width=150)

    # Nel controller verrà gestito come: _onsingleclick(event)
    app.tree_tagli.bind("<<TreeviewSelect>>", getattr(app, "_onsingleclick", lambda e=None: None))
    app.tree_tagli.bind("<Double-1>", getattr(app, "_onsingleclick", lambda e=None: None))

    app.tree_tagli.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    # --- Dettagli ---
    app.lbl_frame_dettagli_selezionato = tk.LabelFrame(
        app.frame_dettagli,
        text="Dettagli taglio selezionato",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.lbl_frame_dettagli_selezionato.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 8))

    app.lbl_taglio = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="TAGLIO",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_taglio.grid(row=0, column=0, padx=8, pady=8, sticky="w")

    app.entry_taglio = ctk.CTkEntry(
        app.lbl_frame_dettagli_selezionato,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.entry_taglio.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

    app.lbl_frame_dettagli_selezionato.columnconfigure(1, weight=1)

    app.lbl_merceologia = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="MERCEOLOGIA",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_merceologia.grid(row=2, column=0, padx=8, pady=8, sticky="w")

    # Combobox merceologia: stessa idea di anag_ingredienti (controller può riempirla)
    app.box_merceologia = ttk.Combobox(
        app.lbl_frame_dettagli_selezionato,
        state="disabled",
        font=(FONT_FAMILY, 12),
        values=[],
    )
    app.box_merceologia.grid(row=2, column=1, padx=8, pady=8, sticky="ew")

    # Compatibilità API: molti controller usano ent_merceologia come handle
    app.ent_merceologia = app.box_merceologia

    # Checkbox: “Visualizza nel modulo Inventario” (presente nel file legacy)
    app.valori_in_inventario = tk.IntVar(value=0)
    app.ckbtn_in_inventario = ctk.CTkCheckBox(
        app.lbl_frame_dettagli_selezionato,
        text="Visualizza nel modulo Inventario",
        variable=app.valori_in_inventario,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled",
    )
    app.ckbtn_in_inventario.grid(row=3, column=0, columnspan=2, padx=8, pady=(6, 8), sticky="w")

    # --- Toolbar Bottoni ---
    app.frame_scegli = ctk.CTkFrame(
        app.frame_toolbar,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.frame_scegli.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

    for col in range(5):
        app.frame_scegli.columnconfigure(col, weight=1)

    app.btn_nuovo = ctk.CTkButton(
        app.frame_scegli,
        text="Nuovo",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=getattr(app, "_nuovo", lambda: None),
    )

    app.btn_modifica = ctk.CTkButton(
        app.frame_scegli,
        text="Modifica",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=getattr(app, "_modifica", lambda: None),
    )

    app.btn_salva = ctk.CTkButton(
        app.frame_scegli,
        text="Salva",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        state="disabled",
        command=getattr(app, "_salva", lambda: None),
    )

    app.btn_annulla = ctk.CTkButton(
        app.frame_scegli,
        text="Annulla",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color="#a93226",
        state="disabled",
        command=getattr(app, "_annulla", lambda: None),
    )

    app.btn_elimina = ctk.CTkButton(
        app.frame_scegli,
        text="Elimina",
        font=btn_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color=COLORS["accent_hover"],
        state="disabled",
        command=getattr(app, "_elimina", lambda: None),
    )

    app.btn_nuovo.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
    app.btn_modifica.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    app.btn_salva.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
    app.btn_annulla.grid(row=0, column=3, padx=8, pady=8, sticky="ew")
    app.btn_elimina.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

    # Aggiornamento dati: se il controller espone _aggiorna
    if hasattr(app, "_aggiorna"):
        app._aggiorna()

