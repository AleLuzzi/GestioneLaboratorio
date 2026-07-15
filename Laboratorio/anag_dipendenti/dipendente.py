class Dipendente:
    """Record dipendente (tabella `dipendenti`, campi: id, nome, email, reparto)."""

    __slots__ = ("id", "nome", "email", "reparto")

    def __init__(self, id=None, nome="", email="", reparto=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.reparto = reparto


    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto da una riga del DB.

        Supporta righe con:
        - (id, nome)
        - (id, nome, email)
        - (id, nome, email, reparto)
        """
        if len(row) == 2:
            return cls(row[0], row[1], "", None)
        if len(row) == 3:
            return cls(row[0], row[1], row[2], None)
        return cls(row[0], row[1], row[2], row[3])


    def params_insert(self):
        """Valori per INSERT INTO dipendenti (nome, email, reparto)."""
        return (self.nome, self.email, self.reparto)


    def params_update(self):
        """Valori per UPDATE dipendenti SET nome=%s, email=%s, reparto=%s WHERE id=%s."""
        return (self.nome, self.email, self.reparto, self.id)



    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i dipendenti presenti nel database."""
        cursor.execute(
            "SELECT id, nome, email, reparto FROM dipendenti"
        )
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, f_id):
        """Cerca un singolo dipendente tramite il suo ID identificativo."""
        cursor.execute(
            "SELECT id, nome, email, reparto FROM dipendenti WHERE id = %s",
            (f_id,),
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None


    def save(self, cursor, conn):
        """Esegue l'aggiornamento (UPDATE) del record corrente sul database."""
        cursor.execute(
            "UPDATE dipendenti SET nome = %s, email = %s, reparto = %s WHERE id = %s",
            self.params_update(),
        )
        conn.commit()


    def delete(self, cursor, conn):
        """Elimina il record corrente dal database utilizzando il suo ID."""
        if self.id is None:
            raise ValueError("Impossibile eliminare un dipendente privo di ID.")

        try:
            cursor.execute("DELETE FROM dipendenti WHERE id = %s", (self.id,))
            conn.commit()
            self.id = None  # Resetta l'ID per riflettere lo stato reale
        except Exception as e:
            conn.rollback()
            raise e

    def insert(self, cursor, conn):
        """Esegue l'inserimento (INSERT) del nuovo dipendente sul database."""
        try:
            cursor.execute(
                "INSERT INTO dipendenti (nome, email, reparto) VALUES (%s, %s, %s)",
                self.params_insert(),
            )


            # Recupera l'ID generato automaticamente dal database
            if hasattr(cursor, "lastrowid") and cursor.lastrowid:
                self.id = cursor.lastrowid

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

