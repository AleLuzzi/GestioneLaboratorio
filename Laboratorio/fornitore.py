class Fornitore:
    """Record fornitore (tabella `fornitori`), allineato a `anagrafica_fornitori`."""

    __slots__ = ("id", "azienda", "flag1_ing_merce", "flag2_inventario")

    def __init__(self, id=None, azienda="", flag1_ing_merce=0, flag2_inventario=0):
        self.id = id
        self.azienda = azienda
        self.flag1_ing_merce = int(flag1_ing_merce)
        self.flag2_inventario = int(flag2_inventario)

    @classmethod
    def from_row(cls, row):
        """Costruisce da una riga `SELECT * FROM fornitori` (ID, azienda, flag1_ing_merce, flag2_inventario)."""
        return cls(row[0], row[1], row[2], row[3])

    def params_insert(self):
        """Valori per INSERT INTO fornitori(azienda, flag1_ing_merce, flag2_inventario) VALUES (...)."""
        return (self.azienda, self.flag1_ing_merce, self.flag2_inventario)

    def params_update(self):
        """Valori per UPDATE ... SET azienda, flag1_ing_merce, flag2_inventario WHERE ID = %s."""
        return (self.azienda, self.flag1_ing_merce, self.flag2_inventario, self.id)

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i fornitori presenti nel database."""
        cursor.execute("SELECT id, azienda, flag1_ing_merce, flag2_inventario FROM fornitori")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, f_id):
        """Cerca un singolo fornitore tramite il suo ID identificativo."""
        cursor.execute("SELECT id, azienda, flag1_ing_merce, flag2_inventario FROM fornitori WHERE id = %s", (f_id,))
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Esegue l'aggiornamento (UPDATE) del record corrente sul database."""
        cursor.execute(
            "UPDATE fornitori SET azienda = %s, flag1_ing_merce = %s, flag2_inventario = %s WHERE id = %s",
            self.params_update()
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente dal database utilizzando il suo ID."""
        cursor.execute("DELETE FROM fornitori WHERE id = %s", (self.id,))
        conn.commit()

    def insert(self, cursor, conn):
        """Esegue l'inserimento (INSERT) del nuovo fornitore sul database."""
        cursor.execute(
            "INSERT INTO fornitori(azienda, flag1_ing_merce, flag2_inventario) VALUES (%s, %s, %s)",
            self.params_insert()
        )
        conn.commit()

