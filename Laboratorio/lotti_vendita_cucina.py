import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import mysql.connector
import shutil
import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Spacer,
                                Table, TableStyle, Paragraph)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import win32api
from tkinter import messagebox

class LottiInVenditaCucina(tk.Toplevel):
    def __init__(self):
        super(LottiInVenditaCucina, self).__init__()
        self.geometry("1024x525+0+0")
        self.title('Lotti in vendita Cucina')

if __name__ == "__main__":
    root = tk.Tk()
    new = LottiInVenditaCucina()
    root.mainloop()
