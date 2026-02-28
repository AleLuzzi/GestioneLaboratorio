"""
Modulo centralizzato per la lettura e scrittura di config.ini.
Il file viene cercato nella stessa cartella di questo modulo.
"""
import configparser
import os

# Percorso della cartella del modulo (Laboratorio) e del file di configurazione
_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_DIR, "config.ini")

_config = None


def get_config():
    """Legge config.ini e restituisce l'oggetto ConfigParser (in cache)."""
    global _config
    if _config is None:
        _config = configparser.ConfigParser()
        _config.read(CONFIG_PATH, encoding="utf-8")
    return _config


def save_config():
    """Scrive la configurazione corrente su config.ini."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        get_config().write(f)


def reload_config():
    """Rilegge config.ini da disco (utile dopo modifiche esterne)."""
    global _config
    _config = None
    return get_config()
