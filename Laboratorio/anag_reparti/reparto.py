class Reparto:
    """Record reparto (tabella `reparti`), allineato a `anagrafica_reparti`."""

    __slots__ = ("id", "reparto", "flag1_dip", "flag2_prod")

    def __init__(self, id=None, reparto="", flag1_dip=0, flag2_prod=0):
        self.id = id
        self.reparto = reparto
        self.flag1_dip = int(flag1_dip)
        self.flag2_prod = int(flag2_prod)

    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto da una riga della tabella reparti (id, reparto, flag1_dip, flag2_prod)."""
        return cls(row[0], row[1], row[2], row[3])

    def params_insert(self):
        """Valori per INSERT INTO reparti(reparto, flag1_dip, flag2_prod) VALUES (...)."""
        return (self.reparto, self.flag1_dip, self.flag2_prod)

    def params_update(self):
        """Valori per UPDATE ... SET reparto, flag1_dip, flag2_prod WHERE id = %s."""
        return (self.reparto, self.flag1_dip, self.flag2_prod, self.id)

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i reparti presenti nel database."""
        cursor.execute("SELECT id, reparto, flag1_dip, flag2_prod FROM reparti")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, f_id):
        """Cerca un singolo reparto tramite il suo ID identificativo."""
        cursor.execute(
            "SELECT id, reparto, flag1_dip, flag2_prod FROM reparti WHERE id = %s",
            (f_id,),
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Esegue l'aggiornamento (UPDATE) del record corrente sul database."""
        cursor.execute(
            "UPDATE reparti SET reparto = %s, flag1_dip = %s, flag2_prod = %s WHERE id = %s",
            self.params_update(),
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente dal database utilizzando il suo ID."""
        if self.id is None:
            raise ValueError("Impossibile eliminare un reparto privo di ID.")

        try:
            cursor.execute("DELETE FROM reparti WHERE id = %s", (self.id,))
            conn.commit()
            self.id = None
        except Exception as e:
            conn.rollback()
            raise e

    def insert(self, cursor, conn):
        """Esegue l'inserimento (INSERT) del nuovo reparto sul database."""
        try:
            cursor.execute(
                "INSERT INTO reparti (reparto, flag1_dip, flag2_prod) VALUES (%s, %s, %s)",
                self.params_insert(),
            )

            if hasattr(cursor, "lastrowid") and cursor.lastrowid:
                self.id = cursor.lastrowid

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
