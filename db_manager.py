import sqlite3

DB_NAME = "database.db"


# =========================
# Připojení k databázi
# =========================
def connect():
    return sqlite3.connect(DB_NAME)


# =========================
# Inicializace databáze
# =========================
def init_db():
    conn = connect()
    cursor = conn.cursor()

    # Tabulka akce
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS akce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT NOT NULL,
            datum TEXT NOT NULL,
            misto TEXT NOT NULL
        )
    """)

    # Tabulka účastníci
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ucastnici (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jmeno TEXT NOT NULL,
            trida TEXT NOT NULL
        )
    """)

    # Vazební tabulka registrace (M:N vztah)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            akce_id INTEGER NOT NULL,
            ucastnik_id INTEGER NOT NULL,
            FOREIGN KEY (akce_id) REFERENCES akce(id) ON DELETE CASCADE,
            FOREIGN KEY (ucastnik_id) REFERENCES ucastnici(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# CRUD - AKCE
# =========================================================
def create_akce(nazev, datum, misto):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO akce (nazev, datum, misto) VALUES (?, ?, ?)",
        (nazev, datum, misto)
    )
    conn.commit()
    conn.close()


def get_all_akce():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM akce")
    data = cursor.fetchall()
    conn.close()
    return data


def delete_akce(akce_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM akce WHERE id = ?", (akce_id,))
    conn.commit()
    conn.close()


# =========================================================
# CRUD - ÚČASTNÍCI
# =========================================================
def create_ucastnik(jmeno, trida):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ucastnici (jmeno, trida) VALUES (?, ?)",
        (jmeno, trida)
    )
    conn.commit()
    conn.close()


def get_all_ucastnici():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ucastnici")
    data = cursor.fetchall()
    conn.close()
    return data


def filter_ucastnici_by_trida(trida):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM ucastnici WHERE trida LIKE ?",
        (f"%{trida}%",)
    )
    data = cursor.fetchall()
    conn.close()
    return data


def delete_ucastnik(ucastnik_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ucastnici WHERE id = ?", (ucastnik_id,))
    conn.commit()
    conn.close()


# =========================================================
# REGISTRACE (VAZBY)
# =========================================================
def create_registrace(akce_id, ucastnik_id):
    conn = connect()
    cursor = conn.cursor()

    # kontrola existence akce
    cursor.execute("SELECT id FROM akce WHERE id = ?", (akce_id,))
    akce = cursor.fetchone()

    # kontrola existence účastníka
    cursor.execute("SELECT id FROM ucastnici WHERE id = ?", (ucastnik_id,))
    ucastnik = cursor.fetchone()

    if not akce or not ucastnik:
        conn.close()
        return False

    cursor.execute(
        "INSERT INTO registrace (akce_id, ucastnik_id) VALUES (?, ?)",
        (akce_id, ucastnik_id)
    )
    conn.commit()
    conn.close()
    return True


def get_all_registrace():
    conn = connect()
    cursor = conn.cursor()

    # JOIN pro hezčí výpis (název akce + jméno účastníka)
    cursor.execute("""
        SELECT registrace.id, akce.nazev, ucastnici.jmeno, ucastnici.trida
        FROM registrace
        JOIN akce ON registrace.akce_id = akce.id
        JOIN ucastnici ON registrace.ucastnik_id = ucastnici.id
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def delete_registrace(registrace_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registrace WHERE id = ?", (registrace_id,))
    conn.commit()
    conn.close()
