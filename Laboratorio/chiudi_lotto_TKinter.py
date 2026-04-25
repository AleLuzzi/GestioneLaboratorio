import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import re

from theme import COLORS, FONT_FAMILY

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

    # Disposizione Frame
    app.frame_sx = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dx = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_basso_azioni = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

    # Treeview con riepilogo lotti aperti
    app.tree = ttk.Treeview(app.frame_sx, height=25)
    app.tree['columns'] = ('data ingresso', 'fornitore', 'peso', 'residuo')

    app.tree.column("data ingresso", width=80)
    app.tree.column("fornitore", width=80)
    app.tree.column("peso", width=80)
    app.tree.column("residuo", width=60)

    app.tree.heading("data ingresso", text="data ingresso")
    app.tree.heading("fornitore", text="fornitore")
    app.tree.heading("peso", text="peso")
    app.tree.heading("residuo", text="residuo")

    app.tree.tag_configure('odd', background=COLORS["bg_light"])

    app.tree.bind("<Double-1>", app._ondoubleclick)

    # LABEL lotti da chiudere
    title_font = ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold")
    app.lbl_nuovo_lotto = ctk.CTkLabel(
        app.frame_dx,
        text='LOTTI DA CHIUDERE',
        font=title_font,
        text_color=COLORS["accent_hover"])

    # Treeview per lotti scelti da chiudere
    app.tree_lotti_selezionati = ttk.Treeview(app.frame_dx)
    app.tree_lotti_selezionati['columns'] = ('lotto', 'taglio')

    app.tree_lotti_selezionati['show'] = 'headings'

    app.tree_lotti_selezionati.column("lotto", width=70)
    app.tree_lotti_selezionati.column("taglio", width=170)
    app.tree_lotti_selezionati.heading("lotto", text="Lotto")
    app.tree_lotti_selezionati.heading("taglio", text="Taglio")

    # BOTTONI azioni
    action_font = ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold")
    app.btn_esci = ctk.CTkButton(
        app.frame_basso_azioni,
        text="CHIUDI FINESTRA",
        font=action_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app.destroy
        )
    app.btn_salva = ctk.CTkButton(
        app.frame_basso_azioni,
        text='SALVA ed ESCI',
        font=action_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._salva
        )
    app.btn_rimuovi_riga = ctk.CTkButton(
        app.frame_dx, 
        text="RIMUOVI RIGA", 
        font=action_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=app._rimuovi_riga_selezionata
    )


    # LAYOUT
    app.frame_sx.grid(row=0, column=0, padx=8, pady=6, sticky="nsew")
    app.frame_dx.grid(row=0, column=1, padx=8, pady=6, sticky="we")
    app.frame_basso_azioni.grid(row=1, column=0, columnspan=2, padx=8, pady=6, sticky="we")

    app.tree.grid(row=0, column=0, sticky='w')
    app.lbl_nuovo_lotto.grid(row=0, column=0)
    app.tree_lotti_selezionati.grid(row=1, column=0)
    app.btn_rimuovi_riga.grid(row=2, column=0, sticky='we')

    app.btn_salva.grid(row=0, column=0, sticky="we")
    app.btn_esci.grid(row=0, column=1, sticky="we")

    app._aggiorna()