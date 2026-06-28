class Ingrediente:
    """Record ingrediente (tabella `ingredienti_base`), allineato a `anagrafica_ingredienti`."""

    __slots__ = ("id", "ingrediente_base", "cod_ean", "flag1_allergene", "merceologia")

    def __init__(self, id=None, ingrediente_base="", cod_ean="", flag1_allergene=0, merceologia=""):
        self.id = id
        self.ingrediente_base = ingrediente_base
        self.cod_ean = cod_ean
        self.flag1_allergene = int(flag1_allergene)
        self.merceologia = merceologia

    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto da una riga della tabella ingredienti_base (id, ingrediente_base, cod_ean, flag1_allergene, merceologia)."""
        return cls(row[0], row[1], row[2], row[3], row[4])

    def params_insert(self):
        """Valori per INSERT INTO ingredienti_base(ingrediente_base, cod_ean, flag1_allergene, merceologia) VALUES (...)."""
        return (self.ingrediente_base, self.cod_ean, self.flag1_allergene, self.merceologia)

    def params_update(self):
        """Valori per UPDATE ... SET ingrediente_base, cod_ean, flag1_allergene, merceologia WHERE id = %s."""
        return (self.ingrediente_base, self.cod_ean, self.flag1_allergene, self.merceologia, self.id)

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti gli ingredienti presenti nel database."""
        cursor.execute("SELECT id, ingrediente_base, cod_ean, flag1_allergene, merceologia FROM ingredienti_base")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, f_id):
        """Cerca un singolo ingrediente tramite il suo ID identificativo."""
        cursor.execute(
            "SELECT id, ingrediente_base, cod_ean, flag1_allergene, merceologia FROM ingredienti_base WHERE id = %s",
            (f_id,),
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Esegue l'aggiornamento (UPDATE) del record corrente sul database."""
        cursor.execute(
            "UPDATE ingredienti_base SET ingrediente_base = %s, cod_ean = %s, flag1_allergene = %s, merceologia = %s WHERE id = %s",
            self.params_update(),
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente dal database utilizzando il suo ID."""
        if self.id is None:
            raise ValueError("Impossibile eliminare un ingrediente privo di ID.")

        try:
            cursor.execute("DELETE FROM ingredienti_base WHERE id = %s", (self.id,))
            conn.commit()
            self.id = None
        except Exception as e:
            conn.rollback()
            raise e

    def insert(self, cursor, conn):
        """Esegue l'inserimento (INSERT) del nuovo ingrediente sul database."""
        try:
            cursor.execute(
                "INSERT INTO ingredienti_base (ingrediente_base, cod_ean, flag1_allergene, merceologia) VALUES (%s, %s, %s, %s)",
                self.params_insert(),
            )

            if hasattr(cursor, "lastrowid") and cursor.lastrowid:
                self.id = cursor.lastrowid

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e