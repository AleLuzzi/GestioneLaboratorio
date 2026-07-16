import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import customtkinter as ctk

from theme import COLORS, FONT_FAMILY, get_font


def setup_window(window):
    """Configura finestra principale anagrafica fornitori."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.title("Anagrafica fornitori")
    # Mantieni solo la posizione: la dimensione verrà calcolata dopo la costruzione UI
    window.geometry("+80+80")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

def build_ui(app):
    """Costruisce layout e widget; richiede connessione/cursor gia' su `app`."""

    title_font = ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold")
    label_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
    body_font = ctk.CTkFont(family=FONT_FAMILY, size=12)
    btn_font = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")

    # --- CONFIGURAZIONE DI app.frame_root ---
    app.frame_root = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_root.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

    # Colonne a larghezza fissa: la finestra si adatta al contenuto, senza espansione orizzontale
    app.frame_root.columnconfigure(0, weight=0)
    app.frame_root.columnconfigure(1, weight=0)

    # Gestione Righe:
    # In questo layout usiamo: row=0 per titolo/toolbar e row=1 per dettagli.
    # L'area elenco (frame_elenco) occupa anche row=0 con rowspan=2.
    app.frame_root.rowconfigure(0, weight=0)
    app.frame_root.rowconfigure(1, weight=1)


    

    app.lbl_titolo = ctk.CTkLabel(
        app.frame_root,
        text="ANAGRAFICA FORNITORI",
        font=title_font,
        text_color=COLORS["accent_hover"],
    )
    app.lbl_titolo.grid(row=0, column=0, columnspan=2, sticky="w", padx=4, pady=(0, 8))

    app.frame_elenco = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli = ctk.CTkFrame(app.frame_root, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_dettagli.grid_columnconfigure(0, weight=1)
    app.frame_dettagli.grid_columnconfigure(1, weight=0, minsize=140)  # colonna "azioni" a larghezza fissa
    app.frame_dettagli.grid_rowconfigure(0, weight=1)

    # --- POSIZIONAMENTO DEI FRAME FIGLI ---

    # L'elenco copre entrambe le righe e segue l'altezza totale grazie a sticky="nsew"
    # (come in anag_dipendenti)
    app.frame_elenco.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=(0, 8), pady=0)

    # Dettagli + azioni affiancati nella colonna 1
    app.frame_dettagli.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=0)

    # Importante: la griglia interna di frame_dettagli deve avere una riga 0 espandibile
    # (per evitare che i box finiscano “a metà” del frame elenco)
    app.frame_dettagli.rowconfigure(0, weight=1)
    app.frame_elenco.rowconfigure(0, weight=1)
    app.frame_elenco.columnconfigure(0, weight=1)

    # 1. Creazione del LabelFrame personalizzato
    app.label_frame_elenco = ctk.CTkFrame(app.frame_elenco, fg_color=COLORS["bg_content"], corner_radius=8)
    app.label_frame_elenco.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    # Configurazione righe: riga 0 (titolo) e riga 1 (ricerca) fisse, riga 2 (Treeview) si espande
    app.label_frame_elenco.rowconfigure(2, weight=1) 
    app.label_frame_elenco.columnconfigure(0, weight=1)

    # 2. Etichetta del titolo "Elenco" (Riga 0)
    titolo_elenco = ctk.CTkLabel(
    app.label_frame_elenco, 
    text="Elenco", 
    font=ctk.CTkFont(size=14, weight="bold"), 
    anchor="w"
    )
    titolo_elenco.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 5))
    
    # 3. Creazione del sotto-contenitore per affiancare barra e pulsante X
    app.frame_ricerca_sub = ctk.CTkFrame(app.label_frame_elenco, fg_color="transparent")
    app.frame_ricerca_sub.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
    app.frame_ricerca_sub.columnconfigure(0, weight=1)  # La barra di ricerca prende tutto lo spazio
    app.frame_ricerca_sub.columnconfigure(1, weight=0)  # Il pulsante mantiene la sua dimensione fissa

    # Campo di inserimento per il filtro (Spostato dentro il frame_ricerca_sub alla colonna 0)
    app.entry_filtro = ctk.CTkEntry(
        app.frame_ricerca_sub, 
        placeholder_text="Cerca azienda..."
    )
    app.entry_filtro.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=0)
    app.entry_filtro.bind("<KeyRelease>", app._filtra_aziende)

    # NUOVO: Piccolo pulsante di reset a fianco (Colonna 1)
    app.btn_reset_filtro = ctk.CTkButton(
        app.frame_ricerca_sub,
        text="✕",               # Simbolo della X di chiusura
        width=30,               # Stretto e compatto
        height=28,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=COLORS["border"],         # Colore neutro iniziale
        hover_color=COLORS["accent_hover"], # Colore d'evidenziazione al passaggio del mouse
        text_color=COLORS["text_dark"],
        command=app._reset_ricerca          # Punta al nuovo metodo nel controller
    )
    app.btn_reset_filtro.grid(row=0, column=1, sticky="e", padx=0, pady=0)

    # 4. Il tuo tree_wrap originale (Spostato alla Riga 2)
    tree_wrap = ctk.CTkFrame(app.label_frame_elenco, fg_color=COLORS["bg_content"], corner_radius=0)
    tree_wrap.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 6))
    tree_wrap.rowconfigure(0, weight=1)
    tree_wrap.columnconfigure(0, weight=1)

    app.tree_fornitori = ttk.Treeview(tree_wrap, height=18)
    app.tree_fornitori["columns"] = ("Id", "Azienda")
    app.tree_fornitori["show"] = "headings"
    app.tree_fornitori.heading("Id", text="Id")
    app.tree_fornitori.heading("Azienda", text="Azienda")
    app.tree_fornitori.column("Id", width=48, anchor="center")
    app.tree_fornitori.column("Azienda", width=200)
    app.tree_fornitori.bind("<<TreeviewSelect>>", app._onsingleclick)
    app.tree_fornitori.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    app.lbl_frame_dettagli_selezionato = ctk.CTkFrame(
        app.frame_dettagli,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8
    )

    # Titolo in alto per allineare i 3 box (titolo+campi e attributi) come nel modello dipendenti
    app.lbl_titolo_dettagli = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="Dettagli fornitore selezionato",
        font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
        text_color=COLORS["text_dark"]
    )
    app.lbl_titolo_dettagli.grid(row=0, column=0, columnspan=2, padx=8, pady=(10, 5), sticky="n")

    app.lbl_frame_dettagli_selezionato.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 8))

    app.lbl_azienda = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="Ragione sociale",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_azienda.grid(row=1, column=0, padx=8, pady=8, sticky="w")
    app.ent_azienda = ctk.CTkEntry(
        app.lbl_frame_dettagli_selezionato,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled"
    )
    app.ent_azienda.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

    # NOTE: Spostate checkbox dal vecchio contenitore “attributi” dentro il contenitore “dettagli”.
    # In questo modo possiamo cancellare completamente app.lbl_frame_attributi_fornitori.

    app.valore_flag_ing_merce = tk.IntVar()
    app.valore_flag_inv = tk.IntVar()
    
    app.ckbtn_ing_merce = ctk.CTkCheckBox(
        app.lbl_frame_dettagli_selezionato,
        text="Visualizza nel modulo Ingresso merce",
        variable=app.valore_flag_ing_merce,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled"
    )
    app.ckbtn_ing_merce.grid(row=2, column=0, padx=8, pady=10, sticky="w")

    app.ckbtn_inv = ctk.CTkCheckBox(
        app.lbl_frame_dettagli_selezionato,
        text="Visualizza nel modulo Inventario",
        variable=app.valore_flag_inv,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
        state="disabled"
    )
    app.ckbtn_inv.grid(row=3, column=0, padx=8, pady=10, sticky="w")


    # --- Azioni: label frame con bottoni a destra del frame "Attributi" e disposti in verticale ---

    app.lbl_frame_scegli = ctk.CTkFrame(
        app.frame_dettagli,
        fg_color=COLORS["bg_light"],
        border_color=COLORS["border"],
        border_width=1,
        corner_radius=8,
    )
    app.lbl_frame_scegli.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
    app.lbl_frame_scegli.columnconfigure(0, weight=1)

    app.btn_nuovo = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Nuovo",
        font=btn_font,
        width=120,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._nuovo,
    )

    app.btn_modifica = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Modifica",
        font=btn_font,
        width=120,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._modifica,
    )

    app.btn_salva = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Salva",
        font=btn_font,
        width=120,
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._salva,
        state="disabled",
    )

    app.btn_annulla = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Annulla",
        font=btn_font,
        width=120,
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
        width=120,
        height=38,
        fg_color=COLORS["danger"],
        hover_color=COLORS["accent_hover"],
        state="disabled",
        command=app._elimina,
    )

    # Pulsanti in verticale (1 colonna)
    app.btn_nuovo.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
    app.btn_modifica.grid(row=2, column=0, padx=8, pady=8, sticky="ew")
    app.btn_salva.grid(row=3, column=0, padx=8, pady=8, sticky="ew")
    app.btn_annulla.grid(row=4, column=0, padx=8, pady=8, sticky="ew")
    app.btn_elimina.grid(row=5, column=0, padx=8, pady=8, sticky="ew")


    # --- Adatta dimensione finestra ai tre labelframe (senza spazio vuoto a destra) ---
    try:
        app.update_idletasks()
        w_elenco = max(app.label_frame_elenco.winfo_reqwidth(), 280)
        w_dettagli = max(app.lbl_frame_dettagli_selezionato.winfo_reqwidth(), 420)
        w_azioni = max(app.lbl_frame_scegli.winfo_reqwidth(), 140)
        gap_dettagli_azioni = 14  # padx + bordi tra dettagli e azioni
        gap_colonne = 16          # padx tra elenco e colonna dettagli
        margini = 40              # padx/pady di frame_root + margini finestra
        w = w_elenco + w_dettagli + w_azioni + gap_dettagli_azioni + gap_colonne + margini
        h = max(app.frame_root.winfo_reqheight() + 40, 420)
        app.geometry(f"{w}x{h}")
        app.minsize(w, 420)
    except Exception:
        app.geometry("900x420")
        app.minsize(900, 420)

    app._aggiorna()


