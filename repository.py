from db import connect_to_db

# -- Přidání úkolu --
def pridat_ukol(nazev, popis, conn=None):
    """
    Přidá nový úkol do tabulky ukoly s daným názvem a popisem.
    Stav i id se nastavují automaticky.
    """
    if not nazev.strip() or not popis.strip():
        raise ValueError("Název a popis úkolu musí být vyplněné!")
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    conn.commit()
    cursor.close()
    if close_conn:
        conn.close()

# -- Výpis úkolů --
def zobrazit_ukoly(only_open=False, conn=None):
    """
    Vrací seznam úkolů z databáze. Pokud only_open=True, filtruje na 'Nezahájeno' a 'Probíhá'.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    cursor = conn.cursor()
    if only_open:
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
    else:
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly")
    vysledek = cursor.fetchall()
    cursor.close()
    if close_conn:
        conn.close()
    return vysledek

# -- Aktualizace úkolu --
def aktualizovat_ukol(ukol_id, novy_stav, conn=None):
    """
    Změní stav úkolu podle id (novy_stav musí být 'Probíhá' nebo 'Hotovo').
    """
    if novy_stav not in ('Probíhá', 'Hotovo'):
        raise ValueError("Neplatný stav úkolu!")
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    cursor = conn.cursor()
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, ukol_id))
    if cursor.rowcount == 0:
        cursor.close()
        if close_conn:
            conn.close()
        raise Exception("Úkol s tímto ID neexistuje!")
    conn.commit()
    cursor.close()
    if close_conn:
        conn.close()

# -- Odstranění úkolu --
def odstranit_ukol(ukol_id, conn=None):
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    if close_conn:
        conn.close()
    return deleted

# -- Vytvoření tabulky --
def vytvoreni_tabulky(conn=None):
    """
    Vytvoří tabulku 'ukoly', pokud ještě neexistuje (používá se na začátku projektu).
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(100) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.close()
    if close_conn:
        conn.close()
