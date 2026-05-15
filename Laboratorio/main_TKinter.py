"""
Costruzione grafica per la finestra principale (Main) e dialog accesso anagrafica.
Usa CustomTkinter per un aspetto moderno; la logica applicativa resta in main.pyw.
"""
import os

import customtkinter as ctk
from PIL import Image

from theme import COLORS, FONT_FAMILY, FONT_SIZE, FONT_SIZE_LARGE


def _ctk_image(path, size):
    """Carica un'immagine (GIF incluso, primo frame) per CTkButton / CTkLabel."""
    pil = Image.open(path)
    if pil.mode not in ("RGB", "RGBA"):
        pil = pil.convert("RGBA")
    return ctk.CTkImage(light_image=pil, dark_image=pil, size=size)


def setup_root(root):
    """Configura finestra principale (CTk) e tema CustomTkinter."""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root.geometry("1200x520+40+40")
    root.minsize(800, 380)
    root.title("Gestione Laboratorio")
    root.configure(fg_color=COLORS["bg_light"])


def center_toplevel(toplevel):
    """Centra approssimativamente un Toplevel / CTkToplevel sullo schermo."""
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split("+")[0].split("x"))
    x = screen_width / 3 - size[0] / 2
    y = screen_height / 3 - size[1] / 2
    toplevel.geometry("+%d+%d" % (x, y))


