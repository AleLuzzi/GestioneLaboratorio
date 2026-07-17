class MovIngressoMerce:
    """Record movimenti per tabella `ingresso_merce`.

    Il progetto (controller + UI) inserisce righe con 9 campi in questo ordine:
      (prog_acq, data, num_ddt, fornitore, taglio, peso_i, peso_f, lotto_chiuso, id_merc)

    Nota naming DB:
    - nel DB la colonna relativa al progressivo è chiamata `progressivo_acq` (non `prog_acq`).
    - questo modello mantiene l'attributo `prog_acq` ma nelle query usa `progressivo_acq`.
    """

    __slots__ = (
        "prog_acq",
        "data",
        "num_ddt",
        "fornitore",
        "taglio",
        "peso_i",
        "peso_f",
        "lotto_chiuso",
        "id_merc",
    )

    def __init__(
        self,
        prog_acq=None,
        data=None,
        num_ddt="",
        fornitore=None,
        taglio="",
        peso_i=None,
        peso_f=None,
        lotto_chiuso="no",
        id_merc=None,
    ):
        self.prog_acq = prog_acq
        self.data = data
        self.num_ddt = num_ddt
        self.fornitore = fornitore
        self.taglio = taglio
        self.peso_i = peso_i
        self.peso_f = peso_f
        self.lotto_chiuso = lotto_chiuso
        self.id_merc = id_merc

    @classmethod
    def from_row(cls, row):
        """Costruisce un oggetto da una riga del DB."""
        if row is None:
            return None

        if len(row) == 9:
            data = row
        elif len(row) == 10:
            data = row[1:]
        else:
            raise ValueError(
                f"Riga non supportata per ingresso_merce: len(row)={len(row)}"
            )

        return cls(
            prog_acq=data[0],
            data=data[1],
            num_ddt=data[2],
            fornitore=data[3],
            taglio=data[4],
            peso_i=data[5],
            peso_f=data[6],
            lotto_chiuso=data[7],
            id_merc=data[8],
        )

    def params_insert(self):
        """Valori per INSERT INTO ingresso_merce VALUES (%s, ...)."""
        return (
            self.prog_acq,
            self.data,
            self.num_ddt,
            self.fornitore,
            self.taglio,
            self.peso_i,
            self.peso_f,
            self.lotto_chiuso,
            self.id_merc,
        )

    def params_where(self):
        """Valori per WHERE basata sulla chiave composta (tutti i campi noti)."""
        return (
            self.prog_acq,
            self.data,
            self.num_ddt,
            self.fornitore,
            self.taglio,
            self.peso_i,
            self.peso_f,
            self.lotto_chiuso,
            self.id_merc,
        )

    def params_update(self):
        """Valori per UPDATE: SET (insert) + WHERE (where)."""
        return self.params_insert() + self.params_where()

    @classmethod
    def fetch_by_progressivo(cls, cursor, progressivo_acq):
        """Recupera tutti i movimenti associati a un dato `progressivo_acq`."""
        cursor.execute(
            """
            SELECT * FROM ingresso_merce
            WHERE progressivo_acq = %s
            """,
            (progressivo_acq,),
        )
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def fetch_all(cls, cursor):
        """Recupera tutti i movimenti presenti in `ingresso_merce` ordinati per data decrescente."""
        cursor.execute("SELECT * FROM ingresso_merce ORDER BY data_acq DESC, progressivo_acq DESC")
        return [cls.from_row(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_key(cls, cursor, key):
        """Cerca una singola riga tramite chiave composta."""
        if isinstance(key, cls):
            params = key.params_where()
        else:
            if len(key) != 9:
                raise ValueError(
                    "Chiave composta ingresso_merce deve contenere 9 valori."
                )
            params = tuple(key)

        cursor.execute(
            """
            SELECT * FROM ingresso_merce
            WHERE progressivo_acq = %s
              AND data_acq = %s
              AND documento = %s
              AND fornitore = %s
              AND prodotto = %s
              AND quantita = %s
              AND residuo = %s
              AND lotto_chiuso = %s
              AND id_merc = %s
            """,
            params,
        )
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    def save(self, cursor, conn):
        """Aggiorna il record corrente tramite `progressivo_acq`."""
        update_values = self.params_insert()
        query_params = update_values + (self.prog_acq,)

        cursor.execute(
            """
            UPDATE ingresso_merce
            SET progressivo_acq = %s,
                data_acq = %s,
                documento = %s,
                fornitore = %s,
                prodotto = %s,
                quantita = %s,
                residuo = %s,
                lotto_chiuso = %s,
                id_merc = %s
            WHERE progressivo_acq = %s
            """,
            query_params,
        )
        conn.commit()

    def insert(self, cursor, conn):
        """Esegue INSERT del nuovo record sul database."""
        cursor.execute(
            """
            INSERT INTO ingresso_merce
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            self.params_insert(),
        )
        conn.commit()

    def delete(self, cursor, conn):
        """Elimina il record corrente tramite chiave composta."""
        cursor.execute(
            """
            DELETE FROM ingresso_merce
            WHERE progressivo_acq = %s
              AND data_acq = %s
              AND documento = %s
              AND fornitore = %s
              AND prodotto = %s
              AND quantita = %s
              AND residuo = %s
              AND lotto_chiuso = %s
              AND id_merc = %s
            """,
            self.params_where(),
        )
        conn.commit()

