"""
Modulo centralizzato per la connessione al database MySQL.
Usa le credenziali da config.ini (tramite config.get_config()).
"""
import mysql.connector
from contextlib import contextmanager

from config import get_config


def get_connection():
    """
    Crea e restituisce una connessione MySQL usando i parametri in config.ini.
    Il chiamante deve chiudere la connessione quando non serve più (es. conn.close()
    alla chiusura della finestra).
    """
    cfg = get_config()["DataBase"]
    port = int(cfg.get("port", 3306))
    return mysql.connector.connect(
        host=cfg["host"],
        port=port,
        database=cfg["db"],
        user=cfg["user"],
        password=cfg["pwd"],
    )


def close_connection(conn):
    """Chiude la connessione in modo sicuro (ignora errori)."""
    if conn is None:
        return
    try:
        conn.close()
    except Exception:
        pass


@contextmanager
def connection():
    """
    Context manager per usare una connessione MySQL con with.
    La connessione viene chiusa automaticamente all'uscita dal blocco.

    Esempio:
        with connection() as conn:
            c = conn.cursor()
            c.execute("SELECT ...")
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
