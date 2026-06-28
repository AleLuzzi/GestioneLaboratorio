class Merceologia:
    """Record merceologia (tabella `merceologie`).

    Allineato ai campi usati da `Laboratorio/anagrafica_merceologie.py`:
      - ID
      - merceologia
      - id_reparto
      - flag1_inv
      - flag2_taglio
      - flag3_ing_base
    """

    __slots__ = (
        "id",
        "merceologia",
        "id_reparto",
        "flag1_inv",
        "flag2_taglio",
        "flag3_ing_base",
    )

    def __init__(
        self,
        id=None,
        merceologia="",
        id_reparto=None,
        flag1_inv=0,
        flag2_taglio=0,
        flag3_ing_base=0,
    ):
        self.id = id
        self.merceologia = merceologia
        self.id_reparto = id_reparto
        self.flag1_inv = int(flag1_inv) if flag1_inv is not None else 0
        self.flag2_taglio = int(flag2_taglio) if flag2_taglio is not None else 0
        self.flag3_ing_base = int(flag3_ing_base) if flag3_ing_base is not None else 0

    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto a partire da una riga fetchata.

        Supporta sia righe di tipo `SELECT * FROM merceologie` (ordine:
        ID, merceologia, id_reparto, flag1_inv, flag2_taglio, flag3_ing_base)
        sia righe esplicite con i campi nello stesso ordine.
        """
        return cls(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
        )

    def params_insert(self):
        """Valori per INSERT INTO merceologie(merceologia,id_reparto,flag1_inv,flag2_taglio,flag3_ing_base) VALUES (...)."""
        return (
            self.merceologia,
            self.id_reparto,
            self.flag1_inv,
            self.flag2_taglio,
            self.flag3_ing_base,
        )

    def params_update(self):
        """Valori per UPDATE merceologie SET ... WHERE ID = %s."""
        return (
            self.merceologia,
            self.id_reparto,
            self.flag1_inv,
            self.flag2_taglio,
            self.flag3_ing_base,
            self.id,
        )

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutte le merceologie presenti nel database."""
        cursor.execute(
            "SELECT id, merceologia, id_reparto, flag1_inv, flag2_taglio, flag3_ing_base FROM merceologie"
        )
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, cursor, m_id):
        """Cerca una singola merceologia tramite il suo ID."""
        cursor.execute(
            "SELECT id, merceologia, id_reparto, flag1_inv, flag2_taglio, flag3_ing_base FROM merceologie WHERE id = %s",
            (m_id,),
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def insert(self, cursor, conn):
        """Esegue l'inserimento del record corrente."""
        cursor.execute(
            "INSERT INTO merceologie(merceologia, id_reparto, flag1_inv, flag2_taglio, flag3_ing_base) "
            "VALUES (%s, %s, %s, %s, %s)",
            self.params_insert(),
        )
        conn.commit()

    def save(self, cursor, conn):
        """Esegue l'aggiornamento del record corrente sul database."""
        cursor.execute(
            "UPDATE merceologie "
            "SET merceologia = %s, id_reparto = %s, flag1_inv = %s, flag2_taglio = %s, flag3_ing_base = %s "
            "WHERE id = %s",
            self.params_update(),
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente dal database usando il suo ID."""
        cursor.execute("DELETE FROM merceologie WHERE id = %s", (self.id,))
        conn.commit()

