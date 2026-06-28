"""Record/Model per la tabella `tagli`.

Questo modulo definisce una classe stile "Record" analoga a `anag_fornitori/fornitore.py`.

Tabella (dal progetto/uso GUI):
- tagli.ID (PK)
- tagli.taglio (descrizione)
- tagli.id_merceologia (FK verso merceologie.id)

Convenzioni:
- attributo Python: `id` (non `ID`)
- attributi: `taglio`, `id_merceologia`
"""


class Taglio:
    """Record taglio (tabella `tagli`)."""

    __slots__ = ("id", "taglio", "id_merceologia")

    def __init__(self, id=None, taglio="", id_merceologia=None):
        self.id = id
        self.taglio = taglio or ""
        self.id_merceologia = id_merceologia

    @classmethod
    def from_row(cls, row):
        """Costruisce da una riga `SELECT id, taglio, id_merceologia FROM tagli`."""
        return cls(row[0], row[1], row[2])

    def params_insert(self):
        """Valori per INSERT INTO tagli(taglio, Id_Merceologia) ..."""
        return (self.taglio, self.id_merceologia)

    def params_update(self):
        """Valori per UPDATE tagli SET taglio=%s, id_merceologia=%s WHERE id=%s"""
        return (self.taglio, self.id_merceologia, self.id)

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i tagli presenti nel database."""
        cursor.execute("SELECT id, taglio, id_merceologia FROM tagli")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, t_id):
        """Cerca un singolo taglio tramite il suo ID."""
        cursor.execute(
            "SELECT id, taglio, id_merceologia FROM tagli WHERE id = %s",
            (t_id,),
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Salva (UPDATE) il record corrente sul database."""
        cursor.execute(
            "UPDATE tagli SET taglio = %s, id_merceologia = %s WHERE id = %s",
            self.params_update(),
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente dal database usando il suo ID."""
        cursor.execute("DELETE FROM tagli WHERE id = %s", (self.id,))
        conn.commit()

    def insert(self, cursor, conn):
        """Inserisce il nuovo record sul database."""
        cursor.execute(
            "INSERT INTO tagli(taglio, Id_Merceologia) VALUES (%s, %s)",
            self.params_insert(),
        )
        conn.commit()

