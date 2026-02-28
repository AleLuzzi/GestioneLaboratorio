"""
Tema grafico centralizzato per Gestione Laboratorio.
Palette coerente e stili ttk per un aspetto moderno e pulito.
"""
import tkinter as tk
import tkinter.ttk as ttk

# Palette colori (tema chiaro professionale)
COLORS = {
    "bg_dark": "#2c3e50",       # Header / barra superiore
    "bg_light": "#ecf0f1",      # Sfondo aree secondarie
    "bg_content": "#ffffff",    # Sfondo contenuti / card
    "accent": "#3498db",        # Blu per bottoni e link
    "accent_hover": "#2980b9",  # Blu scuro (stato attivo)
    "text_dark": "#2c3e50",     # Testo principale
    "text_light": "#7f8c8d",    # Testo secondario
    "border": "#bdc3c7",        # Bordi
    "success": "#27ae60",       # Verde (conferme)
    "danger": "#c0392b",        # Rosso (uscita / azioni critiche)
}

# Font
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10
FONT_SIZE_TITLE = 12
FONT_SIZE_LARGE = 14


def get_font(size=None, bold=False):
    """Restituisce tupla font (family, size, weight)."""
    s = size or FONT_SIZE
    w = "bold" if bold else "normal"
    return (FONT_FAMILY, s, w)


def apply_theme(root):
    """
    Applica il tema all'applicazione.
    Chiamare una volta all'avvio con la finestra principale (root).
    """
    # Sfondo finestra principale
    root.configure(bg=COLORS["bg_light"])

    # Stile ttk: usare 'clam' per avere pieno controllo sui colori
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass  # Se clam non disponibile, restano i default

    # Frame
    style.configure(
        "TFrame",
        background=COLORS["bg_light"],
    )

    # Bottoni
    style.configure(
        "TButton",
        font=get_font(FONT_SIZE),
        padding=(12, 8),
        background=COLORS["accent"],
        foreground="white",
    )
    style.map(
        "TButton",
        background=[("active", COLORS["accent_hover"]), ("pressed", COLORS["accent_hover"])],
        foreground=[("active", "white")],
    )

    # Label
    style.configure(
        "TLabel",
        font=get_font(FONT_SIZE),
        background=COLORS["bg_light"],
        foreground=COLORS["text_dark"],
    )

    # Treeview
    style.configure(
        "Treeview",
        font=get_font(FONT_SIZE - 1),
        rowheight=24,
        background=COLORS["bg_content"],
        foreground=COLORS["text_dark"],
        fieldbackground=COLORS["bg_content"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        font=get_font(FONT_SIZE - 1, bold=True),
        background=COLORS["bg_dark"],
        foreground="white",
    )
    style.map(
        "Treeview",
        background=[("selected", COLORS["accent"])],
        foreground=[("selected", "white")],
    )

    # Notebook (tab)
    style.configure(
        "TNotebook",
        background=COLORS["bg_light"],
    )
    style.configure(
        "TNotebook.Tab",
        font=get_font(FONT_SIZE),
        padding=(12, 6),
    )

    # Entry / Combobox
    style.configure(
        "TEntry",
        font=get_font(FONT_SIZE),
        padding=4,
    )
    style.configure(
        "TCombobox",
        font=get_font(FONT_SIZE),
        padding=4,
    )

    # LabelFrame
    style.configure(
        "TLabelframe",
        background=COLORS["bg_light"],
        foreground=COLORS["text_dark"],
    )
    style.configure(
        "TLabelframe.Label",
        font=get_font(FONT_SIZE_TITLE, bold=True),
        background=COLORS["bg_light"],
        foreground=COLORS["text_dark"],
    )


def style_header_frame(frame):
    """Applica lo stile della barra header (scura) a un tk.Frame."""
    frame.configure(bg=COLORS["bg_dark"], bd=0, highlightthickness=0)


def style_content_frame(frame):
    """Applica lo stile area contenuto (chiara) a un tk.Frame."""
    frame.configure(bg=COLORS["bg_content"], bd=0, highlightthickness=0)


def style_footer_frame(frame):
    """Applica lo stile barra inferiore a un tk.Frame."""
    frame.configure(bg=COLORS["bg_light"], bd=0, highlightthickness=0)