def build_main_ui(app):
    """
    Costruisce frame, immagini, bottoni e layout della schermata principale.
    `app` e' CTkFrame (Main) con attributi parent, config e metodi command.
    """
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    icon_size = (44, 44)
    btn_font = ctk.CTkFont(family=FONT_FAMILY, size=11)
    pad = (6, 10)

    app.frm_alto = ctk.CTkFrame(app, fg_color=COLORS["bg_dark"], corner_radius=0)
    app.frm_centrale = ctk.CTkFrame(
        app,
        fg_color=COLORS["bg_content"],
        corner_radius=10,
        border_width=1,
        border_color=COLORS["border"],
    )
    app.frm_basso = ctk.CTkFrame(app, fg_color=COLORS["bg_light"], corner_radius=0)

    img_dir = "immagini"
    app.img_btn1 = _ctk_image(os.path.join(img_dir, "lbeef.gif"), icon_size)
    app.img_btn2 = _ctk_image(os.path.join(img_dir, "documentnew.gif"), icon_size)
    app.img_btn3 = _ctk_image(os.path.join(img_dir, "drun.gif"), icon_size)
    app.img_btn4 = _ctk_image(os.path.join(img_dir, "lfood.gif"), icon_size)
    app.img_btn4_a = _ctk_image(os.path.join(img_dir, "list.gif"), icon_size)
    app.img_btn5 = _ctk_image(os.path.join(img_dir, "ingredienti.gif"), icon_size)
    app.img_btn6 = _ctk_image(os.path.join(img_dir, "lock.gif"), icon_size)
    app.img_btn7 = _ctk_image(os.path.join(img_dir, "lvendita.gif"), icon_size)
    app.img_btn8 = _ctk_image(os.path.join(img_dir, "impostazioni.gif"), icon_size)
    app.img_btn9 = _ctk_image(os.path.join(img_dir, "menu.gif"), icon_size)
    app.img_btn9_a = _ctk_image(os.path.join(img_dir, "Order.gif"), icon_size)
    app.img_btn9_b = _ctk_image(os.path.join(img_dir, "bilancia.gif"), icon_size)
    app.img_btn10 = _ctk_image(os.path.join(img_dir, "exit.gif"), icon_size)

    btn_kw = dict(
        master=app.frm_alto,
        compound="bottom",
        font=btn_font,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        text_color="white",
        corner_radius=8,
        height=86,
        width=108,
        border_spacing=4,
    )

    bottone1 = ctk.CTkButton(
        text="Ingresso Merce", image=app.img_btn1, command=app.ingresso_merce, **btn_kw
    )
    bottone2 = ctk.CTkButton(
        text="Nuovo Lotto", image=app.img_btn2, command=app.nuovo_lotto, **btn_kw
    )
    bottone3 = ctk.CTkButton(
        text="Inventario", image=app.img_btn3, command=app.inventario, **btn_kw
    )
    bottone4 = ctk.CTkButton(
        text="Lotto Cucina", image=app.img_btn4, command=app.nuovo_lotto_cucina, **btn_kw
    )
    bottone4a = ctk.CTkButton(
        text="Lotti Vendita Cucina",
        image=app.img_btn4_a,
        command=app.lotti_vendita_cucina,
        **btn_kw,
    )
    bottone5 = ctk.CTkButton(
        text="Ingredienti", image=app.img_btn5, command=app.ingredienti, **btn_kw
    )
    bottone6 = ctk.CTkButton(
        text="Chiudi Lotti", image=app.img_btn6, command=app.chiudi_lotto, **btn_kw
    )
    bottone7 = ctk.CTkButton(
        text="Vendita", image=app.img_btn7, command=app.lotti_in_vendita, **btn_kw
    )
    bottone8 = ctk.CTkButton(
        text="Impostazioni", image=app.img_btn8, command=app.anagrafica, **btn_kw
    )
    bottone9 = ctk.CTkButton(
        text="Nuovo Menu", image=app.img_btn9, command=app.nuovo_menu, **btn_kw
    )
    bottone9a = ctk.CTkButton(
        text="Ordine",
        image=app.img_btn9_a,
        state="disabled",
        **btn_kw,
    )
    bottone9b = ctk.CTkButton(
        text="Dosi", image=app.img_btn9_b, command=app.dosi, **btn_kw
    )
    bottone10 = ctk.CTkButton(
        text="Uscita",
        image=app.img_btn10,
        command=app._esci,
        fg_color=COLORS["danger"],
        hover_color="#a93226",
        **{k: v for k, v in btn_kw.items() if k not in ("fg_color", "hover_color")},
    )

    app.immagine1 = _ctk_image(os.path.join(img_dir, "dlogo.gif"), (320, 120))
    label1 = ctk.CTkLabel(app.frm_centrale, image=app.immagine1, text="")

    foot_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE)
    lbl_utente = ctk.CTkLabel(
        app.frm_basso,
        text="Utente: ",
        font=foot_font,
        text_color=COLORS["text_dark"],
        fg_color="transparent",
    )
    lbl_nome_utente = ctk.CTkLabel(
        app.frm_basso,
        text=os.environ.get("COMPUTERNAME", ""),
        font=foot_font,
        text_color=COLORS["text_dark"],
        fg_color="transparent",
    )
    lbl_winswgx = ctk.CTkLabel(
        app.frm_basso,
        text="Winswgx: ",
        font=foot_font,
        text_color=COLORS["text_light"],
        fg_color="transparent",
    )
    lbl_winswgx_percorso = ctk.CTkLabel(
        app.frm_basso,
        text=app.config["Winswgx"]["dir"] or "(non impostato)",
        font=foot_font,
        text_color=COLORS["text_dark"],
        fg_color="transparent",
    )

    bottone1.grid(row=0, column=0, padx=pad[0], pady=pad[1])
    bottone2.grid(row=0, column=1, padx=pad[0], pady=pad[1], sticky="we")
    bottone3.grid(row=0, column=2, padx=pad[0], pady=pad[1], sticky="we")
    bottone6.grid(row=0, column=3, padx=pad[0], pady=pad[1])
    bottone7.grid(row=0, column=4, padx=pad[0], pady=pad[1])
    bottone8.grid(row=0, column=5, padx=pad[0], pady=pad[1])
    bottone9a.grid(row=0, column=6, padx=pad[0], pady=pad[1])
    bottone9b.grid(row=0, column=7, padx=pad[0], pady=pad[1])
    bottone10.grid(row=0, column=8, padx=pad[0], pady=pad[1])
    bottone5.grid(row=1, column=0, padx=pad[0], pady=pad[1])
    bottone4.grid(row=1, column=1, padx=pad[0], pady=pad[1])
    bottone4a.grid(row=1, column=2, padx=pad[0], pady=pad[1])
    bottone9.grid(row=1, column=3, padx=pad[0], pady=pad[1])

    for c in range(9):
        app.frm_alto.grid_columnconfigure(c, weight=1)

    app.frm_centrale.grid_propagate(False)
    app.frm_centrale.configure(height=220, width=900)
    app.frm_centrale.grid_rowconfigure(0, weight=1)
    app.frm_centrale.grid_columnconfigure(0, weight=1)

    app.frm_alto.grid(row=0, column=0, sticky="ew")
    app.frm_centrale.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
    app.frm_basso.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))

    label1.grid(row=0, column=0)
    lbl_utente.grid(row=0, column=0, padx=(8, 0), pady=8)
    lbl_nome_utente.grid(row=0, column=1, padx=4, pady=8)
    lbl_winswgx.grid(row=0, column=2, padx=(16, 0), pady=8)
    lbl_winswgx_percorso.grid(row=0, column=3, padx=(0, 8), pady=8)


def build_anagrafica_access_ui(window, try_login):
    """
    Crea il dialog password per accesso anagrafica (CustomTkinter).
    `try_login` viene chiamato al click su Accedi e su Invio.
    Restituisce CTkEntry (per .get() nel callback).
    """
    window.title("Accesso Impostazioni")
    window.geometry("340x180")
    window.configure(fg_color=COLORS["bg_light"])
    window.bind("<Return>", try_login)

    frame = ctk.CTkFrame(window, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    lbl_password = ctk.CTkLabel(
        frame,
        text="Password:",
        font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_LARGE, weight="bold"),
        text_color=COLORS["text_dark"],
    )
    ent_password = ctk.CTkEntry(frame, show="*", width=200, height=32, corner_radius=6)
    btn_login = ctk.CTkButton(
        frame,
        text="Accedi",
        command=try_login,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        height=36,
        corner_radius=8,
    )
    ent_password.focus()

    lbl_password.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="e")
    ent_password.grid(row=0, column=1, padx=8, pady=8, sticky="we")
    btn_login.grid(row=1, column=0, columnspan=2, padx=8, pady=12, sticky="ew")
    frame.grid_columnconfigure(1, weight=1)
    return ent_password
