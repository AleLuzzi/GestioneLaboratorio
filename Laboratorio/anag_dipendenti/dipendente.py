class Dipendente:
    """Record dipendente (tabella `dipendenti`), allineato a `anagrafica_dipendenti`."""

    __slots__ = ("id", "nome")

    def __init__(self, id=None, nome=""):
        self.id = id
        self.nome = nome

    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto da una riga della tabella dipendenti (id, nome)."""
        return cls(row[0], row[1])

    def params_insert(self):
        """Valori per INSERT INTO dipendenti(nome VALUES (...)."""
        return (self.nome,)

    def params_update(self):
        """Valori per UPDATE ... SET nome WHERE ID = %s."""
        return (self.nome, self.id)

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i dipendenti presenti nel database."""
        cursor.execute("SELECT id, nome FROM dipendenti")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, f_id):
        """Cerca un singolo dipendente tramite il suo ID identificativo."""
        cursor.execute("SELECT id, nome FROM dipendenti WHERE id = %s", (f_id,))
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Esegue l'aggiornamento (UPDATE) del record corrente sul database."""
        cursor.execute(
            "UPDATE dipendenti SET nome = %s WHERE id = %s",
            self.params_update()
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
                "INSERT INTO dipendenti (nome) VALUES (%s)",
                self.params_insert()
            )
            
            # Recupera l'ID generato automaticamente dal database
            if hasattr(cursor, "lastrowid") and cursor.lastrowid:
                self.id = cursor.lastrowid
                
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e


