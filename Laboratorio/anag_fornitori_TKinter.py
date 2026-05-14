import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import customtkinter as ctk
import mysql.connector

from theme import COLORS, FONT_FAMILY, get_font


def setup_window(window):
    """Configura finestra principale anagrafica fornitori."""
    ctk.set_appearance_mode("light")
    window.configure(bg=COLORS["bg_light"])
    window.title("Anagrafica fornitori")
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

    # --- CONFIGURAZIONE DI app.frame_root ---
    app.frame_root = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)
    app.frame_root.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Gestione Colonne: elenco (colonna 0) prende più spazio orizzontale della colonna 1
    app.frame_root.columnconfigure(0, weight=2)
    app.frame_root.columnconfigure(1, weight=1)
    app.frame_root.columnconfigure(2, weight=0)

    # Gestione Righe: 
    app.frame_root.rowconfigure(0, weight=0)  # La toolbar non deve deformarsi in altezza
    app.frame_root.rowconfigure(1, weight=1)  # La riga dei dettagli si espande e riempie il vuoto

    

    app.lbl_titolo = ctk.CTkLabel(
        app.frame_root,
        text="ANAGRAFICA FORNITORI",
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

    # --- POSIZIONAMENTO DEI FRAME FIGLI ---

    # L'elenco copre entrambe le righe e segue l'altezza totale grazie a sticky="nsew"
    app.frame_elenco.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8), pady=0)

    # La toolbar sta in alto a destra e non si allunga verticalmente (sticky="new")
    app.frame_toolbar.grid(row=0, column=1, sticky="new", padx=(8, 0), pady=0)

    # Il frame dettagli riempie TUTTA la riga 1 sia in larghezza che in altezza (sticky="nsew")
    app.frame_dettagli.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=0)

    # app.frame_elenco.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8), pady=0)
    # app.frame_toolbar.grid(row=0, column=1, sticky="new", padx=(8, 0), pady=0)
    # app.frame_dettagli.grid(row=1, column=1, sticky="new", padx=4, pady=0)
    
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

    # 3. NUOVO: Campo di inserimento per il filtro (Riga 1)
    app.entry_filtro = ctk.CTkEntry(
        app.label_frame_elenco, 
        placeholder_text="Cerca azienda..."
    )
    app.entry_filtro.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
    # Collega l'evento "tasto rilasciato" alla funzione di filtraggio
    app.entry_filtro.bind("<KeyRelease>", app._filtra_aziende)

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

    app.lbl_frame_dettagli_selezionato = tk.LabelFrame(
        app.frame_dettagli,
        text="Dettagli fornitore selezionato",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.lbl_frame_dettagli_selezionato.grid(row=0, column=0, sticky="nsew", pady=(0, 8))

    app.lbl_azienda = ctk.CTkLabel(
        app.lbl_frame_dettagli_selezionato,
        text="Ragione sociale",
        font=label_font,
        text_color=COLORS["text_dark"],
    )
    app.lbl_azienda.grid(row=0, column=0, padx=8, pady=8, sticky="w")
    app.ent_azienda = ctk.CTkEntry(
        app.lbl_frame_dettagli_selezionato,
        width=240,
        height=34,
        font=body_font,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    app.ent_azienda.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    app.lbl_frame_dettagli_selezionato.columnconfigure(1, weight=1)

    app.lbl_frame_attributi_fornitori = tk.LabelFrame(
        app.frame_dettagli,
        text="Attributi fornitore selezionato",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.lbl_frame_attributi_fornitori.grid(row=0, column=1, sticky="nsew", pady=(0, 8))

    app.valore_flag_ing_merce = tk.IntVar()
    app.valore_flag_inv = tk.IntVar()

    app.ckbtn_ing_merce = ctk.CTkCheckBox(
        app.lbl_frame_attributi_fornitori,
        text="Visualizza nel modulo Ingresso merce",
        variable=app.valore_flag_ing_merce,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    app.ckbtn_ing_merce.grid(row=0, column=0, padx=8, pady=10, sticky="w")

    app.ckbtn_inv = ctk.CTkCheckBox(
        app.lbl_frame_attributi_fornitori,
        text="Visualizza nel modulo Inventario",
        variable=app.valore_flag_inv,
        onvalue=1,
        offvalue=0,
        font=body_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    app.ckbtn_inv.grid(row=1, column=0, padx=8, pady=10, sticky="w")

    app.lbl_frame_scegli = tk.LabelFrame(
        app.frame_toolbar,
        text="Azioni",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    app.lbl_frame_scegli.grid(row=0, column=0, sticky="ew")

    
    

    app.btn_nuovo = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Nuovo",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=app._inserisci,
    )

    app.btn_modifica = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Modifica",
        font=btn_font,
        height=38,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        # command=app._modifica,
    )

    app.btn_salva = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Salva",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        command=app._salva,
    )

    app.btn_annulla = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Annulla",
        font=btn_font,
        height=38,
        fg_color=COLORS["accent"],
        hover_color="#a93226",
        # command=app._annulla,
    )

    app.btn_elimina = ctk.CTkButton(
        app.lbl_frame_scegli,
        text="Elimina",
        font=btn_font,
        height=38,
        fg_color=COLORS["danger"],
        hover_color=COLORS["accent_hover"],
        # command=app._elimina,
    )

    
    app.btn_nuovo.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
    app.btn_modifica.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
    app.btn_salva.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
    app.btn_annulla.grid(row=0, column=3, padx=8, pady=8, sticky="ew")
    app.btn_elimina.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

    for col in range(5):
        app.lbl_frame_scegli.columnconfigure(col, weight=1)

    app._aggiorna()


def show_insert_fornitore_dialog(app):
    """Finestra modale inserimento nuovo fornitore (solo UI + commit su `app`)."""

    def _centra(toplevel):
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        w = toplevel.winfo_reqwidth()
        h = toplevel.winfo_reqheight()
        x = max(0, int(screen_width / 2 - w / 2))
        y = max(0, int(screen_height / 2 - h / 2))
        toplevel.geometry(f"+{x}+{y}")

    def _salva_nuovo():
        nome_azienda = ent_azienda_new.get().strip()
        if nome_azienda:
            lista_da_salvare = [
                nome_azienda,
                ckbtn_ing_merce_value.get(),
                ckbtn_inventario_value.get(),
            ]
            try:
                app.c.execute(
                    "INSERT INTO fornitori(azienda, flag1_ing_merce, flag2_inventario) "
                    "VALUES (%s, %s, %s)",
                    lista_da_salvare,
                )
                app.conn.commit()
                app._aggiorna()
                nuovo_fornitore.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Errore Database", str(e))
        else:
            messagebox.showwarning("Attenzione", "Nome azienda obbligatorio.")

    nuovo_fornitore = tk.Toplevel(app)
    nuovo_fornitore.title("Nuovo fornitore")
    nuovo_fornitore.configure(bg=COLORS["bg_light"])
    nuovo_fornitore.resizable(False, False)

    body_font_dlg = ctk.CTkFont(family=FONT_FAMILY, size=12)
    label_font_dlg = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
    btn_font_dlg = ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")

    root_dlg = ctk.CTkFrame(nuovo_fornitore, fg_color=COLORS["bg_light"], corner_radius=0)
    root_dlg.pack(fill="both", expand=True, padx=14, pady=14)

    lbl_azienda_new = ctk.CTkLabel(
        root_dlg,
        text="Fornitore",
        font=label_font_dlg,
        text_color=COLORS["text_dark"],
    )
    lbl_azienda_new.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="w")

    ent_azienda_new = ctk.CTkEntry(
        root_dlg,
        width=280,
        height=34,
        font=body_font_dlg,
        fg_color=COLORS["bg_content"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    ent_azienda_new.grid(row=0, column=1, pady=8, sticky="ew")
    root_dlg.columnconfigure(1, weight=1)

    lblfrm_scelta_attributi = tk.LabelFrame(
        root_dlg,
        text="Mostra nei moduli",
        font=get_font(12, bold=True),
        fg=COLORS["text_dark"],
        bg=COLORS["bg_light"],
        labelanchor="n",
    )
    lblfrm_scelta_attributi.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 4))

    ckbtn_ing_merce_value = tk.IntVar()
    ckbtn_inventario_value = tk.IntVar()

    ckbtn_ingresso_merce = ctk.CTkCheckBox(
        lblfrm_scelta_attributi,
        text="Ingresso merce",
        variable=ckbtn_ing_merce_value,
        onvalue=1,
        offvalue=0,
        font=body_font_dlg,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    ckbtn_ingresso_merce.grid(row=0, column=0, padx=8, pady=10, sticky="w")

    ckbtn_inventario = ctk.CTkCheckBox(
        lblfrm_scelta_attributi,
        text="Inventario",
        variable=ckbtn_inventario_value,
        onvalue=1,
        offvalue=0,
        font=body_font_dlg,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_dark"],
    )
    ckbtn_inventario.grid(row=1, column=0, padx=8, pady=10, sticky="w")

    btn_row = ctk.CTkFrame(root_dlg, fg_color=COLORS["bg_light"], corner_radius=0)
    btn_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    btn_row.columnconfigure(0, weight=1)
    btn_row.columnconfigure(1, weight=1)

    btn_salva = ctk.CTkButton(
        btn_row,
        text="Salva dati",
        font=btn_font_dlg,
        height=36,
        fg_color=COLORS["success"],
        hover_color="#1e8449",
        command=_salva_nuovo,
    )
    btn_salva.grid(row=0, column=0, padx=(0, 6), sticky="ew")

    btn_chiudi = ctk.CTkButton(
        btn_row,
        text="Chiudi",
        font=btn_font_dlg,
        height=36,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        command=nuovo_fornitore.destroy,
    )
    btn_chiudi.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    nuovo_fornitore.transient(app)
    nuovo_fornitore.grab_set()
    _centra(nuovo_fornitore)
